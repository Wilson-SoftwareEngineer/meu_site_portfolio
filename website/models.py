from django.db import models

class Configuracao(models.Model):
    """Permite editar o rodapé e configurações gerais pelo admin"""
    titulo_site = models.CharField(max_length=100, default="Piauí Tech Hub")
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    def save(self, *args, **kwargs):
        self.pk = 1  # Garante que só exista 1 registro de configuração
        super().save(*args, **kwargs)

    def __str__(self):
        return "Configurações Gerais do Site"

class Perfil(models.Model):
    """Torna a seção 'Sobre Mim' editável"""
    nome_completo = models.CharField(max_length=100, default="Wilson Sousa")
    titulo_profissional = models.CharField(max_length=100, default="Engenheiro de Software em formação")
    resumo = models.TextField(help_text="Texto curto introdutório")
    biografia_completa = models.TextField(help_text="Texto longo da seção Sobre Mim")
    foto = models.ImageField(upload_to='perfil/', blank=True)
    linkedin = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        self.pk = 1  # Garante apenas 1 perfil principal
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_completo

class Post(models.Model):
    # Categorias que correspondem exatamente ao seu Menu
    CATEGORIAS = [
        ('ENG', 'Engenharia de Software'),
        ('TUT', 'Tutoriais'),
        ('GUIA', 'Guias Completos'),
        ('TOOL', 'Ferramentas'),
        ('NEWS', 'Atualidades Tech'),
        ('ENG', 'Engenharia Geral'),
        ('DEV', 'Desenvolvimento'),
        ('ARQ', 'Arquitetura de Software'),
        ('AGIL', 'Gestão Ágil'),
        
    ]

    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    imagem = models.ImageField(upload_to='posts/')
    # Alterado para usar choices (menu dropdown no admin)
    categoria = models.CharField(max_length=4, choices=CATEGORIAS, default='NEWS') 
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