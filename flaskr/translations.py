supported_locales = {
    'en': {
        'Posts': 'Posts',
        'New': 'New',
        'by': 'by',
        'on': 'on',
        'Edit': 'Edit'
    },
    'es': {
        'Posts': 'Publicaciones',
        'New': 'Nuevo',
        'by': 'por',
        'on': 'en',
        'Edit': 'Editar'
    }
}

def get_translations(locale):
    return supported_locales.get(locale, supported_locales['en'])
