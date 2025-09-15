/**
 * Scripts principaux pour Ivoire Ciné
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des fonctionnalités
    initDropdowns();
    initImageLazyLoading();
    initSearchForm();
    initThemeToggle();
});

/**
 * Initialise les menus déroulants
 */
function initDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');

        if (toggle && menu) {
            // Afficher au hover
            dropdown.addEventListener('mouseenter', () => {
                menu.style.display = 'block';
            });

            // Masquer au leave
            dropdown.addEventListener('mouseleave', () => {
                menu.style.display = 'none';
            });

            // Gérer les clics sur les liens
            toggle.addEventListener('click', (e) => {
                e.preventDefault();
                const isVisible = menu.style.display === 'block';
                menu.style.display = isVisible ? 'none' : 'block';
            });
        }
    });

    // Fermer les dropdowns si on clique ailleurs
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.style.display = 'none';
            });
        }
    });
}

/**
 * Améliore le chargement des images avec lazy loading
 */
function initImageLazyLoading() {
    // Utiliser le lazy loading natif du navigateur
    const images = document.querySelectorAll('img[loading="lazy"]');

    images.forEach(img => {
        // Ajouter une transition douce
        img.style.transition = 'opacity 0.3s ease';
        img.style.opacity = '0';

        // Quand l'image est chargée
        img.onload = function() {
            this.style.opacity = '1';
            this.classList.add('loaded');
        };

        // En cas d'erreur
        img.onerror = function() {
            this.style.opacity = '1';
            this.classList.add('error');
        };

        // Si l'image est déjà en cache, l'afficher immédiatement
        if (img.complete && img.naturalHeight !== 0) {
            img.style.opacity = '1';
            img.classList.add('loaded');
        }
    });
}

/**
 * Améliore le formulaire de recherche
 */
function initSearchForm() {
    const searchForm = document.querySelector('.search-form');
    const searchInput = searchForm?.querySelector('input[name="query"]');

    if (searchInput) {
        // Trim automatique des espaces
        searchInput.addEventListener('input', function() {
            this.value = this.value.trimStart();
        });

        // Validation avant soumission
        searchForm.addEventListener('submit', function(e) {
            const query = searchInput.value.trim();

            if (query.length < 1) {
                e.preventDefault();
                showMessage('Veuillez saisir au moins un caractère pour la recherche', 'warning');
                searchInput.focus();
                return false;
            }

            if (query.length > 100) {
                e.preventDefault();
                showMessage('La recherche est trop longue (maximum 100 caractères)', 'error');
                searchInput.focus();
                return false;
            }
        });
    }
}

/**
 * Affiche un message à l'utilisateur
 * @param {string} message - Le message à afficher
 * @param {string} type - Le type de message (info, warning, error, success)
 */
function showMessage(message, type = 'info') {
    // Supprimer les anciens messages
    const existingMessage = document.querySelector('.flash-message');
    if (existingMessage) {
        existingMessage.remove();
    }

    // Créer le nouveau message
    const messageDiv = document.createElement('div');
    messageDiv.className = `flash-message flash-${type}`;
    messageDiv.textContent = message;

    // Styles inline pour le message
    Object.assign(messageDiv.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '12px 20px',
        borderRadius: '4px',
        color: 'white',
        fontWeight: '500',
        zIndex: '9999',
        maxWidth: '400px',
        boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
    });

    // Couleurs selon le type
    const colors = {
        info: '#007BFF',
        warning: '#FFA500',
        error: '#DC3545',
        success: '#28A745'
    };

    messageDiv.style.backgroundColor = colors[type] || colors.info;

    // Ajouter au DOM
    document.body.appendChild(messageDiv);

    // Supprimer automatiquement après 4 secondes
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 4000);
}

/**
 * Utilitaire pour débouncer les fonctions
 * @param {Function} func - La fonction à débouncer
 * @param {number} wait - Le délai en millisecondes
 * @returns {Function} La fonction débouncée
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Gestion des erreurs JavaScript globales
 */
window.addEventListener('error', function(e) {
    console.error('Erreur JavaScript:', e.error);
    // En production, envoyer l'erreur à un service de monitoring
});

/**
 * Amélioration progressive pour les anciennes versions de navigateurs
 */
if (!window.fetch) {
    console.warn('Fetch API non supportée. Certaines fonctionnalités peuvent être limitées.');
}

/**
 * Initialise le système de basculement de thème
 */
function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;

    // Récupérer le thème sauvegardé ou utiliser la préférence système
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = savedTheme || (prefersDark ? 'dark' : 'light');

    // Appliquer le thème initial
    setTheme(initialTheme);

    // Écouter les clics sur le bouton de basculement
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
    });

    // Écouter les changements de préférence système
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (!localStorage.getItem('theme')) {
            setTheme(e.matches ? 'dark' : 'light');
        }
    });
}

/**
 * Applique un thème donné
 * @param {string} theme - Le thème à appliquer ('light' ou 'dark')
 */
function setTheme(theme) {
    const themeToggle = document.getElementById('theme-toggle');

    if (theme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        if (themeToggle) themeToggle.textContent = '☀️';
        localStorage.setItem('theme', 'dark');
    } else {
        document.documentElement.removeAttribute('data-theme');
        if (themeToggle) themeToggle.textContent = '🌙';
        localStorage.setItem('theme', 'light');
    }
}

// Export pour les tests (si module system disponible)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initDropdowns,
        initImageLazyLoading,
        initSearchForm,
        initThemeToggle,
        setTheme,
        showMessage,
        debounce
    };
}