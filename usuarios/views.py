from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if len(username.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(
                request, messages.ERROR, 'Preencha todos os campos!'
            )
            return redirect(reverse('cadastro'))
        
        if not senha == confirmar_senha:
            messages.add_message(
                request, messages.ERROR, 'As senhas não coincídem'
            )
            return redirect(reverse('cadastro'))

        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(
                request,
                messages.ERROR,
                'Já existe um usuário com o mesmo username',
            )
            return redirect(reverse('cadastro'))

        try:
            user = User.objects.create_user(
                username=username,
                password=confirmar_senha,
            )
            messages.add_message(
                request, messages.SUCCESS, 'Usuário cadastrado com sucesso.'
            )

            return redirect(reverse('login'))
        
        except:
            messages.add_message(
                request, messages.ERROR, 'Erro interno do sistema'
            )
            return redirect(reverse('cadastro'))

    else:
        return render(request, 'cadastro.html')


def logar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        if len(username.strip()) == 0 or len(senha.strip()) == 0:
            messages.add_message(
                request, messages.ERROR, 'Preencha todos os campos!'
            )
            return redirect(reverse('login'))

        user = authenticate(request, username=username, password=senha)
        if user:
            login(request, user)
            return redirect(reverse('novo_flashcard'))
        else:
            messages.add_message(
                request, messages.ERROR, 'Username ou senha inválidos'
            )
            return redirect(reverse('login'))

    else:
        return render(request, 'login.html')


def sair(request):
    logout(request)
    return redirect(reverse('login'))
