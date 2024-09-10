translations = {
    'en_GB': {
        'posts': 'Posts',
        'log_in': 'Log In',
        'log_out': 'Log Out',
        'new': 'New',
        'edit': 'Edit',
    },
    'es_ES': {
        'posts': 'Entradas',
        'log_in': 'Iniciar sesion',
        'log_out': 'Salir',
        'new': 'Nuevo',
        'edit': 'Editar',
    }
}

def get_translation(locale):
    return translations.get(locale, translations['en_GB'])
