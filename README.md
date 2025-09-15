# 🎬 Ivoire Ciné

Une application web moderne de streaming et découverte de films utilisant l'API TMDB.

## 🌟 Fonctionnalités

### 🎯 Navigation et Découverte
- **Films populaires** avec pagination intelligente
- **Catégories TMDB** : Films en salle, populaires, mieux notés, à venir
- **Genres** : Action, comédie, drame, et tous les genres TMDB
- **Recherche avancée** avec validation et nettoyage des requêtes

### 🎨 Interface Utilisateur
- **Design responsive** adaptatif mobile/desktop
- **Navigation moderne** avec dropdowns interactifs
- **Cartes de films** avec lazy loading des images
- **Pagination fluide** avec navigation contextuelle

### 🔒 Sécurité et Performance
- **Validation complète** des entrées utilisateur
- **Protection XSS** et injection de code
- **Cache API intelligent** (1h TTL)
- **Gestion d'erreurs** sécurisée sans exposition de données sensibles
- **Timeouts configurés** pour les requêtes API

## 🏗️ Architecture

### Structure MVC Moderne
```
app/
├── factory.py              # Factory pattern Flask
├── config/
│   └── settings.py         # Configuration multi-environnements
├── routes/
│   └── movies.py           # Routes avec blueprints
├── services/
│   └── tmdb_service.py     # Service API avec cache
└── utils/
    ├── validators.py       # Validation et sanitisation
    ├── errors.py           # Gestion d'erreurs centralisée
    └── context_processors.py
```

### Templates Modulaires
```
templates/
├── base.html               # Template de base
├── components/
│   ├── navbar.html         # Navigation réutilisable
│   ├── movie_card.html     # Carte film standardisée
│   └── pagination.html     # Pagination intelligente
└── [pages].html            # Pages spécifiques
```

## 🚀 Installation et Usage

### Prérequis
- Python 3.8+
- Clé API TMDB (gratuite sur [themoviedb.org](https://www.themoviedb.org/settings/api))

### Installation
```bash
# Cloner le repository
git clone https://github.com/NomelN/Ivoire-cine.git
cd Ivoire-cine

# Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configuration
cp .env.example .env
# Éditer .env et ajouter votre TMDB_API_KEY
```

### Lancement
```bash
# Méthode recommandée
source .venv/bin/activate && python app.py

# Alternative avec Flask
export FLASK_APP=app
flask run --port=5002
```

L'application sera accessible sur **http://127.0.0.1:5002**

## 🧪 Tests et Qualité

### Framework de Tests
- **pytest** avec 42 tests unitaires
- **92% de couverture** de code
- **Mocking** des appels API externes
- **Tests de sécurité** et validation

```bash
# Lancer tous les tests
python -m pytest

# Avec rapport de couverture
python -m pytest --cov=app --cov-report=term-missing

# Tests spécifiques
python -m pytest tests/test_validators.py -v

# Rapport HTML
python -m pytest --cov=app --cov-report=html
```

### Métriques de Qualité
- ✅ **42 tests** passants
- ✅ **92% coverage**
- ✅ **0 duplication** de code
- ✅ **Architecture MVC** propre
- ✅ **Sécurité** validée

## 🔧 Configuration

### Environnements
- **Development** : Debug activé, logs détaillés
- **Production** : Optimisé, logs sécurisés
- **Testing** : Configuration isolée pour les tests

### Variables d'environnement
```bash
TMDB_API_KEY=your_api_key_here
FLASK_ENV=development  # ou production
SECRET_KEY=your_secret_key_for_production
```

## 🎨 Fonctionnalités Techniques

### Performance
- **Cache en mémoire** pour les appels API répétés
- **Lazy loading** des images de films
- **Pagination limitée** (max 500 pages TMDB)
- **Validation côté client** JavaScript

### Sécurité
- **Validation stricte** des paramètres GET
- **Sanitisation** des entrées utilisateur
- **Timeouts** sur les requêtes externes
- **Messages d'erreur** sécurisés
- **Protection contre l'exposition** de clés API

### UX/UI
- **Design responsive** Grid/Flexbox
- **Dropdowns interactifs** avec JavaScript
- **Messages flash** pour le feedback utilisateur
- **États vides** informatifs

## 🌐 API TMDB

L'application utilise [The Movie Database API](https://www.themoviedb.org/documentation/api) :

### Endpoints utilisés
- `/movie/popular` - Films populaires
- `/movie/now_playing` - Films en salle
- `/movie/top_rated` - Films mieux notés
- `/movie/upcoming` - Films à venir
- `/search/movie` - Recherche de films
- `/discover/movie` - Découverte par genre
- `/genre/movie/list` - Liste des genres

### Spécifications
- **Langue** : Français (fr-FR)
- **Images** : 500px de largeur
- **Pagination** : Limitée à 500 pages max
- **Cache** : 1 heure de TTL

## 📁 Structure du Projet

```
Ivoire-cine/
├── app.py                  # Point d'entrée principal
├── app/                    # Package principal
├── templates/              # Templates Jinja2
├── static/                 # Assets CSS/JS
├── tests/                  # Suite de tests
├── requirements.txt        # Dépendances Python
├── pytest.ini            # Configuration des tests
├── .env.example           # Template de configuration
├── .gitignore            # Fichiers à ignorer
└── CLAUDE.md             # Documentation développeur
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.