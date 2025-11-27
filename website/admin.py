from django.contrib import admin
from .models import Post, HallOfFameMember, Configuracao, Perfil

# Registra os modelos simples
admin.site.register(HallOfFameMember)
admin.site.register(Configuracao)
admin.site.register(Perfil)

# Personaliza a listagem de Posts
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'data_criacao')
    list_filter = ('categoria',) # Cria filtro lateral por categoria
    search_fields = ('titulo', 'conteudo')