import os
import excavator as env
import dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv.load_dotenv(os.path.join(BASE_DIR, '.env'))  # Local overrides (not tracked)
dotenv.load_dotenv(os.path.join(BASE_DIR, '.env_defaults'))  # Development defaults (tracked)

SECRET_KEY = env.get('DJANGO_SECRET_KEY', required=True)

DEBUG = env.get('DJANGO_DEBUG', type=bool, default=False)
DEBUG_ETH_USER_INIT_BALANCE = env.get('DEBUG_ETH_USER_INIT_BALANCE', type=float, default=10.0)

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # 3rd party
    'corsheaders',
    'authtools',
    'rest_framework',
    'argonauts',
    'storages',
    's3_folder_storage',
    'django_tables2',
    'materializecssform',
    'constance',
    'constance.backends.database',
    # Project
    'dynamis.core',
    'dynamis.apps.accounts.apps.AccountsConfig',
    'dynamis.apps.policy',
    'dynamis.apps.payments'
]

if env.get('DJANGO_DEBUG_TOOLBAR_ENABLED', type=bool, default=True):
    # Django Debug Toolbar
    # Provides useful tools for debugging sites either in development or
    # production.
    try:
        import debug_toolbar  # NOQA

        INSTALLED_APPS.append('debug_toolbar')
    except ImportError:
        pass

if DEBUG:
    MIDDLEWARE_CLASSES = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'dynamis.middleware.DisableCSRFMiddleWare',
        'dynamis.middleware.ReplaceResponseCodesMiddleWare',
    ]

    CSRF_COOKIE_SECURE = True

else:
    MIDDLEWARE_CLASSES = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

EMAIL_BACKEND = env.get('DJANGO_EMAIL_BACKEND', required=True)
EMAIL_HOST = env.get('DJANGO_EMAIL_HOST', type=str, default='localhost')
EMAIL_HOST_USER = env.get('DJANGO_EMAIL_HOST_USER', type=str, default='')
EMAIL_HOST_PASSWORD = env.get('DJANGO_EMAIL_HOST_PASSWORD', type=str, default='')
EMAIL_PORT = env.get('DJANGO_EMAIL_PORT', type=int, default=25)
EMAIL_USE_TLS = env.get('DJANGO_EMAIL_USE_TLS', type=bool, default=True)
EMAIL_USE_SSL = env.get('DJANGO_EMAIL_USE_SSL', type=bool, default=False)

DEFAULT_FROM_EMAIL = env.get(
    'DJANGO_DEFAULT_FROM_EMAIL',
    type=str,
    default='no-reply@quickleft.com',  # FIXME transactional email address?
)

ROOT_URLCONF = 'dynamis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'dynamis', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dynamis.core.context_processors.api_urls',
                'constance.context_processors.config',
            ],
        },
    },
]

WSGI_APPLICATION = 'dynamis.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DJANGO_DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DJANGO_DATABASE_NAME', 'dynamisappdb'),
        'USER': os.environ.get('DJANGO_DATABASE_USER', ''),
        'PASSWORD': os.environ.get('DJANGO_DATABASE_PASSWORD', ''),
        'HOST': os.environ.get('DJANGO_DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DJANGO_DATABASE_PORT', ''),
    }
}

DATABASES['default']['ATOMIC_REQUESTS'] = env.get(
    'DJANGO_ATOMIC_REQUESTS',
    type=bool,
    default=True,
)

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

# for dev, these are commented out. probably want them later
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = env.get('DJANGO_SITE_ID', type=int, default=1)

DEFAULT_S3_PATH = "media"
STATIC_S3_PATH = "static"

AWS_ACCESS_KEY_ID = env.get('AWS_ACCESS_KEY_ID', type=str, default=None)
AWS_SECRET_ACCESS_KEY = env.get('AWS_SECRET_ACCESS_KEY', type=str, default=None)
AWS_STORAGE_BUCKET_NAME = env.get('AWS_STORAGE_BUCKET_NAME', type=str, default=None)
AWS_DEFAULT_REGION = env.get('AWS_DEFAULT_REGION', type=str, default=None)

AWS_REDUCED_REDUNDANCY = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = True
AWS_S3_SECURE_URLS = True
AWS_IS_GZIPPED = False
AWS_PRELOAD_METADATA = True
AWS_HEADERS = {
    "Cache-Control": "public, max-age=86400",
}

if AWS_DEFAULT_REGION:
    # Fix for https://github.com/boto/boto/issues/621
    AWS_S3_HOST = "s3-{0}.amazonaws.com".format(AWS_DEFAULT_REGION)

DEFAULT_FILE_STORAGE = env.get(
    'DJANGO_DEFAULT_FILE_STORAGE',
    type=str,
    default='django.core.files.storage.FileSystemStorage',
)

