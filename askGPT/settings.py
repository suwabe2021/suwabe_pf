from pathlib import Path
import json
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#公開したくないものをjsonに入れてあるのでそれを読み込む
try:
    with open("ignore.json") as config_file:
        config_data = json.load(config_file)
except FileNotFoundError:
    raise RuntimeError("ファイルが見つからない: ignore.json")
except json.JSONDecodeError:
    raise RuntimeError("JSON形式の解析中にエラーが発生: ignore.json")

# プライベートIPとドメインのを取得（拡張性のためjsonにそれぞれ複数設定できるようにしている）
PRIVATE_IPS = config_data.get("PRIVATE_IPS", [])
DOMAINS = config_data.get("DOMAINS", [])

#セキュリティキーもjsonで管理
SECRET_KEY = config_data["SECRET_KEY"]

#データベース
DATABASES = config_data.get("DATABASES", [])

#Lineログイン用のチャンネル
SOCIAL_AUTH_LINE_KEY = config_data["SOCIAL_AUTH_LINE_KEY"]
SOCIAL_AUTH_LINE_SECRET = config_data["SOCIAL_AUTH_LINE_SECRET"]

#Lineログインに進めるURLパラメータ(accountで使う)
REDIRECT_KEY = config_data["REDIRECT_KEY"]

#LINEリダイレクトURL ※LINE DevelopersのコールバックURLと一致すること
LINE_REDIRECT_URL = "https://" + DOMAINS[0] + "/portfolio/"

#LINEのACCESSTOKEN
ACCESSTOKEN = config_data["ACCESSTOKEN"]

#chatGPTのAPI_KEY
OPENAI_API_KEY = config_data["OPENAI_API_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = PRIVATE_IPS + DOMAINS + ["localhost", "127.0.0.1"]

#No-IPのサブドメインだとこれ入れないと管理画面でCSRFエラーになる
CSRF_TRUSTED_ORIGINS = [ "https://" + DOMAINS[0] ]

# Application definition

INSTALLED_APPS = [
    'account',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'line_bot',
    'social_django',
    'chatgpt',
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

AUTHENTICATION_BACKENDS = (
    'social_core.backends.line.LineOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'askGPT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'askGPT.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
      "ENGINE":"django.db.backends.postgresql_psycopg2",
      "NAME":DATABASES[0],
      "USER":DATABASES[1],
      "PASSWORD":DATABASES[2],
      "HOST":"localhost",
      "PORT":"5432"
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
AUTH_USER_MODEL = 'account.User'