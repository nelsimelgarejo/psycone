from django.shortcuts import redirect, render, get_object_or_404
from sentirsebien.models import Perfil, FichaSociodemografica, ComponenteBienestar
from sentirsebien.forms import FichaSociodemograficaForm

# Create your views here.
def home(request):
    perfil = get_object_or_404(Perfil, usuario__username = request.user)
    is_ficha = False

    if not ComponenteBienestar.objects.filter(perfil=perfil).exists():
        """Permite crear los componentes para el nuevo usuario"""
        componentes = ComponenteBienestar.objects.filter(perfil=None)
        for componente in componentes:
            ComponenteBienestar.objects.create(
                perfil = perfil,
                topico = componente.topico,
                completado = componente.completado
            )

    if FichaSociodemografica.objects.filter(perfil = perfil).exists():
        is_ficha = True

    ctx = {
        'perfil': perfil,
        'is_ficha' : is_ficha
    }

    return render(request, 'dashboard/home.html', ctx)


def ficha_sociodemografica(request):
    perfil = get_object_or_404(Perfil, usuario__username = request.user)
    if request.method == 'POST':
        form = FichaSociodemograficaForm(request.POST)
        if form.is_valid():
            ficha =  form.save(commit=False)
            ficha.perfil = perfil
            ficha.save()
            
    return redirect('home')

def ficha_form(request):

    return render(request, 'dashboard/ficha_form.html')

def ver_perfil(request):
    perfil = get_object_or_404(Perfil, usuario__username = request.user)

    return render(request, 'dashboard/perfil.html', {'perfil':perfil})