from .models import Categoria

def categorias_nav(request):
    categorias = Categoria.objects.all()
    return {'categorias_nav': categorias}
