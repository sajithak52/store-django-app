from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',

        'NAME': 'postgres',
        # 'NAME': 'postgresql',

        'USER': 'postgres',

        'PASSWORD': 'rahq1w2',

        'HOST': 'localhost',

        'PORT': '5432',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'rv4971254@gmail.com'
# EMAIL_HOST_PASSWORD = '9656582215'
EMAIL_HOST_USER = 'mission242022@gmail.com'
EMAIL_HOST_PASSWORD = 'tuhzllskvtlavuyv'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


