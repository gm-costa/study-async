from django.contrib import admin
from .models import Categoria, Flashcard, Desafio, FlashcardDesafio


class FlashcardAdmin(admin.ModelAdmin):
    list_display = ['user', 'pergunta', 'resposta', 'categoria', 'dificuldade']


class DesafioAdmin(admin.ModelAdmin):
    list_display = ['user', 'titulo', 'quantidade_perguntas', 'dificuldade', 'categorias', 'flashs']

    def categorias(self, obj):
        return [cat.nome for cat in obj.categoria.all()]
    
    def flashs(self, obj):
        return [flash.flashcard for flash in obj.flashcards.all()]


class FlashcardDesafioAdmin(admin.ModelAdmin):
    list_display = ['flashcard', 'respondido', 'acertou']

admin.site.register(Categoria)
admin.site.register(Flashcard, FlashcardAdmin)
admin.site.register(Desafio, DesafioAdmin)
admin.site.register(FlashcardDesafio, FlashcardDesafioAdmin)
