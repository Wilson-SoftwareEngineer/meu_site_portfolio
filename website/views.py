import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decouple import config
from openai import OpenAI
from .models import Post, HallOfFameMember

# Configuração do Cliente OpenAI (lendo do .env)
try:
    client = OpenAI(api_key=config('OPENAI_API_KEY'))
except:
    client = None

def index(request):
    posts = Post.objects.all().order_by('-data_criacao')[:4]
    membros = HallOfFameMember.objects.all()
    context = {'posts': posts, 'membros': membros}
    return render(request, 'website/index.html', context)

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'website/post_detail.html', {'post': post})

def engenharia_software(request):
    return render(request, 'website/engenharia_software.html')

# --- CHATBOT INTELIGENTE ---
@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            # Verifica se a chave da API existe
            if not client:
                return JsonResponse({'reply': 'Erro: Chave de API não configurada no servidor.'})

            data = json.loads(request.body)
            user_message = data.get('message', '')

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "Você é o assistente inteligente do Piauí Tech Hub. Responda de forma curta e técnica."
                    },
                    {"role": "user", "content": user_message}
                ],
                max_tokens=250,
                temperature=0.7
            )

            ai_response = response.choices[0].message.content
            return JsonResponse({'reply': ai_response})
        
        except Exception as e:
            # Se der erro (ex: falta de créditos), mostramos no console da VPS
            print(f"ERRO OPENAI: {e}")
            return JsonResponse({'reply': 'Estou com dificuldade de conexão com a IA no momento. Tente mais tarde.'}, status=500)

    return JsonResponse({'error': 'Método inválido'}, status=400)