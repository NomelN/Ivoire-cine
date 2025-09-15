"""
Gestionnaire d'erreurs centralisé
"""
from flask import render_template, request, current_app
import logging

def register_error_handlers(app):
    """Enregistre les gestionnaires d'erreurs pour l'application"""

    @app.errorhandler(404)
    def not_found_error(error):
        """Gestionnaire pour les erreurs 404"""
        current_app.logger.warning(f"Page non trouvée: {request.url}")
        return render_template('error.html', error="Page non trouvée"), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Gestionnaire pour les erreurs 500"""
        current_app.logger.error(f"Erreur interne: {str(error)}")
        return render_template(
            'error.html',
            error="Une erreur inattendue s'est produite"
        ), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        """Gestionnaire pour les erreurs 403"""
        current_app.logger.warning(f"Accès interdit: {request.url}")
        return render_template('error.html', error="Accès interdit"), 403

    @app.errorhandler(429)
    def ratelimit_handler(error):
        """Gestionnaire pour les erreurs de limitation de débit"""
        current_app.logger.warning(f"Trop de requêtes depuis: {request.remote_addr}")
        return render_template(
            'error.html',
            error="Trop de requêtes - veuillez patienter"
        ), 429

def setup_logging(app):
    """Configure le système de logs de manière sécurisée"""

    # SÉCURITÉ: Désactiver les logs debug d'urllib3 qui exposent les clés API
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests.packages.urllib3').setLevel(logging.WARNING)

    if not app.debug and not app.testing:
        # Configuration pour la production
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        app.logger.setLevel(logging.INFO)
        app.logger.info('Application Ivoire Ciné démarrée')
    else:
        # Configuration pour le développement - logs sécurisés
        logging.basicConfig(
            level=logging.INFO,  # Changé de DEBUG à INFO pour éviter l'exposition des clés
            format='%(asctime)s %(levelname)s: %(message)s'
        )
        app.logger.setLevel(logging.INFO)
        app.logger.info('Application Ivoire Ciné démarrée en mode développement')