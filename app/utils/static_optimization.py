"""
Optimisation des ressources statiques
"""
from flask import Flask
import gzip
import os
from pathlib import Path


def configure_static_optimization(app: Flask):
    """Configure l'optimisation des ressources statiques"""

    @app.after_request
    def add_cache_headers(response):
        """Ajoute les en-têtes de cache pour les ressources statiques"""
        if (response.content_type and
            (response.content_type.startswith('text/css') or
             response.content_type.startswith('application/javascript') or
             response.content_type.startswith('image/'))):

            # Cache pour 1 jour pour le CSS/JS, 1 semaine pour les images
            if response.content_type.startswith('image/'):
                response.cache_control.max_age = 604800  # 1 semaine
            else:
                response.cache_control.max_age = 86400   # 1 jour

            response.cache_control.public = True

        return response

    @app.after_request
    def compress_response(response):
        """Compresse les réponses si possible"""
        # Ne pas compresser les fichiers statiques gérés par Flask
        if request.endpoint == 'static':
            return response

        # Vérifier si la compression est supportée par le client
        accept_encoding = request.headers.get('Accept-Encoding', '')

        if ('gzip' in accept_encoding and
            response.status_code == 200 and
            response.content_type and
            (response.content_type.startswith('text/') or
             response.content_type.startswith('application/json') or
             response.content_type.startswith('application/javascript'))):

            # Vérifier si la réponse a des données à compresser
            try:
                response_data = response.get_data()
                # Compresser seulement les réponses > 1KB
                if len(response_data) > 1024:
                    compressed = gzip.compress(response_data)

                    # Seulement si la compression est bénéfique
                    if len(compressed) < len(response_data) * 0.9:
                        response.set_data(compressed)
                        response.headers['Content-Encoding'] = 'gzip'
                        response.headers['Content-Length'] = len(compressed)
            except (RuntimeError, AttributeError):
                # Ignorer les erreurs de compression pour les réponses en mode passthrough
                pass

        return response


def minify_css(css_content: str) -> str:
    """Minification basique du CSS"""
    import re

    # Supprimer les commentaires CSS
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)

    # Supprimer les espaces multiples et les sauts de ligne
    css_content = re.sub(r'\s+', ' ', css_content)

    # Supprimer les espaces autour des caractères spéciaux
    css_content = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', css_content)

    # Supprimer les points-virgules avant les accolades fermantes
    css_content = re.sub(r';}', '}', css_content)

    return css_content.strip()


def minify_js(js_content: str) -> str:
    """Minification basique du JavaScript"""
    import re

    # Supprimer les commentaires de ligne
    js_content = re.sub(r'//.*?$', '', js_content, flags=re.MULTILINE)

    # Supprimer les commentaires de bloc
    js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)

    # Supprimer les espaces multiples et normaliser les sauts de ligne
    js_content = re.sub(r'\s+', ' ', js_content)

    # Supprimer les espaces autour des opérateurs
    js_content = re.sub(r'\s*([{}()[\];,=+\-*/])\s*', r'\1', js_content)

    return js_content.strip()


def create_optimized_static_files(app: Flask):
    """Crée des versions optimisées des fichiers statiques"""
    static_folder = Path(app.static_folder)

    # Optimiser les fichiers CSS
    css_files = static_folder.rglob('*.css')
    for css_file in css_files:
        if not css_file.name.endswith('.min.css'):
            content = css_file.read_text(encoding='utf-8')
            minified = minify_css(content)

            # Créer le fichier minifié
            min_file = css_file.with_suffix('.min.css')
            min_file.write_text(minified, encoding='utf-8')

            print(f"CSS minifié: {css_file.name} -> {min_file.name}")

    # Optimiser les fichiers JavaScript
    js_files = static_folder.rglob('*.js')
    for js_file in js_files:
        if not js_file.name.endswith('.min.js'):
            content = js_file.read_text(encoding='utf-8')
            minified = minify_js(content)

            # Créer le fichier minifié
            min_file = js_file.with_suffix('.min.js')
            min_file.write_text(minified, encoding='utf-8')

            print(f"JS minifié: {js_file.name} -> {min_file.name}")


# Import de request pour la fonction compress_response
from flask import request