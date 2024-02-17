from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from flashcard.models import Categoria, Desafio, Flashcard, FlashcardDesafio

@login_required(login_url='login')
def novo_flashcard(request):
    
    categorias = Categoria.objects.all()
    dificuldades = Flashcard.DIFICULDADE_CHOICES
    flashcards = Flashcard.objects.filter(user=request.user)

    categoria_filtro = request.GET.get('categoria-filtro')
    dificuldade_filtro = request.GET.get('dificuldade-filtro')

    if categoria_filtro:
        flashcards = flashcards.filter(categoria__id=categoria_filtro)
        categoria_filtro = Categoria.objects.get(id=categoria_filtro)

    if dificuldade_filtro:
        flashcards = flashcards.filter(dificuldade=dificuldade_filtro)
            
    context = {
        'categorias': categorias,
        'dificuldades': dificuldades,
        'flashcards': flashcards,
        'cat_filtro': categoria_filtro,
        'dif_filtro': dificuldade_filtro,
    }
    if request.method == 'POST':
        pergunta = request.POST.get('pergunta')
        resposta = request.POST.get('resposta')
        categoria = request.POST.get('categoria')
        dificuldade = request.POST.get('dificuldade')

        if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
            messages.add_message(
                request, messages.ERROR, 'Preencha os campos de pergunta e resposta'
            )
            return redirect(reverse('novo_flashcard'))

        flashcard = Flashcard(
            user=request.user,
            pergunta=pergunta,
            resposta=resposta,
            categoria_id=categoria,
            dificuldade=dificuldade,
        )

        try:
            flashcard.save()
            messages.add_message(
                request, messages.SUCCESS, 'Flashcard criado com sucesso'
            )
        except:
            messages.add_message(
                request, messages.ERROR, 'Não foi possível salvar os dados!')
            
        return redirect(reverse('novo_flashcard'))
        
    else:

        return render(request, 'novo_flashcard.html', context)


@login_required(login_url='login')
def deletar_flashcard(request, id):
    flashcard = get_object_or_404(Flashcard, id=id)
    if flashcard.user == request.user:
        flashcard.delete()
        messages.add_message(
            request, messages.SUCCESS, 'Flashcard deletado com sucesso!'
        )
    else:
        messages.add_message(
            request, messages.ERROR, f'O flashcard "{flashcard.pergunta}" não lhe pertence.'
        )
    
    return redirect(reverse('novo_flashcard'))


@login_required(login_url='login')
def iniciar_desafio(request):

    categorias = Categoria.objects.all()
    dificuldades = Flashcard.DIFICULDADE_CHOICES

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        categorias = request.POST.getlist('categoria')
        dificuldade = request.POST.get('dificuldade')
        qtd_perguntas = request.POST.get('qtd_perguntas')

        desafio = Desafio(
            user=request.user,
            titulo=titulo,
            quantidade_perguntas=qtd_perguntas,
            dificuldade=dificuldade,
        )
        desafio.save()

        desafio.categoria.add(*categorias)

        flashcards = (
            Flashcard.objects.filter(user=request.user)
            .filter(dificuldade=dificuldade)
            .filter(categoria_id__in=categorias)
            .order_by('?')
        )

        if flashcards.count() < int(qtd_perguntas):
            #TODO: Tratar para escolher depois
            messages.add_message(
                request, messages.ERROR, 'Os flashcards não foram incluídos no desafio!'
            )
            return redirect(reverse('iniciar_desafio'))

        flashcards = flashcards[: int(qtd_perguntas)]

        for f in flashcards:
            flashcard_desafio = FlashcardDesafio(
                flashcard=f,
            )
            flashcard_desafio.save()
            desafio.flashcards.add(flashcard_desafio)

        desafio.save()
        messages.add_message(
                request, messages.SUCCESS, 'Desafio cadastrado com sucesso.'
            )
        
        return redirect(reverse('listar_desafio'))
        # return redirect(f'/flashcard/desafio/{desafio.id}')

    else:
        return render(
            request,
            'iniciar_desafio.html',
            {'categorias': categorias, 'dificuldades': dificuldades},
        )


