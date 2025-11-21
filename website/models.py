from django.db import models

from django.db import models

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    imagem = models.ImageField(upload_to='posts/')
    categoria = models.CharField(max_length=50) # Ex: DevOps, AI
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class HallOfFameMember(models.Model):
    nome = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100) # Ex: Pai da Computação
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='hall_of_fama/')
    
    def __str__(self):
        return self.nome
# Create your models here.
