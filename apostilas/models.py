from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag
    

class Apostila(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to='apostilas')
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.titulo


class ViewApostila(models.Model):
    ip = models.GenericIPAddressField()
    apostila = models.ForeignKey(Apostila, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.ip


class Avaliacao(models.Model):
    apostila = models.ForeignKey(Apostila, on_delete=models.CASCADE)
    nota = models.IntegerField()
    comentario = models.TextField()

    def __str__(self):
        return f'{self.apostila} - {self.nota}'