@login_required(login_url='login')
def listar_desafio(request):
    categorias = Categoria.objects.all()
    dificuldades = Flashcard.DIFICULDADE_CHOICES
    lista_status = ['Em aberto', 'Concluído']

    categoria_filtro = request.GET.get('categoria')
    dificuldade_filtro = request.GET.get('dificuldade')
    status_filtro = request.GET.get('status')

    desafios = Desafio.objects.filter(user=request.user)

    if categoria_filtro:
        desafios = desafios.filter(categoria__id=categoria_filtro)
        categoria_filtro = Categoria.objects.get(id=categoria_filtro)
    
    if dificuldade_filtro:
        desafios = desafios.filter(dificuldade=dificuldade_filtro)

    if status_filtro:
        desafios = [x for x in desafios if x.status==status_filtro]

    context = {
        'categorias': categorias,
        'dificuldades': dificuldades,
        'lista_status': lista_status,
        'cat_filtro': categoria_filtro,
        'dif_filtro': dificuldade_filtro,
        'status_filtro': status_filtro,
        'desafios': desafios,
    }

    return render(
        request,
        'listar_desafio.html',
        context
    )


@login_required(login_url='login')
def desafio(request, id):
    desafio = get_object_or_404(Desafio, id=id)

    if not desafio.user == request.user:
        raise Http404()

    acertos = desafio.flashcards.filter(respondido=True).filter(acertou=True).count()
    erros = desafio.flashcards.filter(respondido=True).filter(acertou=False).count()
    faltantes = desafio.flashcards.filter(respondido=False).count()

    if request.method == 'GET':
        return render(
            request,
            'desafio.html',
            {
                'desafio': desafio,
                'acertos': acertos,
                'erros': erros,
                'faltantes': faltantes,
            },
        )


@login_required(login_url='login')
def responder_flashcard(request, id):
    flashcard_desafio = get_object_or_404(FlashcardDesafio, id=id)

    if not flashcard_desafio.flashcard.user == request.user:
        raise Http404()

    acertou = request.GET.get('acertou')
    desafio_id = request.GET.get('desafio_id')

    flashcard_desafio.respondido = True
    flashcard_desafio.acertou = True if acertou == '1' else False
    flashcard_desafio.save()
    return redirect(f'/flashcard/desafio/{desafio_id}/')


@login_required(login_url='login')
def relatorio(request, id):
    desafio = get_object_or_404(Desafio, id=id)

    acertos = desafio.flashcards.filter(acertou=True).count()
    erros = desafio.flashcards.filter(respondido=True).filter(acertou=False).count()
    faltantes = desafio.flashcards.filter(respondido=False).count()

    dados = [acertos, erros, faltantes]

    categorias = desafio.categoria.all()
    name_categorias = [i.nome for i in categorias]

    dados2 = {}
    melhores_materias = {}
    piores_materias = {}

    for categoria in categorias:

        acertos = desafio.flashcards.filter(flashcard__categoria=categoria).filter(acertou=True).count()

        erros = desafio.flashcards.filter(flashcard__categoria=categoria).filter(respondido=True).filter(acertou=False).count()

        faltantes = desafio.flashcards.filter(flashcard__categoria=categoria).filter(respondido=False).count()

        dados2[categoria.nome] = [acertos, erros, faltantes]
        
        if (acertos + erros) > 0:
            if acertos / (acertos + erros) >= 0.5:
                melhores_materias[categoria.nome] = [acertos, erros, faltantes]
            elif acertos / (acertos + erros) < 0.4:
                piores_materias[categoria.nome] = [acertos, erros, faltantes]
    
    context = {
        'desafio': desafio,
        'dados': dados,
        'categorias': name_categorias,
        'dados2': dados2,
        'melhores_materias': melhores_materias,
        'piores_materias': piores_materias,
    }

    return render(request, 'relatorio.html', context)
