from django.forms import ModelForm,Textarea
from .models import Product, Categoria,Checkout

#PRODUCTOS
class add_product_form(ModelForm):
    class Meta:
        model = Product
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria', 'imagen']

#CATEGORIA
class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

#checkout
class CheckoutForm(ModelForm):
    class Meta:
        model = Checkout
        fields = ['nombre', 'direccion', 'telefono', 'correo', 'metodo_pago']
        widgets = {
            'direccion': Textarea(attrs={'rows': 3}),
        }

