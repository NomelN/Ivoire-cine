"""
Tests pour les fonctions de validation
"""
import pytest
from app.utils.validators import validate_query, validate_page, validate_genre_id, sanitize_for_display


class TestValidateQuery:
    """Tests pour validate_query"""

    def test_validate_query_valid(self):
        """Test avec une requête valide"""
        assert validate_query("batman") == "batman"
        assert validate_query("  batman  ") == "batman"
        assert validate_query("batman returns") == "batman returns"

    def test_validate_query_empty(self):
        """Test avec une requête vide"""
        assert validate_query("") is None
        assert validate_query("   ") is None
        assert validate_query(None) is None

    def test_validate_query_dangerous_chars(self):
        """Test avec des caractères dangereux"""
        assert validate_query("<script>alert()</script>") == "scriptalert()/script"
        assert validate_query("batman\"test") == "batmantest"
        assert validate_query("batman'test") == "batmantest"

    def test_validate_query_too_long(self):
        """Test avec une requête trop longue"""
        long_query = "a" * 101
        assert validate_query(long_query) is None

    def test_validate_query_max_length(self):
        """Test avec une requête à la limite"""
        max_query = "a" * 100
        assert validate_query(max_query) == max_query


class TestValidatePage:
    """Tests pour validate_page"""

    def test_validate_page_valid(self):
        """Test avec des pages valides"""
        assert validate_page(1) == 1
        assert validate_page("5") == 5
        assert validate_page(100) == 100

    def test_validate_page_invalid(self):
        """Test avec des pages invalides"""
        assert validate_page("abc") == 1
        assert validate_page(None) == 1
        assert validate_page("") == 1

    def test_validate_page_limits(self):
        """Test avec les limites"""
        assert validate_page(0) == 1  # Minimum à 1
        assert validate_page(-5) == 1  # Négatif → 1
        assert validate_page(2000) == 1000  # Maximum à 1000


class TestValidateGenreId:
    """Tests pour validate_genre_id"""

    def test_validate_genre_id_valid(self):
        """Test avec des IDs valides"""
        assert validate_genre_id(28) == 28
        assert validate_genre_id("35") == 35
        assert validate_genre_id(10779) == 10779  # Maximum TMDB

    def test_validate_genre_id_invalid(self):
        """Test avec des IDs invalides"""
        assert validate_genre_id("abc") is None
        assert validate_genre_id(None) is None
        assert validate_genre_id("") is None

    def test_validate_genre_id_limits(self):
        """Test avec les limites"""
        assert validate_genre_id(0) is None  # En dessous du minimum
        assert validate_genre_id(-1) is None  # Négatif
        assert validate_genre_id(10780) is None  # Au-dessus du maximum


class TestSanitizeForDisplay:
    """Tests pour sanitize_for_display"""

    def test_sanitize_for_display_normal(self):
        """Test avec du texte normal"""
        assert sanitize_for_display("Hello World") == "Hello World"
        assert sanitize_for_display("") == ""

    def test_sanitize_for_display_html_chars(self):
        """Test avec des caractères HTML"""
        assert sanitize_for_display("<script>") == "&lt;script&gt;"
        assert sanitize_for_display("A & B") == "A &amp; B"
        assert sanitize_for_display('Say "Hello"') == "Say &quot;Hello&quot;"
        assert sanitize_for_display("It's here") == "It&#x27;s here"

    def test_sanitize_for_display_none(self):
        """Test avec None"""
        assert sanitize_for_display(None) == ""