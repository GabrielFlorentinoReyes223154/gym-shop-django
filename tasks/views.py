from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Permission
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError, transaction
from .forms import add_product_form, CategoriaForm, CheckoutForm
from .models import Product, Categoria, Carrito, ItemCarrito, Checkout,CheckoutItem
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html',{
        'products':products
    })

'''
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form' : UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password= request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form' : UserCreationForm,
                    'error': 'Usuario ya existente'
                })
        return render(request, 'signup.html', {
                    'form' : UserCreationForm,
                    'error': 'Las constrasenas no coinciden'
                })
'''

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=request.POST['username'],
                        password=request.POST['password1']
                    )
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Usuario ya existente'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm
        }) 
    else:
        user =  authenticate(request, username=request.POST['username'],password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': 'Usuario o contrasena incorrecto'
            })
        else:
            login(request, user)
            return redirect('home')

#PRODUCTOS
def products(request):
    products = Product.objects.all()

    return render(request, 'product_list.html',{
        'products': products
    })

@permission_required('tasks.add_product')
def product_create(request):
    if request.method == 'POST':
        form = add_product_form(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.user = request.user
            new_product.save()
            return redirect('products')
    else:
        form = add_product_form()
    return render(request, 'product_form.html', {'form': form})
        
@permission_required('tasks.add_product') 
def product_update(request, product_id):
    producto = get_object_or_404(Product, pk=product_id)
    form = add_product_form(request.POST or None, request.FILES or None, instance=producto)
    if form.is_valid():
        form.save()
        return redirect('products')
    return render(request, 'product_form.html', {'form': form})

@permission_required('tasks.add_product') 
def product_delete(request, product_id):
    producto = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('products')
    return render(request, 'product_confirm_delete.html', {'producto': producto})
    
#CATEGORIAS
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria_list.html', {'categorias': categorias})

@permission_required('tasks.add_product')
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'categoria_form.html', {'form': form})

@permission_required('tasks.add_product')
def categoria_update(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        return redirect('categoria_list')
    return render(request, 'categoria_form.html', {'form': form})

@permission_required('tasks.add_product')
def categoria_delete(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categoria_list')
    return render(request, 'categoria_confirm_delete.html', {'categoria': categoria})

def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    productos = Product.objects.filter(categoria=categoria)
    return render(request, 'productos_por_categoria.html', {
        'categoria': categoria,
        'productos': productos
    })

#CARRITO
@login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user, activo=True)
    items = carrito.items.all()
    total = sum(item.producto.precio * item.cantidad for item in items)

    return render(request, 'carrito.html', {
        'carrito': carrito,
        'items': items,
        'total': total
    })

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Product, pk=producto_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user, activo=True)

    item, creado_item = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)

    if not creado_item:
        item.cantidad += 1
        item.save()

    messages.success(request, f'"{producto.nombre}" fue agregado al carrito.')
    return redirect('home') 

@login_required
def actualizar_cantidad(request, item_id):
    item = get_object_or_404(ItemCarrito, pk=item_id, carrito__usuario=request.user)

    if request.method == 'POST':
        nueva_cantidad = int(request.POST.get('cantidad', 1))
        item.cantidad = max(1, nueva_cantidad)  
        item.save()

    return redirect('ver_carrito')

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, pk=item_id, carrito__usuario=request.user)

    if request.method == 'POST':
        item.delete()

    return redirect('ver_carrito')

#CHECKOUT(PEDIDOS)
@login_required
def checkout_view(request):
    carrito = Carrito.objects.filter(usuario=request.user, activo=True).first()
    if not carrito or not carrito.items.exists():
        return redirect('ver_carrito')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            checkout = form.save(commit=False)
            checkout.usuario = request.user
            checkout.save()

            for item in carrito.items.all():
                CheckoutItem.objects.create(
                    checkout=checkout,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    precio_unitario=item.producto.precio
                )

            carrito.activo = False
            carrito.save()
            return redirect('home')
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form})


@permission_required('tasks.change_checkout', raise_exception=True)
def listar_pedidos(request):
    pedidos = Checkout.objects.all().order_by('-creado')
    return render(request, 'pedidos_list.html', {'pedidos': pedidos})


@permission_required('tasks.change_checkout', raise_exception=True)
def actualizar_pedido(request, pedido_id):
    pedido = get_object_or_404(Checkout, pk=pedido_id)
    items = pedido.items.all()

    if request.method == 'POST':
        pedido.estado = request.POST.get('estado')
        pedido.save()
        return redirect('listar_pedidos')

    return render(request, 'pedido_update.html', {
        'pedido': pedido,
        'items': items
    })

@permission_required('tasks.delete_checkout', raise_exception=True)
def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Checkout, pk=pedido_id)

    if pedido.estado != 'entregado':
        return redirect('listar_pedidos')  

    if request.method == 'POST':
        pedido.delete()
        return redirect('listar_pedidos')

    return render(request, 'pedido_confirm_delete.html', {'pedido': pedido})

#CLIENTES
@permission_required('auth.view_user', raise_exception=True)
def listar_clientes(request):
    clientes = User.objects.annotate(
        pedidos=Count('checkout')
    ).order_by('-is_staff', 'username')
    return render(request, 'clientes_list.html', {'clientes': clientes})

@permission_required('auth.change_user', raise_exception=True)
def editar_cliente(request, user_id):
    cliente = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        is_staff = request.POST.get('is_staff') == 'on'
        cliente.is_staff = is_staff
        cliente.save()

        if is_staff:
            # Obtener permisos de los modelos necesarios
            modelos = [Checkout, Product, Categoria]
            permisos = Permission.objects.filter(
                content_type__model__in=[model._meta.model_name for model in modelos]
            )
            cliente.user_permissions.set(permisos)
        else:
            cliente.user_permissions.clear()

        return redirect('listar_clientes')

    return render(request, 'cliente_update.html', {'cliente': cliente})

@permission_required('auth.delete_user', raise_exception=True)
def eliminar_cliente(request, user_id):
    cliente = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')

    return render(request, 'cliente_confirm_delete.html', {'cliente': cliente})


@login_required
def mis_pedidos(request):
    pedidos = Checkout.objects.filter(usuario=request.user).order_by('-creado')

    for pedido in pedidos:
        pedido.total = sum(item.subtotal() for item in pedido.items.all())

    return render(request, 'mis_pedidos.html', {'pedidos': pedidos})
