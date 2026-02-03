import pytest

from vaches.exceptions import InvalidVacheException
from vaches.nourriture.TypeNourriture import TypeNourriture
from vaches.pie_noire import PieNoire
from vaches.vache import Vache
from vaches.vache_a_lait import VacheALait


@pytest.fixture
def pie_ok() -> PieNoire:
    # État valide
    return PieNoire(
        petit_nom ="Bella",
        poids=520.0,
        age=6,
        nb_taches_blanches=12,
        nb_taches_noires=18,
    )


# -------------------------
# INIT + PROPERTIES
# -------------------------

def test_should_create_pie_noire_given_valid_state(pie_ok: PieNoire):
    # Arrange / Act
    nb = pie_ok.nb_taches_noires

    # Assert (1 assertion métier)
    assert nb == 18


def test_should_return_copy_of_ration_given_ration_property(pie_ok: PieNoire):
    # Arrange
    pie_ok.brouter(2.0, TypeNourriture.HERBE)

    # Act
    r = pie_ok.ration
    r[TypeNourriture.HERBE] = 999.0  # modif sur la copie

    # Assert (1 assertion métier) : la ration interne n'est pas modifiée
    assert pie_ok.ration[TypeNourriture.HERBE] == 2.0


@pytest.mark.parametrize("val", [0, -1])
def test_should_raise_invalid_vache_exception_given_non_positive_white_spots(val: int):
    # Arrange / Act / Assert
    with pytest.raises(InvalidVacheException):
        PieNoire("Bella", 520.0, 6, nb_taches_blanches=val, nb_taches_noires=10)


@pytest.mark.parametrize("val", [0, -1])
def test_should_raise_invalid_vache_exception_given_non_positive_black_spots(val: int):
    # Arrange / Act / Assert
    with pytest.raises(InvalidVacheException):
        PieNoire("Bella", 520.0, 6, nb_taches_blanches=10, nb_taches_noires=val)


@pytest.mark.parametrize("val", ["12", 12.0, None])
def test_should_raise_invalid_vache_exception_given_non_int_white_spots(val):
    # Arrange / Act / Assert
    with pytest.raises(InvalidVacheException):
        PieNoire("Bella", 520.0, 6, nb_taches_blanches=val, nb_taches_noires=10)


@pytest.mark.parametrize("val", ["18", 18.0, None])
def test_should_raise_invalid_vache_exception_given_non_int_black_spots(val):
    # Arrange / Act / Assert
    with pytest.raises(InvalidVacheException):
        PieNoire("Bella", 520.0, 6, nb_taches_blanches=10, nb_taches_noires=val)


# -------------------------
# BROUTER : primaire + typé
# -------------------------

def test_should_not_change_ration_given_primary_brouter(pie_ok: PieNoire):
    # Arrange

    # Act
    pie_ok.brouter(3.0)

    # Assert (1 assertion métier)
    assert pie_ok.ration == {}


def test_should_add_food_in_ration_given_typed_brouter(pie_ok: PieNoire):
    # Arrange

    # Act
    pie_ok.brouter(2.0, TypeNourriture.FOIN)

    # Assert (1 assertion métier)
    assert pie_ok.ration[TypeNourriture.FOIN] == 2.0


def test_should_accumulate_same_food_given_two_typed_brouter_calls(pie_ok: PieNoire):
    # Arrange
    pie_ok.brouter(2.0, TypeNourriture.HERBE)

    # Act
    pie_ok.brouter(1.5, TypeNourriture.HERBE)

    # Assert (1 assertion métier)
    assert pie_ok.ration[TypeNourriture.HERBE] == 3.5


# -------------------------
# _calculer_lait : branche ration vide + ration non vide
# -------------------------

def test_should_fallback_to_vache_a_lait_calcul_given_empty_ration(pie_ok: PieNoire):
    # Arrange
    pie_ok.brouter(10.0)  # panse > 0, ration vide => super()._calculer_lait(panse_avant)
    expected = VacheALait.RENDEMENT_LAIT * 10.0

    # Act
    pie_ok.ruminer()
    lait = pie_ok.lait_disponible

    # Assert (1 assertion métier)
    assert lait == pytest.approx(expected)


def test_should_compute_specialized_lait_given_non_empty_ration(pie_ok: PieNoire):
    # Arrange
    pie_ok.brouter(2.0, TypeNourriture.HERBE)
    pie_ok.brouter(1.0, TypeNourriture.CEREALES)

    facteur = (
            2.0 * PieNoire.COEFFICIENT_NUTRITIONNEL[TypeNourriture.HERBE]
            + 1.0 * PieNoire.COEFFICIENT_NUTRITIONNEL[TypeNourriture.CEREALES]
    )
    expected = VacheALait.RENDEMENT_LAIT * facteur

    # Act
    pie_ok.ruminer()
    lait = pie_ok.lait_disponible

    # Assert (1 assertion métier)
    assert lait == pytest.approx(expected)


# -------------------------
# _post_rumination : reset ration
# -------------------------

def test_should_clear_ration_given_ruminer_called(pie_ok: PieNoire):
    # Arrange
    pie_ok.brouter(2.0, TypeNourriture.MARGUERITE)

    # Act
    pie_ok.ruminer()
    lait = pie_ok.lait_disponible

    # Assert (1 assertion métier)
    assert pie_ok.ration == {}


# -------------------------
# Couverture des validations héritées via brouter (quantité invalide / panse max)
# -------------------------

@pytest.mark.parametrize("q", [0.0, -1.0])
def test_should_raise_invalid_vache_exception_given_non_positive_quantity_when_brouter(pie_ok: PieNoire, q: float):
    # Arrange / Act / Assert
    with pytest.raises(InvalidVacheException):
        pie_ok.brouter(q)


def test_should_raise_invalid_vache_exception_given_panse_overflow_when_brouter(pie_ok: PieNoire):
    # Arrange
    pie_ok.brouter(Vache.PANSE_MAX)  # remplit exactement la panse

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        pie_ok.brouter(0.1)
