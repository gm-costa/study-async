from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.db import transaction
from .models import Apostila, ViewApostila, Tag


def adicionar_apostilas(request):
    apostilas = Apostila.objects.filter(user=request.user)

    views_totais = ViewApostila.objects.filter(apostila__user = request.user).count()

    if request.method == 'GET':
        tags_busca = request.GET.get('tags-busca')

        list_tags = []

        if tags_busca:
            list_tags = tags_busca.split(';')
            apostilas = apostilas.filter(tags__tag__in=list_tags)

        context = {
            'apostilas': apostilas, 
            'views_totais': views_totais,
        }

        return render(request, 'adicionar_apostilas.html', context)
    
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        tags = request.POST.get('tags')

        context = {
            'titulo': titulo,
            'tags': tags,
        }

        if not titulo:
            messages.add_message(request, messages.ERROR, 'Título não informado !')
            return render(request, 'adicionar_apostilas.html', context)
        
        if not request.FILES:
            messages.add_message(request, messages.ERROR, 'Arquivo não escolhido !')
            return render(request, 'adicionar_apostilas.html', context)
        
        arquivo = request.FILES['arquivo']

        if not tags:
            context['arquivo'] = arquivo.name
            print(context)
            messages.add_message(request, messages.ERROR, 'Nenhuma tag informada !')
            return render(request, 'adicionar_apostilas.html', context)
        else:
            list_tags = tags.split(';')

        apostila = Apostila(user=request.user, titulo=titulo, arquivo=arquivo)
        try:
            with transaction.atomic():
                apostila.save()
                # apostila.tags.add(*list_tags)
                for tag in list_tags:
                    tag = tag.strip().lower()
                    if not Tag.objects.filter(tag=tag):
                        nova_tag = Tag(tag=tag)
                        nova_tag.save()
                        apostila.tags.add(nova_tag)

                apostila.save()

                messages.add_message(
                    request, messages.SUCCESS, 'Apostila adicionada com sucesso.'
                )
        except:
            messages.add_message(
                request, messages.ERROR, 'Não foi possível adicionar os dados !'
            )
        
        return redirect(reverse('adicionar_apostilas'))


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

