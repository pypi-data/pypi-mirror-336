SECRET_KEY = 'django-insecure-bs_wsbkt2&e$-+lver%rhjd6@#13_6t_x1&$x7g9n%^yu*#fbb'

DEBUG = True

INSTALLED_APPS = [
    'django_filtering',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
