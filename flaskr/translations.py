translations = {
    "en_GB": {
        "Posts": "Posts",
        "Log In": "Log In",
        "Log Out": "Log Out",
        "New": "New",
        "Edit": "Edit"
    },
    "es_ES": {
        "Posts": "Entradas",
        "Log In": "Iniciar sesion",
        "Log Out": "Salir",
        "New": "Nuevo",
        "Edit": "Editar"
    }
}

def get_translation(locale, text):
    return translations.get(locale, translations["en_GB"]).get(text, text)
