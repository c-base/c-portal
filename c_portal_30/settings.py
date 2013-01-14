# Django settings for c_portal_30 project.

import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cportal',
        'USER': 'cportal',
        'PASSWORD': 'cportal!42pw',
        'HOST': 'database.c-base.org',
        'PORT': '3306',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'de-de'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/var/www/cportal30/c_portal_30/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/var/www/cportal30/c_portal_30/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'w6jm=$(v2ks2mpgp+)^h@73w#z3)i2zeo!2xl+w(8#rl2qr&amp;q='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

APPEND_SLASH = True

ROOT_URLCONF = 'c_portal_30.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'c_portal_30.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

AUTH_LDAP_SERVER_URI = "ldap://slurp.c-base.org"
AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=crew,dc=c-base,dc=org"
AUTH_LDAP_START_TLS = False
AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = False

AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 300
AUTH_LDAP_MIRROR_GROUPS = True
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
	"dc=c-base,dc=org",
	ldap.SCOPE_SUBTREE,
	"(objectClass=groupOfNames)",
)
AUTH_LDAP_REQUIRE_GROUP = "cn=crew,ou=groups,dc=c-base,dc=org"
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
	"is_member": "cn=crew,ou=groups,dc=c-base,dc=org",
	"is_circle_member": "cn=circle,ou=groups,dc=c-base,dc=org",
}

AUTHENTICATION_BACKENDS = (
		'django_auth_ldap.backend.LDAPBackend',
		'django.contrib.auth.backends.ModelBackend',
		)

#if DEBUG:
#	import logging, logging.handlers
#	logfile = "/tmp/django-ldap-debug.log"
#	my_logger = logging.getLogger('django_auth_ldap')
#	my_logger.setLevel(logging.DEBUG)
#	handler = logging.handlers.RotatingFileHandler(
#	logfile, maxBytes=1024 * 500, backupCount=5)
#	my_logger.addHandler(handler)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
	'django.contrib.markup',
	'south',
	'jsonrpc',
	'account',
	'c_portal',
	'api',
	'polls',
	'shoutbox',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
