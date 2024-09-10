translations = {
    'en_GB': {
        'Posts': 'Posts',
        'Log In': 'Log In',
        'Log Out': 'Log Out',
        'Register': 'Register',
        'New': 'New',
        'Edit': 'Edit'
    },
    'es_ES': {
        'Posts': 'Entradas',
        'Log In': 'Iniciar sesion',
        'Log Out': 'Salir',
        'Register': 'Registrarse',
        'New': 'Nuevo',
        'Edit': 'Editar'
    }
}

def translate(text, locale):
    return translations.get(locale, {}).get(text, text)
