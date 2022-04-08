# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru-RU'
LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Russian'),
)
LOCALE_PATHS = ('movies/locale',)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