MEDIA_ROOT = env.get(
    'DJANGO_MEDIA_ROOT',
    type=str,
    default=os.path.join(BASE_DIR, 'public', 'media'),
)
MEDIA_URL = env.get(
    'DJANGO_MEDIA_URL',
    type=str,
    default='/media/',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'public', 'compiled'),
    os.path.join(BASE_DIR, 'tests', 'javascript'),
    os.path.join(BASE_DIR, 'dynamis', 'static'),
)

STATIC_ROOT = env.get(
    'DJANGO_STATIC_ROOT',
    type=str,
    default=os.path.join(BASE_DIR, 'public', 'static'),
)

STATIC_URL = env.get(
    'DJANGO_STATIC_URL',
    type=str,
    default='/static/',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = env.get(
    'DJANGO_STATICFILES_STORAGE',
    type=str,
    default='django.contrib.staticfiles.storage.StaticFilesStorage',
)

AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
}

PUBLIC_KEY_PROVIDER_PATH = env.get(
    'PUBLIC_KEY_PROVIDER_PATH',
    default='dynamis.apps.identity.providers.keybase.KeybasePublicKeyProvider',
)

# TODO: this needs to be unique across all installs of the site.  Any two sites
# which have the same SITE_DOMAIN will allow signatures from one site to be
# reused on the other.
SITE_DOMAIN = env.get("DJANGO_SITE_DOMAIN", required=True)

IPFS_HOST = env.get('IPFS_HOST', default=None)
IPFS_PORT = env.get('IPFS_PORT', type=int, default=443)
IPFS_SSL_VERIFY = env.get('IPFS_SSL_VERIFY', type=bool, default=True)

IPFS_AUTH_USERNAME = env.get('IPFS_AUTH_USERNAME')
IPFS_AUTH_PASSWORD = env.get('IPFS_AUTH_PASSWORD', required=IPFS_AUTH_USERNAME)

if DEBUG:
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_HEADERS = [

        # default
        'x-requested-with',
        'content-type',
        'accept',
        'origin',
        'authorization',
        'x-csrftoken',
        'user-agent',
        'accept-encoding',

        # custom
        'x-prototype-version',
        'allow',
        'access-control-allow-headers'
    ]
    CORS_EXPOSE_HEADERS = ['accept', 'content-type', 'set-cookie', 'cookie']
    CORS_ORIGIN_WHITELIST = env.get('CORS_ORIGIN_WHITELIST', type=tuple, default=tuple())

CONSTANCE_CONFIG = {
    'IDENTITY_RECORDS_RATIO': (3, 'Witch rate of peer reviews we need to move policy to active status'),
    'RISK_ASSESSORS_PER_POLICY_COUNT': (5, 'How many risk assessors we need to move policy to status '
                                           'on_completeness_check'),
    'PREMIUM_PAYMENT_PERIODICITY': ('monthly', 'How often users have to pay premium payment'),
    'EHT_TOKEN_EXCHANGE_RATE': (0.1, 'How many eth we have to spend to by 1 token'),
    'DOLLAR_ETH_EXCHANGE_RATE': (12.57, 'How many dollars we have to spend to by 1 Ethereum'),
    'DOLLAR_ETH_EXCHANGE_RATE_VALID_FOR_MINUTES': (60, 'How many minutes dollar/eth rate will valid'),
    'WAIT_FOR_RECEIVE_SMART_DEPOSIT_MINUTES': (60, 'How many minutes we can wait for smart deposit'),
    'ADDRESS_TO_SEND_ETH': ('0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8_test', 'address to send eth'),
    'BET_MIN_AMOUNT_USER': (1, 'RiskAssessor allowed to use minimum 1 token on ClaimStart and 1 token on ClaimLength.'),
    'BET_MAX_AMOUNT_USER': (2, 'RiskAssessor allowed to use maximum 2 tokens on ClaimStart and 2 tokens on '
                               'ClaimLength.'),
    'BET_MIN_AMOUNT_ADMIN': (1, 'Admin is allowed to use minimum 1 token on ClaimStart and 1 token on ClaimLength.'),
    'BET_MAX_AMOUNT_ADMIN': (4, 'Admin is allowed to use maximum 4 tokens on ClaimStart and 4 tokens on ClaimLength.'),
    'MONTHS_PAY_PREMIUMS_BEFORE_OPENING_A_CLAIM_MIN': (6, 'How many months of premiums will this policyholder pay'
                                                          ' before opening a claim?'),
    'MONTHS_PAY_PREMIUMS_BEFORE_OPENING_A_CLAIM_MAX': (36, 'How many months of premiums will this policyholder pay'
                                                           ' before opening a claim?'),
    'WEEKS_PAID_FOR_FIRST_CLAIM_MIN': (0, 'How many weeks will be paid out to this'
                                          ' policyholder for their first claim?'),
    'WEEKS_PAID_FOR_FIRST_CLAIM_MAX': (88, 'How many weeks will be paid out to this'
                                           ' policyholder for their first claim?'),
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
