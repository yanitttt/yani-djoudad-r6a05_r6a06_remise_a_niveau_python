import pytest

from vaches.exceptions import InvalidVacheException
from vaches.vache import Vache


# -------------------------
# CONSTRUCTION
# -------------------------

def test_should_create_vache_given_valid_state():
    # Arrange
    vache = Vache(petitNom="Marguerite", poids=450.0, age=5)

    # Act
    poids = vache.poids

    # Assert (1 assertion métier)
    assert poids == 450.0


@pytest.mark.parametrize("petitNom", ["", "   ", "\n\t"])
def test_should_raise_invalid_vache_exception_given_empty_petit_nom(petitNom):
    # Arrange / Act / Assert
    with pytest.raises(InvalidVacheException):
        Vache(petitNom=petitNom, poids=450.0, age=5)


@pytest.mark.parametrize("age", [-1, 26])
def test_should_raise_invalid_vache_exception_given_invalid_age(age):
    # Arrange / Act / Assert
    with pytest.raises(InvalidVacheException):
        Vache(petitNom="Marguerite", poids=450.0, age=age)


@pytest.mark.parametrize("poids", [-1.0])
def test_should_raise_invalid_vache_exception_given_negative_poids(poids):
    # Arrange / Act / Assert
    with pytest.raises(InvalidVacheException):
        Vache(petitNom="Marguerite", poids=poids, age=5)


# -------------------------
# BROUTER (primaire uniquement)
# -------------------------

def test_should_increase_panse_given_positive_quantity_when_brouter():
    # Arrange
    vache = Vache(petitNom="Marguerite", poids=450.0, age=5)
    vache.brouter(10.0)  # panse initiale = 10

    # Act
    vache.brouter(5.0)

    # Assert (1 assertion métier)
    assert vache.panse == 15.0


@pytest.mark.parametrize("quantite", [0.0, -1.0])
def test_should_raise_invalid_vache_exception_given_non_positive_quantity_when_brouter(quantite):
    # Arrange
    vache = Vache(petitNom="Marguerite", poids=450.0, age=5)

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        vache.brouter(quantite)


def test_should_raise_invalid_vache_exception_given_typed_food_when_brouter_on_vache():
    # Arrange
    vache = Vache(petitNom="Marguerite", poids=450.0, age=5)
    vache.brouter(10.0)

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        vache.brouter(5.0, nourriture="HERBE")  # tout ≠ None doit être refusé


def test_should_allow_brouter_given_quantity_that_reaches_panse_max_exactly():
    # Arrange
    vache = Vache(petitNom="Marguerite", poids=450.0, age=5)
    vache.brouter(Vache.PANSE_MAX - 5.0)

    # Act
    vache.brouter(5.0)

    # Assert (1 assertion métier)
    assert vache.panse == Vache.PANSE_MAX


def test_should_raise_invalid_vache_exception_given_quantity_that_exceeds_panse_max_when_brouter():
    # Arrange
    vache = Vache(petitNom="Marguerite", poids=450.0, age=5)
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
    vache = Vache(petitNom="Marguerite", poids=450.0, age=5)
    vache.brouter(panse_initiale)

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        vache.brouter(quantite)


# -------------------------
# RUMINER
# -------------------------

def test_should_empty_panse_given_positive_panse_when_ruminer():
    # Arrange
    vache = Vache(petitNom="Marguerite", poids=450.0, age=5)
    vache.brouter(10.0)

    # Act
    vache.ruminer()

    # Assert (1 assertion métier)
    assert vache.panse == 0.0


def test_should_increase_poids_given_positive_panse_when_ruminer():
    # Arrange
    vache = Vache(petitNom="Marguerite", poids=450.0, age=5)
    vache.brouter(20.0)

    # Act
    vache.ruminer()

    # Assert (1 assertion métier)
    assert vache.poids == 450.0 + (Vache.RENDEMENT_RUMINATION * 20.0)


def test_should_raise_invalid_vache_exception_given_empty_panse_when_ruminer():
    # Arrange
    vache = Vache(petitNom="Marguerite", poids=450.0, age=5)

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        vache.ruminer()


# -------------------------
# VIEILLIR
# -------------------------

def test_should_increase_age_by_one_given_age_below_age_max_when_vieillir():
    # Arrange
    vache = Vache(petitNom="Marguerite", poids=450.0, age=5)

    # Act
    vache.vieillir()

    # Assert (1 assertion métier)
    assert vache.age == 6


def test_should_raise_invalid_vache_exception_given_age_max_when_vieillir():
    # Arrange
    vache = Vache(petitNom="Marguerite", poids=450.0, age=Vache.AGE_MAX)

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        vache.vieillir()
