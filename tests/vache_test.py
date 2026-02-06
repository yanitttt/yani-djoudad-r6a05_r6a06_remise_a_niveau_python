import pytest

from src.vaches.domain.errors.exceptions import InvalidVacheException
from src.vaches.domain.vache import Vache


# -------------------------
# CONSTRUCTION
# -------------------------

def test_should_create_vache_given_valid_state():
    # Arrange
    vache = Vache(petit_nom="Marguerite", poids=450.0)

    # Act
    poids = vache.poids

    # Assert (1 assertion métier)
    assert poids == 450.0


@pytest.mark.parametrize("petit_nom", ["", "   ", "\n\t"])
def test_should_raise_invalid_vache_exception_given_empty_petit_nom(petit_nom):
    # Arrange / Act / Assert
    with pytest.raises(InvalidVacheException):
        Vache(petit_nom=petit_nom, poids=450.0)


'''@pytest.mark.parametrize("age", [-1, 26])
def test_should_raise_invalid_vache_exception_given_invalid_age(age):
    # Arrange / Act / Assert
    with pytest.raises(InvalidVacheException):
        Vache(petit_nom="Marguerite", poids=450.0)
'''

def test_should_initialize_age_at_birth_age_given_new_vache():
    # Arrange
    vache = Vache(petit_nom="Béb", poids=40.0)

    # Act / Assert
    # On vérifie que l'age est bien initialisé à AGE_NAISSANCE (0)
    assert vache.age == Vache.AGE_NAISSANCE

@pytest.mark.parametrize("poids", [-1.0])
def test_should_raise_invalid_vache_exception_given_negative_poids(poids):
    # Arrange / Act / Assert
    with pytest.raises(InvalidVacheException):
        Vache(petit_nom="Marguerite", poids=poids)


# -------------------------
# BROUTER (primaire uniquement)
# -------------------------

def test_should_increase_panse_given_positive_quantity_when_brouter():
    # Arrange
    vache = Vache(petit_nom="Marguerite", poids=450.0)
    vache.brouter(10.0)  # panse initiale = 10

    # Act
    vache.brouter(5.0)

    # Assert (1 assertion métier)
    assert vache.panse == 15.0


@pytest.mark.parametrize("quantite", [0.0, -1.0])
def test_should_raise_invalid_vache_exception_given_non_positive_quantity_when_brouter(quantite):
    # Arrange
    vache = Vache(petit_nom="Marguerite", poids=450.0)

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        vache.brouter(quantite)


def test_should_raise_invalid_vache_exception_given_typed_food_when_brouter_on_vache():
    # Arrange
    vache = Vache(petit_nom="Marguerite", poids=450.0)
    vache.brouter(10.0)

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        vache.brouter(5.0, nourriture="HERBE")  # tout ≠ None doit être refusé


def test_should_allow_brouter_given_quantity_that_reaches_panse_max_exactly():
    # Arrange
    vache = Vache(petit_nom="Marguerite", poids=450.0)
    vache.brouter(Vache.PANSE_MAX - 5.0)

    # Act
    vache.brouter(5.0)

    # Assert (1 assertion métier)
    assert vache.panse == Vache.PANSE_MAX


def test_should_raise_invalid_vache_exception_given_quantity_that_exceeds_panse_max_when_brouter():
    # Arrange
    vache = Vache(petit_nom="Marguerite", poids=450.0)
    vache.brouter(Vache.PANSE_MAX - 5.0)

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        vache.brouter(5.0001)


@pytest.mark.parametrize(
    "panse_initiale, quantite",
    [
        (Vache.PANSE_MAX, 0.1),
        (Vache.PANSE_MAX - 0.01, 0.02),
        (Vache.PANSE_MAX - 1.0, 2.0),
    ],
)
def test_should_raise_invalid_vache_exception_given_panse_overflow_cases_when_brouter(panse_initiale, quantite):
    # Arrange
    vache = Vache(petit_nom="Marguerite", poids=450.0)
    vache.brouter(panse_initiale)

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        vache.brouter(quantite)


# -------------------------
# RUMINER
# -------------------------

def test_should_empty_panse_given_positive_panse_when_ruminer():
    # Arrange
    vache = Vache(petit_nom="Marguerite", poids=450.0)
    vache.brouter(10.0)

    # Act
    vache.ruminer()

    # Assert (1 assertion métier)
    assert vache.panse == 0.0


def test_should_increase_poids_given_positive_panse_when_ruminer():
    # Arrange
    vache = Vache(petit_nom="Marguerite", poids=450.0)
    vache.brouter(20.0)

    # Act
    vache.ruminer()

    # Assert (1 assertion métier)
    assert vache.poids == 450.0 + (Vache.RENDEMENT_RUMINATION * 20.0)


def test_should_raise_invalid_vache_exception_given_empty_panse_when_ruminer():
    # Arrange
    vache = Vache(petit_nom="Marguerite", poids=450.0)

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        vache.ruminer()


# -------------------------
# VIEILLIR
# -------------------------

def test_should_raise_invalid_vache_exception_when_aging_beyond_max_limit():
    # Arrange
    vache = Vache(petit_nom="Mamie", poids=450.0)

    # On utilise le helper pour l'amener a l'age de 25 ans
    _faire_vieillir_jusqu_a_la_limite(vache)

    # Act / Assert
    # a 25 ans, essayer de vieillir une fois de plus doit lever l'exception
    with pytest.raises(InvalidVacheException):
        vache.vieillir()

'''
HELPER
'''

def _faire_vieillir_jusqu_a_la_limite(vache: Vache):
    """
    Simule le passage des années en appelant la méthode officielle vieillir()
    jusqu'à ce que la vache atteigne son âge maximum.
    """
    # On calcule combien d'années il reste avant l'âge max
    annees_restantes = Vache.AGE_MAX - vache.age

    for _ in range(annees_restantes):
        vache.vieillir()