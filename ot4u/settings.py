"""
Django settings for ot4u project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import environ
import os
import dj_database_url
import mimetypes

from pathlib import Path
from django.conf.global_settings import DEFAULT_FILE_STORAGE
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialise environment variables
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# False if not in os.environ because of casting above
DEBUG = env("DEBUG")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# Make sure Django sees CSS files as CSS
mimetypes.add_type("text/css", ".css", True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "")

ALLOWED_HOSTS = ["ot4u-ci.herokuapp.com", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cloudinary_storage",
    "cloudinary",
    "home",
    "therapy",
    #  used by the social account app to create the proper callback URLs
    #  when connecting via social media accounts
    "django.contrib.sites",
    "allauth",
    #  allauth app that allows all the basic user account stuff
    #  like logging in and out, User registration and password resets
    "allauth.account",
    #  handles logging in via social media providers like Facebook and Google
    "allauth.socialaccount",
    # Booking Therapy sessions
    "bookings",
    # Purchasing the booked therapy sessions
    "purchase",
    # Set user profile
    "profiles",
    "maintenance",
    "testimonials",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ot4u.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "templates", "allauth"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                # if we want to access request.user or request.user.email
                # in our django templates.
                # We'll be able to do it with this context processor.
                # required by allauth
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Without this the media URL template tag doesn't work
                "django.template.context_processors.media",
                # Anytime we need to access the bookings contents
                # in any template across the entire site they'll be available to us
                # without having to return them from
                # a whole bunch of different views across different apps
                "bookings.contexts.booking_contents",
            ],
        },
    },
]

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": env("CLOUDINARY_NAME"),
    "API_KEY": env("CLOUDINARY_API_KEY"),
    "API_SECRET": env("CLOUDINARY_API_SECRET"),
}

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

WSGI_APPLICATION = "ot4u.wsgi.application"

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    # Handles superusers logging into the Admin which allauth doesn't handle
    # Defer to the default django Code for this
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    # Allow users to log into our site via their email
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

# Account authentication method is what tells allauth that we want to allow
# authentication using either usernames or emails.
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# ACCOUNT_AUTHENTICATION_METHOD = "username"

# These three email settings
# make it so that an email is required to register for the site.
ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_REQUIRED = False
# Verifying your email is mandatory so we know users are using a real email.
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# ACCOUNT_EMAIL_VERIFICATION = "none"
# Required to enter their email twice on the registration page
# to make sure that they haven't made any typos
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
# ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = False
# setting a minimum username length of four characters
ACCOUNT_USERNAME_MIN_LENGTH = 4
# specifying a login url and a url to redirect back to after logging in
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"

if "DEVELOPMENT" in os.environ:
    # By default allauth will send confirmation emails to any new accounts.
    # We need to temporarily log those emails to the console
    # so we can get the confirmation links.
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "ot4u@ot4u.com"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    DEFAULT_FROM_EMAIL = env("EMAIL_HOST_USER")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = "/static/"
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# Below line might interfere with setting up AWS
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
if "DATABASE_URL" in os.environ:
    DATABASES = {"default": dj_database_url.parse(env("DATABASE_URL"))}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Stripe
STRIPE_CURRENCY = "eur"
STRIPE_PUBLIC_KEY = env("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")


STRIPE_WH_SECRET = env("STRIPE_WH_SECRET")

# https://ordinarycoders.com/blog/article/django-messages-framework
MESSAGE_TAGS = {
    messages.DEBUG: "yellowBackground",
    messages.INFO: "blueBackground",
    messages.SUCCESS: "greenBackground",
    messages.WARNING: "orangeBackground",
    messages.ERROR: "redBackground",
}
