from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from flashcard.models import Categoria, Flashcard


def novo_flashcard(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    
    categorias = Categoria.objects.all()
    dificuldades = Flashcard.DIFICULDADE_CHOICES
    flashcards = Flashcard.objects.filter(user=request.user)

    context = {
        'categorias': categorias,
        'dificuldades': dificuldades,
        'flashcards': flashcards,
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

        flashcard.save()

        messages.add_message(
            request, messages.SUCCESS, 'Flashcard criado com sucesso'
        )
        return redirect(reverse('novo_flashcard'))
        
    else:

        categoria_filtro = request.GET.get('categoria')
        dificuldade_filtro = request.GET.get('dificuldade')

        if categoria_filtro:
            flashcards = flashcards.filter(categoria__id=categoria_filtro)

        if dificuldade_filtro:
            flashcards = flashcards.filter(dificuldade=dificuldade_filtro)

        context = {
            'categorias': categorias,
            'dificuldades': dificuldades,
            'flashcards': flashcards,
            'filtro_cat': categoria_filtro,
        }
        return render(request, 'novo_flashcard.html', context)
