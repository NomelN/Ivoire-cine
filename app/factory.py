"""
Factory pour créer l'application Flask
"""
import logging
from flask import Flask
from app.config.settings import get_config
from app.routes.movies import movies_bp
from app.utils.errors import register_error_handlers, setup_logging
from app.utils.context_processors import register_context_processors
from app.utils.static_optimization import configure_static_optimization

# SÉCURITÉ: Configurer les logs dès l'import pour éviter l'exposition de clés API
logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('requests.packages.urllib3').setLevel(logging.WARNING)

def create_app(config_name=None):
    """
    Factory pour créer l'application Flask

    Args:
        config_name: Nom de la configuration à utiliser

    Returns:
        Application Flask configurée
    """
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')

    # Charger la configuration
    config = get_config(config_name)
    app.config.from_object(config)

    # Valider la configuration
    config.validate()

    # Configurer les logs
    setup_logging(app)

    # Enregistrer les blueprints
    app.register_blueprint(movies_bp)

    # Enregistrer les gestionnaires d'erreurs
    register_error_handlers(app)

    # Enregistrer les processeurs de contexte
    register_context_processors(app)

    # Configurer l'optimisation des ressources statiques
    configure_static_optimization(app)

    return app