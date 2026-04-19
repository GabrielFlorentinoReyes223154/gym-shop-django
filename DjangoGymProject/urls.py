"""
URL configuration for DjangoGymProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('signup/', views.signup, name = 'signup'), 
    path('logout/', views.signout, name = 'logout'),
    path('signin/', views.signin, name = 'signin'),
    #PRODUCTOS
    path('productos/', views.products, name = 'products'),
    path('productos/nuevo/', views.product_create, name='product_create'),
    path('productos/editar/<int:product_id>/', views.product_update, name='product_update'),
    path('tasks/<int:product_id>/delete', views.product_delete, name = 'product_delete'),
    #CATEGORIAS
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/nueva/', views.categoria_create, name='categoria_create'),
    path('categorias/editar/<int:categoria_id>/', views.categoria_update, name='categoria_update'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('categorias/eliminar/<int:categoria_id>/', views.categoria_delete, name='categoria_delete'),

    #CHECKOUT
    path('checkout/', views.checkout_view, name='checkout'),
    path('listar_pedidos/', views.listar_pedidos, name='listar_pedidos'),
    path('actualizar_pedido/<int:pedido_id>/editar/', views.actualizar_pedido, name='actualizar_pedido'),
    path('eliminar_pedido/<int:pedido_id>/eliminar/', views.eliminar_pedido, name='eliminar_pedido'),

    #CARRITO
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),

    #PEDIDOS
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),

    #CLIENTES
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/<int:user_id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:user_id>/eliminar/', views.eliminar_cliente, name='eliminar_cliente')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
