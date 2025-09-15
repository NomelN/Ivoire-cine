"""
Utilitaires de validation pour l'application
"""
import re
from typing import Optional
from app.config.settings import get_config

config = get_config()

def validate_query(query: Optional[str]) -> Optional[str]:
    """
    Valide et nettoie une requête de recherche

    Args:
        query: La requête à valider

    Returns:
        La requête nettoyée ou None si invalide
    """
    if not query:
        return None

    # Supprimer les caractères dangereux et nettoyer
    query = re.sub(r'[<>"\'\\]', '', query.strip())

    # Vérifier la longueur
    if len(query) > config.MAX_QUERY_LENGTH:
        return None

    # Vérifier qu'il reste du contenu utile
    if len(query.strip()) < 1:
        return None

    return query

def validate_page(page: any) -> int:
    """
    Valide le numéro de page

    Args:
        page: Le numéro de page à valider

    Returns:
        Un numéro de page valide entre 1 et MAX_PAGE_LIMIT
    """
    try:
        page_num = int(page)
        return max(1, min(page_num, config.MAX_PAGE_LIMIT))
    except (ValueError, TypeError):
        return 1

def validate_genre_id(genre_id: any) -> Optional[int]:
    """
    Valide l'ID de genre

    Args:
        genre_id: L'ID de genre à valider

    Returns:
        L'ID de genre valide ou None si invalide
    """
    try:
        genre_num = int(genre_id)
        if 1 <= genre_num <= config.MAX_GENRE_ID:
            return genre_num
        return None
    except (ValueError, TypeError):
        return None

def sanitize_for_display(text: str) -> str:
    """
    Nettoie un texte pour l'affichage sécurisé

    Args:
        text: Le texte à nettoyer

    Returns:
        Le texte nettoyé
    """
    if not text:
        return ""

    # Échapper les caractères HTML de base
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&#x27;")

    return text