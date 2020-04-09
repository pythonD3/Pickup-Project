"""
Django settings for Pickup project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import socket
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o-m$-@tpxj-l6%71_txalhq)4#d4n)0r*^ww99(uk3a&#daf=a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
		'Pickup_App'
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

ROOT_URLCONF = 'Pickup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'Pickup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
    # 'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
# }


DATABASES = {
	'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Pickup_Dev_DB',
				'USER':'root',
				'PASSWORD':'root',
				'HOST':'127.0.0.1',
				'PORT':'3306',
		
	}
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

### Email Settings
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'vycleans@gmail.com'
# EMAIL_HOST_PASSWORD = "iF)=6,]#*?8k'2I"




#######................ Email Settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = socket.gethostbyname('smtp.gmail.com')
# EMAIL_HOST_USER = 'vycleans@gmail.com'
# EMAIL_HOST_PASSWORD = "iF)=6,]#*?8k'2I"
# EMAIL_PORT = 465
# EMAIL_USE_SSL = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = socket.gethostbyname('smtp.gmail.com')
EMAIL_HOST_USER = 'pickupsparenting@gmail.com'
EMAIL_HOST_PASSWORD = "Pickups2020"
EMAIL_PORT = 465
EMAIL_USE_SSL = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

########### Image size ###############
DATA_UPLOAD_MAX_MEMORY_SIZE = 11242880


###############################Android Firebase Server Key#################################
# API_KEY_CUSTOMER = "AAAAq-DpeAI:APA91bH-7K_xk4ivcK6ym1rU3BntBBm7G4G-yCpSBf_w9VUw4sIvF-gjL7CJAy7I508sve9ZgeRthXyuC6a2fZXUaqI9vKkEgkMnZsDDCKrH-tfWz7YjiJesfRvZec7ar26Eqj20mVgR"

API_KEY_NOTIFICATION = "AAAApMZxdO8:APA91bEAFaXyVzW5_W_VH2OvuUVTzHWo5wNcT8arXeLxTFlAWYn4mZwTPdykOKhXrQiyITR5nEsDT0GQyzMIj0T1KM6oMK9xL6MjWi4FnRapd9K6RyhlPl104X3weCSCIkCkHWqYJlsI"