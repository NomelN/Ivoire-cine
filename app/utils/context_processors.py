"""
Processeurs de contexte pour les templates
"""
from app.services.tmdb_service import tmdb_service

def register_context_processors(app):
    """Enregistre les processeurs de contexte pour l'application"""

    @app.context_processor
    def inject_genres():
        """Injecte les genres de films dans tous les templates"""
        data, error = tmdb_service.get_genres()

        if data:
            genres = data.get("genres", [])
            genres_dict = {genre['id']: genre['name'] for genre in genres}
            return {"genres": genres, "genres_dict": genres_dict}
        else:
            # En cas d'erreur, retourner des valeurs par défaut
            return {"genres": [], "genres_dict": {}}

    @app.context_processor
    def inject_config():
        """Injecte la configuration dans les templates"""
        from app.config.settings import get_config
        config = get_config()
        return {
            "TMDB_IMAGE_BASE_URL": config.TMDB_IMAGE_BASE_URL
        }