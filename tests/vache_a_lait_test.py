import pytest

from src.vaches.domain.errors.exceptions import InvalidVacheException
from src.vaches import VacheALait


# -------------------------
# RUMINATION -> PRODUCTION/ STOCKAGE DE LAIT (dépend de la panse)
# -------------------------

def test_should_start_with_empty_panse_given_new_vache_a_lait():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)

    # Act / Assert (1 assertion métier)
    assert vache.panse == 0


def test_should_increase_lait_disponible_given_positive_panse_when_ruminer():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)
    vache.brouter(10.0)

    # Act
    vache.ruminer()

    # Assert (1 assertion métier)
    assert vache.lait_disponible == pytest.approx(VacheALait.RENDEMENT_LAIT * 10.0)


def test_should_increase_lait_total_produit_given_positive_panse_when_ruminer():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)
    vache.brouter(10.0)

    # Act
    vache.ruminer()
    actual = vache.lait_total_produit
    expected = VacheALait.RENDEMENT_LAIT * 10.0

    # Assert (1 assertion métier)
    assert actual == pytest.approx(expected)


def test_should_return_lait_produced_given_positive_panse_when_ruminer():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)
    vache.brouter(10.0)

    # Act
    vache.ruminer()
    actual = vache.lait_total_produit
    expected = VacheALait.RENDEMENT_LAIT * 10.0

    # Assert (1 assertion métier)
    assert actual == pytest.approx(expected)


def test_should_raise_invalid_vache_exception_given_empty_panse_when_ruminer():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        vache.ruminer()


def test_should_accumulate_lait_disponible_given_two_ruminations():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)


    # Act
    vache.brouter(10.0)
    vache.ruminer()
    vache.brouter(4.0)
    vache.ruminer()

    # Assert (1 assertion métier)

    assert vache.lait_disponible == pytest.approx(VacheALait.RENDEMENT_LAIT * (10.0 + 4.0))


# -------------------------
# TRAITE
# -------------------------

def test_should_decrease_lait_disponible_given_valid_litres_when_traire():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)
    vache.brouter(10.0)
    vache.ruminer()

    # Act
    vache.traire(3.0)

    # Assert (1 assertion métier)
    assert vache.lait_disponible == pytest.approx((VacheALait.RENDEMENT_LAIT * 10.0) - 3.0)


def test_should_return_litres_given_valid_litres_when_traire():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)
    vache.brouter(10.0)
    vache.ruminer()

    # Act
    litres_trais = vache.traire(3.0)

    # Assert (1 assertion métier)
    assert litres_trais == 3.0


def test_should_increase_lait_total_traite_given_valid_litres_when_traire():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)
    vache.brouter(10.0)
    vache.ruminer()

    # Act
    vache.traire(3.0)

    # Assert (1 assertion métier)
    assert vache.lait_total_traite == 3.0


def test_should_accumulate_lait_total_traite_given_two_traite_operations():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)
    vache.brouter(10.0)
    vache.ruminer()

    # Act
    vache.traire(2.0)
    vache.traire(3.0)

    # Assert (1 assertion métier)
    assert vache.lait_total_traite == 5.0


@pytest.mark.parametrize("litres", [0.0, -1.0])
def test_should_raise_invalid_vache_exception_given_non_positive_litres_when_traire(litres):
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)
    vache.brouter(10.0)
    vache.ruminer()

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        vache.traire(litres)


def test_should_raise_invalid_vache_exception_given_litres_greater_than_lait_disponible_when_traire():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)
    vache.brouter(10.0)
    vache.ruminer()

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        vache.traire(vache.lait_disponible + 0.0001)


# -------------------------
# BROUTEMENT TYPÉ INTERDIT SUR VacheALait
# -------------------------

def test_should_raise_invalid_vache_exception_given_typed_food_when_brouter_on_vache_a_lait():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        vache.brouter(2.0, nourriture="FOIN")


# -------------------------
# Test de la production de lait (capacité max)
# -------------------------

def _produire_lait_jusqua(vache: VacheALait, cible_lait: float) -> None:
    if cible_lait < 0:
        raise ValueError("cible_lait doit être >= 0")
    if cible_lait > VacheALait.PRODUCTION_LAIT_MAX:
        raise ValueError("cible_lait ne doit pas dépasser PRODUCTION_LAIT_MAX")

    while vache.lait_disponible < cible_lait:
        restant = cible_lait - vache.lait_disponible
        panse_necessaire = restant / VacheALait.RENDEMENT_LAIT
        quantite = min(panse_necessaire, vache.PANSE_MAX)

        vache.brouter(quantite)
        vache.ruminer()

        if vache.lait_disponible > cible_lait + 1e-9:
            break


def test_should_allow_ruminer_given_lait_production_reaches_production_max_exactly():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)
    _produire_lait_jusqua(vache, VacheALait.PRODUCTION_LAIT_MAX - 1.0)

    # Act
    panse = 1.0 / VacheALait.RENDEMENT_LAIT
    vache.brouter(panse)
    vache.ruminer()

    # Assert (1 assertion métier)
    assert vache.lait_disponible == pytest.approx(VacheALait.PRODUCTION_LAIT_MAX)


def test_should_raise_invalid_vache_exception_given_lait_production_exceeds_production_max_when_ruminer():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)
    _produire_lait_jusqua(vache, VacheALait.PRODUCTION_LAIT_MAX - 0.5)

    # Act / Assert
    panse = 1.0 / VacheALait.RENDEMENT_LAIT
    vache.brouter(panse)

    with pytest.raises(InvalidVacheException):
        vache.ruminer()


def test_should_allow_ruminer_again_given_traite_frees_capacity_below_production_max():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)
    _produire_lait_jusqua(vache, VacheALait.PRODUCTION_LAIT_MAX)
    vache.traire(10.0)

    # Act
    panse = 10.0 / VacheALait.RENDEMENT_LAIT
    vache.brouter(panse)
    vache.ruminer()

    # Assert (1 assertion métier)
    assert vache.lait_disponible == pytest.approx(VacheALait.PRODUCTION_LAIT_MAX)


def test_should_raise_invalid_vache_exception_given_production_max_reached_when_ruminer():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)
    _produire_lait_jusqua(vache, VacheALait.PRODUCTION_LAIT_MAX)

    # Act / Assert
    vache.brouter(0.1)

    with pytest.raises(InvalidVacheException):
        vache.ruminer()

def test_should_include_milk_fields_in_str_given_new_vache_a_lait():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)

    # Act
    s = str(vache)

    # Assert (1 assertion métier)
    assert "Lait disponible : 0.0 L" in s

def test_should_reflect_milk_values_in_str_given_ruminer_and_traire():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, age=5)
    vache.brouter(10.0)
    vache.ruminer()      # produit 11.0 L
    vache.traire(3.0)    # reste 8.0 L, total trait 3.0 L

    # Act
    s = str(vache)

    # Assert (1 assertion métier)
    assert "Lait total trait : 3.0 L" in s
