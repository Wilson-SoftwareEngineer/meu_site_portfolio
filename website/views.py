import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decouple import config
from openai import OpenAI
from .models import Post, HallOfFameMember, Perfil, Configuracao

# --- Configuração OpenAI ---
try:
    client = OpenAI(api_key=config('OPENAI_API_KEY'))
except:
    client = None

# --- Helper para dados comuns (Header/Footer) ---
def get_common_context():
    config_site, _ = Configuracao.objects.get_or_create(pk=1)
    return {'config': config_site}

# --- Views do Site ---
def index(request):
    context = get_common_context()
    
    # Busca dados dinâmicos
    perfil, _ = Perfil.objects.get_or_create(pk=1)
    posts = Post.objects.all().order_by('-data_criacao')[:6] # Mostra os 6 últimos
    membros = HallOfFameMember.objects.all()
    
    context.update({
        'posts': posts, 
        'membros': membros,
        'perfil': perfil
    })
    return render(request, 'website/index.html', context)

def listar_posts_por_categoria(request, categoria_slug):
    """Filtra posts quando clica no Menu (Tutoriais, Guias, etc)"""
    context = get_common_context()
    
    posts = Post.objects.filter(categoria=categoria_slug).order_by('-data_criacao')
    nome_categoria = dict(Post.CATEGORIAS).get(categoria_slug, "Publicações")
    
    context.update({
        'posts': posts,
        'titulo_pagina': nome_categoria
    })
    return render(request, 'website/lista_posts.html', context)

def post_detail(request, id):
    context = get_common_context()
    post = get_object_or_404(Post, id=id)
    context['post'] = post
    return render(request, 'website/post_detail.html', context)

# ... (imports anteriores mantidos)

def engenharia_software(request):
    context = get_common_context()
    
    # Define quais categorias pertencem ao grupo "Engenharia de Software"
    categorias_eng = ['ENG', 'DEV', 'ARQ', 'AGIL']
    
    # Filtra posts onde a categoria esteja DENTRO dessa lista (__in)
    posts = Post.objects.filter(categoria__in=categorias_eng).order_by('-data_criacao')
    
    context.update({
        'posts': posts
    })
    
    return render(request, 'website/engenharia_software.html', context)

# ... (restante do arquivo continua igual)

# --- CHATBOT INTELIGENTE ---
@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            if not client:
                return JsonResponse({'reply': 'Erro: Chave de API não configurada no servidor.'})

            data = json.loads(request.body)
            user_message = data.get('message', '')

            response = client.chat.completions.create(
                # O 'mini' é muito inteligente e extremamente barato
                model="gpt-4o-mini", 
                
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "Você é o assistente técnico do Piauí Tech Hub. "
                            "Suas respostas devem ser diretas, assertivas e tecnicamente profundas. "
                            "Vá direto ao ponto e priorize a solução técnica."
                        )
                    },
                    {"role": "user", "content": user_message}
                ],
                max_tokens=700, # Pode manter alto, o mini é barato
                temperature=0.3
            )

            ai_response = response.choices[0].message.content
            return JsonResponse({'reply': ai_response})
        
        except Exception as e:
            print(f"ERRO OPENAI: {e}")
            return JsonResponse({'reply': 'Estou com dificuldade de conexão com a IA no momento.'}, status=500)

    return JsonResponse({'error': 'Método inválido'}, status=400)