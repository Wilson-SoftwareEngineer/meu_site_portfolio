"""
Django settings for core project.
"""
import os
from pathlib import Path
from decouple import config, Csv # Importamos o Csv para ler listas do .env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# CONFIGURAÇÕES DE SEGURANÇA (LENDO DO ARQUIVO .ENV)
# ==============================================================================

# A chave secreta agora vem do arquivo .env. Se não achar, usa uma padrão (apenas para evitar erro local)
SECRET_KEY = config('SECRET_KEY', default='chave-insegura-para-dev-local')

# O Debug agora é controlado pelo .env (True no seu PC, False na Hostinger)
DEBUG = config('DEBUG', default=False, cast=bool)

# Lista de IPs permitidos. No .env separamos por vírgula: "127.0.0.1,SEU_IP_HOSTINGER"
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website', # Seu app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==============================================================================
# INTERNACIONALIZAÇÃO (MUDADO PARA PT-BR)
# ==============================================================================

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Fortaleza' # Fuso horário do Piauí/Nordeste

USE_I18N = True

USE_TZ = True


# ==============================================================================
# ARQUIVOS ESTÁTICOS E MÍDIA
# ==============================================================================

STATIC_URL = 'static/'

# Onde o Django procura estáticos durante o desenvolvimento (seu PC)
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Onde o Django JOGA os estáticos quando rodamos 'collectstatic' (na Hostinger/Produção)
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

# Configuração de Upload de Imagens
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'