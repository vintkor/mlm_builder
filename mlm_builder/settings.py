try:
    from mlm_builder.prod_settings import *
except:
    import os

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'jjh30x(ay_bc6&am73hv=pottqy2*g@w$-cv+h^@7_0hs$)(**'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = ['*']
    INTERNAL_IPS = '127.0.0.1'

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.humanize',

        'datetimepicker',
        'debug_toolbar',
        'mptt',
        'ckeditor',
        'ckeditor_uploader',
        'sorl.thumbnail',
        'phonenumber_field',
        'widget_tweaks',

        'profile_mlm',
        'webinar',
        'finance',
        'package',
        'landing',
        'dashboard_home',
        'facebook_adds',
        'images',
        'user_email',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django.middleware.locale.LocaleMiddleware',
    ]

    ROOT_URLCONF = 'mlm_builder.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.template.context_processors.i18n',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'mlm_builder.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/2.0/ref/settings/#databases

    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.mysql',
    #         'NAME': 'mlm_builder',
    #         'USER': 'root',
    #         'PASSWORD': '7108471084',
    #         'HOST': '127.0.0.1',
    #         'PORT': '',
    #         'OPTIONS': {
    #             "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
    #         }
    #     }
    # }

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'mlm_builder',
            'USER': 'mlm_builder',
            'PASSWORD': 'mlm_builder',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }


    # Password validation
    # https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

    LOGIN_URL = 'profile:login'

    # Internationalization
    # https://docs.djangoproject.com/en/2.0/topics/i18n/

    LANGUAGE_CODE = 'ru-RU'

    TIME_ZONE = 'Europe/Kiev'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = False

    DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/

    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
    )

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

    CKEDITOR_UPLOAD_PATH = 'uploads/'
    MPTT_ADMIN_LEVEL_INDENT = 20

    CKEDITOR_CONFIGS = {
        'default': {
            # 'skin': 'moono',
            # 'skin': 'office2013',
            'toolbar_Basic': [
                ['Source', '-', 'Bold', 'Italic']
            ],
            'toolbar_YourCustomToolbarConfig': [
                {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
                {'name': 'clipboard',
                 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
                {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
                {'name': 'basicstyles',
                 'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
                {'name': 'paragraph',
                 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv',
                           '-',
                           'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                           'Language']},
                {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
                {'name': 'insert',
                 'items': ['Image', 'Youtube', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak',
                           'Iframe']},
                '/',
                {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
                {'name': 'colors', 'items': ['TextColor', 'BGColor']},
                {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
                {'name': 'about', 'items': ['About']},
                {'name': 'yourcustomtools', 'items': ['Preview', 'Maximize', ]},
            ],
            'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
            # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
            # 'height': 291,
            # 'width': '100%',
            # 'filebrowserWindowHeight': 725,
            # 'filebrowserWindowWidth': 940,
            # 'toolbarCanCollapse': True,
            # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
            'tabSpaces': 4,
            'extraPlugins': ','.join([
                'uploadimage',  # the upload image feature
                # your extra plugins here
                'div',
                'autolink',
                'autoembed',
                'embedsemantic',
                'autogrow',
                # 'devtools',
                'widget',
                'lineutils',
                'clipboard',
                'dialog',
                'dialogui',
                # 'youtube',
                'elementspath'
            ]),
        }
    }

    # ------------------ TEST FACEBOOK ------------------
    FACEBOOK_APP_ID = '872611946244817'
