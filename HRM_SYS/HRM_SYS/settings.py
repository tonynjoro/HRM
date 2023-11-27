"""
Django settings for HRM_SYS project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+bo43m_vcns%1t_9u(n3f$8!t+0^b=99s7&ppvi(tyxw@53@=&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

X_FRAME_OPTIONS = 'SAMEORIGIN'

# Application definition
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True

USE_L10N = False


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin_interface', 
      'colorfield',
      'tinymce',
    'crispy_forms',
    'crispy_bootstrap5',
    'searchableselect',
   
    'management.apps.ManagementConfig',
    'payroll.apps.PayrollConfig',
    'hrm_users.apps.HrmUsersConfig',
    'storages',
    'mathfilters',
    'user_visit',
 



]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'HRM_SYS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'HRM_SYS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''


DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'railway',
       'USER': 'postgres',
       'PASSWORD': 'gAB2d4eeGEabd15-c333FbF3fGEd6CGf',
       'HOST': 'roundhouse.proxy.rlwy.net',
       'PORT': '32398',
   }
}




# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATIC_ROOT =  os.path.join(BASE_DIR,'management/static')

STATIC_URL = 'static/'

#STATICFILES_STORAGE = "storages.backends.dropbox.DropboxStorage"



MEDIA_ROOT = os.path.join(BASE_DIR,'media')

MEDIA_URL = 'media/'

'''
    django.core.files.storage.FileSystemStorage
    storages.backends.dropbox.DropBoxStorage

'''

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
    "mediafiles": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}


LOGIN_REDIRECT_URL = 'management-home'
LOGIN_URL = 'login'

CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET","POST"]
CORS_ALLOW_HEADERS = [ "accept", "accept-encoding", "authorization", "content-type", "dnt", "origin", "user-agent", "x-csrftoken", "x-requested-with" ]

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

CSRF_TRUSTED_ORIGINS = ['https://hrm-production-02c6.up.railway.app','https://*.127.0.0.1']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'admin@koshtech.site'
EMAIL_HOST_PASSWORD = 'suid wqby mzyx vcjp'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# dropbox configurations 

DROPBOX_ACCESS_TOKEN = 'sl.Bn8fV-EMhs68duxFUZIcCObLQE-jcQ21vHT97HzzqolDtIC80dLBuJ_7TQClmxx6_SPcroegfHwwDjbMeNxXjvYipT41IHj9HvMYEu8mZhmUuIh6f0oqfn7v6ftPLnSJHtczMZ6kd7x3NQ8eJUBPCuI'

DROPBOX_APP_KEY = '878rh9tt2lqnbwc'

DROPBOX_APP_SECRET = 'p1z60sqyjy1gpjx'

DROPBOX_OAUTH2_REFRESH_TOKEN = 'OB6GXurPyhcAAAAAAAAAAWbYbxfp9e1izkfBVFr3UQiyGclINpl71M0fVfwO0vf5'


TINYMCE_DEFAULT_CONFIG = {
    "entity_encoding": "raw",
    "menubar": "file edit view insert format tools table help",
    "plugins": 'print preview paste importcss searchreplace autolink autosave save code visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists wordcount imagetools textpattern noneditable help charmap emoticons quickbars',
    "toolbar": "fullscreen preview | undo redo | bold italic forecolor backcolor | formatselect | image link | "
    "alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | fontsizeselect "
    "emoticons | ",
    "custom_undo_redo_levels": 50,
    "quickbars_insert_toolbar": False,
    "file_picker_callback": """function (cb, value, meta) {
        var input = document.createElement("input");
        input.setAttribute("type", "file");
        if (meta.filetype == "image") {
            input.setAttribute("accept", "image/*");
        }
        if (meta.filetype == "media") {
            input.setAttribute("accept", "video/*");
        }

        input.onchange = function () {
            var file = this.files[0];
            var reader = new FileReader();
            reader.onload = function () {
                var id = "blobid" + (new Date()).getTime();
                var blobCache = tinymce.activeEditor.editorUpload.blobCache;
                var base64 = reader.result.split(",")[1];
                var blobInfo = blobCache.create(id, file, base64);
                blobCache.add(blobInfo);
                cb(blobInfo.blobUri(), { title: file.name });
            };
            reader.readAsDataURL(file);
        };
        input.click();
    }""",
    "content_style": "body { font-family:Roboto,Helvetica,Arial,sans-serif; font-size:14px }",
}
