from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from website.views import index, post_detail, engenharia_software, chat_api, listar_posts_por_categoria

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    
    # Rotas de Conteúdo
    path('post/<int:id>/', post_detail, name='post_detail'),
    path('engenharia-software/', engenharia_software, name='engenharia_software'),
    
    # Rota Mágica do Menu (Filtra Tutoriais, Guias, etc)
    path('categoria/<str:categoria_slug>/', listar_posts_por_categoria, name='posts_por_categoria'),
    
    # API
    path('api/chat/', chat_api, name='chat_api'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)