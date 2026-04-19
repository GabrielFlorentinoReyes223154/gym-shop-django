import pytest
from django.test import Client
from django.contrib.auth.models import User
from tasks.models import Product, Categoria, Carrito, ItemCarrito

# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def usuario(db):
    return User.objects.create_user(
        username='testuser',
        password='Password123!'
    )

@pytest.fixture
def categoria(db):
    return Categoria.objects.create(
        nombre='Suplementos',
        descripcion='Proteínas y vitaminas'
    )

@pytest.fixture
def producto(db, categoria):
    return Product.objects.create(
        nombre='Proteína Whey',
        descripcion='Proteína de suero de leche',
        precio=500.00,
        stock=10,
        categoria=categoria
    )

# ── Pruebas de Autenticación (signup / signin) ─────────────────────────────────

class TestSignup:

    def test_signup_exitoso(self, client, db):
        """TC-001: Registro con datos válidos redirige al home"""
        response = client.post('/signup/', {
            'username': 'nuevousuario',
            'password1': 'Password123!',
            'password2': 'Password123!'
        })
        assert response.status_code == 302
        assert User.objects.filter(username='nuevousuario').exists()

    def test_signup_passwords_no_coinciden(self, client, db):
        """TC-002: Passwords distintos muestran error — DEF-AUTH-001"""
        response = client.post('/signup/', {
            'username': 'nuevousuario',
            'password1': 'Password123!',
            'password2': 'OtraPassword!'
        })
        assert response.status_code == 200
        assert 'error' in response.context

    def test_signup_usuario_duplicado(self, client, usuario, db):
        """TC-003: Usuario ya existente muestra error"""
        response = client.post('/signup/', {
            'username': 'testuser',
            'password1': 'Password123!',
            'password2': 'Password123!'
        })
        assert response.status_code == 200
        assert 'error' in response.context


class TestSignin:

    def test_signin_exitoso(self, client, usuario, db):
        """TC-004: Login con credenciales correctas redirige al home"""
        response = client.post('/signin/', {
            'username': 'testuser',
            'password': 'Password123!'
        })
        assert response.status_code == 302

    def test_signin_credenciales_incorrectas(self, client, db):
        """TC-005: Login con credenciales incorrectas muestra error"""
        response = client.post('/signin/', {
            'username': 'noexiste',
            'password': 'wrongpassword'
        })
        assert response.status_code == 200
        assert 'error' in response.context


# ── Pruebas del Carrito ────────────────────────────────────────────────────────

class TestCarrito:

    def test_agregar_producto_autenticado(self, client, usuario, producto, db):
        """TC-006: Usuario autenticado puede agregar producto al carrito"""
        client.login(username='testuser', password='Password123!')
        response = client.post(f'/carrito/agregar/{producto.id}/')
        assert response.status_code == 302
        carrito = Carrito.objects.get(usuario=usuario, activo=True)
        assert ItemCarrito.objects.filter(carrito=carrito, producto=producto).exists()

    def test_agregar_producto_no_autenticado(self, client, producto, db):
        """TC-007: Usuario no autenticado es redirigido al login"""
        response = client.post(f'/carrito/agregar/{producto.id}/')
        assert response.status_code == 302
        assert '/signin/' in response.url

    def test_actualizar_cantidad_minimo_uno(self, client, usuario, producto, db):
        """TC-008: La cantidad nunca baja de 1 — DEF-CART-001"""
        client.login(username='testuser', password='Password123!')
        carrito = Carrito.objects.create(usuario=usuario, activo=True)
        item = ItemCarrito.objects.create(carrito=carrito, producto=producto, cantidad=1)
        response = client.post(f'/carrito/actualizar/{item.id}/', {
            'cantidad': -5
        })
        item.refresh_from_db()
        assert item.cantidad >= 1


# ── Pruebas de Checkout ────────────────────────────────────────────────────────

class TestCheckout:

    def test_checkout_carrito_vacio_redirige(self, client, usuario, db):
        """TC-009: Checkout con carrito vacío redirige al carrito"""
        client.login(username='testuser', password='Password123!')
        response = client.get('/checkout/')
        assert response.status_code == 302
        assert 'carrito' in response.url