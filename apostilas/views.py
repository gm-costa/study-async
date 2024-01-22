from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import Apostila, ViewApostila


def adicionar_apostilas(request):
    apostilas = Apostila.objects.filter(user=request.user)
    # TODO: Criar as tags
    views_totais = ViewApostila.objects.filter(apostila__user = request.user).count()

    context = {
        'apostilas': apostilas, 
        'views_totais': views_totais,
    }
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        arquivo = request.FILES['arquivo']

        apostila = Apostila(user=request.user, titulo=titulo, arquivo=arquivo)
        try:
            apostila.save()
            messages.add_message(
                request, messages.SUCCESS, 'Apostila adicionada com sucesso.'
            )
        except:
            messages.add_message(
                request, messages.ERROR, 'Não foi possível adicionar os dados !'
            )
        
        return redirect(reverse('adicionar_apostilas'))

    else:
        return render(request, 'adicionar_apostilas.html', context)


def apostila(request, id):
    apostila = get_object_or_404(Apostila, id=id)

    view = ViewApostila(
        ip=request.META['REMOTE_ADDR'],
        apostila=apostila
    )
    view.save()

    views_unicas = ViewApostila.objects.filter(apostila=apostila).values('ip').distinct().count()
    views_totais = ViewApostila.objects.filter(apostila=apostila).count()

    context = {
        'apostila': apostila,
        'views_unicas': views_unicas,
        'views_totais': views_totais,
    }
    return render(request, 'apostila.html', context)
