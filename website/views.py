import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decouple import config
from openai import OpenAI
from .models import Post, HallOfFameMember

# Configuração do Cliente OpenAI
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

# --- CHATBOT INTELIGENTE ---
@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # Chama a OpenAI com limite de tokens
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "Você é o assistente inteligente do Wilson. Responda dúvidas sobre Engenharia de Software, Python, Django e Tecnologia de forma didática. Se a pergunta for muito complexa ou fora do tema, sugira contato com o Eng. Wilson pelo LinkedIn."
                    },
                    {"role": "user", "content": user_message}
                ],
                max_tokens=300, # Limita a resposta para economizar (aprox. 2 parágrafos)
                temperature=0.7
            )

            ai_response = response.choices[0].message.content
            return JsonResponse({'reply': ai_response})
        
        except Exception as e:
            print(f"Erro OpenAI: {e}")
            return JsonResponse({'reply': 'Minha conexão neural falhou. Tente novamente mais tarde.'}, status=500)

    return JsonResponse({'error': 'Método inválido'}, status=400)