import os
import dj_database_url
from django.test.runner import DiscoverRunner


MAX_CONN_AGE = 600

def settings(config, *, db_colors=False, databases=True, test_runner=True, staticfiles=True, allowed_hosts=True, logging=True, secret_key=True):

    # Database configuration.
    if databases:
        database_settings(config,db_colors)

    if test_runner and 'CI' in os.environ:
        # Enable test runner if found in CI environment.
        config['TEST_RUNNER'] = 'django_heroku.HerokuDiscoverRunner'

    # Staticfiles configuration.
    if staticfiles:
        static_settings(config)

    if allowed_hosts:
        config['ALLOWED_HOSTS'] = ['*']
    # SECRET_KEY configuration.
    if secret_key and 'SECRET_KEY' in os.environ:
        # Set the Django setting from the environment variable.
        config['SECRET_KEY'] = os.environ['SECRET_KEY']

def database_settings(config, db_colors):
    # Integrity check.
    if 'DATABASES' not in config:
        config['DATABASES'] = {'default': None}

    conn_max_age = config.get('CONN_MAX_AGE', MAX_CONN_AGE)
        
    if db_colors:
        # Support all Heroku databases.
        for (env, url) in os.environ.items():
            if env.startswith('HEROKU_POSTGRESQL'):
                db_color = env[len('HEROKU_POSTGRESQL_'):].split('_')[0]
                config['DATABASES'][db_color] = dj_database_url.parse(url, conn_max_age=conn_max_age, ssl_require=True)

    if 'DATABASE_URL' in os.environ:
        # Configure Django for DATABASE_URL environment variable.
        config['DATABASES']['default'] = dj_database_url.config(conn_max_age=conn_max_age, ssl_require=True)

        # Enable test database if found in CI environment.
        if 'CI' in os.environ:
            config['DATABASES']['default']['TEST'] = config['DATABASES']['default']

def static_settings(config):
    config['STATIC_ROOT'] = os.path.join(config['BASE_DIR'], 'staticfiles')
    config['STATIC_URL'] = '/static/'

    # Ensure STATIC_ROOT exists.
    os.makedirs(config['STATIC_ROOT'], exist_ok=True)

    # Insert Whitenoise Middleware.
    try:
        config['MIDDLEWARE_CLASSES'] = tuple(['whitenoise.middleware.WhiteNoiseMiddleware'] + list(config['MIDDLEWARE_CLASSES']))
    except KeyError:
        config['MIDDLEWARE'] = tuple(['whitenoise.middleware.WhiteNoiseMiddleware'] + list(config['MIDDLEWARE']))

    # Enable GZip.
    config['STATICFILES_STORAGE'] = 'whitenoise.storage.CompressedManifestStaticFilesStorage'