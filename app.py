"""
Point d'entrée principal de l'application Ivoire Ciné
"""
import os
from app.factory import create_app

# Créer l'application avec la configuration appropriée
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

# Pour flask run - exportation de l'app
def create_flask_app():
    """Factory function pour flask run"""
    return create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Lancer en mode développement
    app.run(debug=True, host='127.0.0.1', port=5002)