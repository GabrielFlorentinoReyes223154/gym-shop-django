from django.forms import ModelForm,Textarea,ValidationError
from .models import Product, Categoria,Checkout

#PRODUCTOS
class add_product_form(ModelForm):
    class Meta:
        model = Product
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria', 'imagen']

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise ValidationError('El precio no puede ser negativo.')
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise ValidationError('El stock no puede ser negativo.')
        return stock

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

