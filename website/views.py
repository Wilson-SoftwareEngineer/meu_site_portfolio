import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from decouple import config
from openai import OpenAI
from .models import Post, HallOfFameMember

# Configuração do Cliente OpenAI (lendo do .env)
client = OpenAI(api_key=config('OPENAI_API_KEY'))

def index(request):
    posts = Post.objects.all().order_by('-data_criacao')[:3]
    membros = HallOfFameMember.objects.all()
    context = {
        'posts': posts,
        'membros': membros,
    }
    return render(request, 'website/index.html', context)

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'website/post_detail.html', {'post': post})

def engenharia_software(request):
    return render(request, 'website/engenharia_software.html')

# --- NOVA FUNÇÃO DO CHAT ---
def chat_api(request):
    if request.method == 'POST':
        try:
            # 1. Pega a mensagem que veio do Javascript
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # 2. Envia para a OpenAI
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", # Ou "gpt-4o-mini" (mais rápido e barato)
                messages=[
                    {
                        "role": "system", 
                        "content": "Você é o assistente virtual do Piauí Tech Hub. Responda apenas: Olá, Entre em contato com o Eng.Wilson pelo whatsapp da pagina."
                    },
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150 # Limita o tamanho da resposta para não gastar muito
            )

            # 3. Pega a resposta da IA
            ai_response = response.choices[0].message.content
            
            # 4. Devolve para o site
            return JsonResponse({'reply': ai_response})
        
        except Exception as e:
            print(f"Erro na OpenAI: {e}") # Mostra o erro no terminal
            return JsonResponse({'reply': 'Desculpe, estou em manutenção no momento.'}, status=500)

    return JsonResponse({'error': 'Método inválido'}, status=400)