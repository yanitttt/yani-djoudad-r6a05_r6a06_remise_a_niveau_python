from src.vaches.domain.errors.exceptions import InvalidVacheException

class Vache:
    AGE_MAX:int = 25
    POIDS_MAX:float = 1000.0
    PANSE_MAX:float = 50.0
    POIDS_MIN_PANSE:float = 0.0
    PENSE_VIDE:float = 0.0
    RENDEMENT_RUMINATION:float = 0.25
    AGE_NAISSANCE:int = 0

    _NEXT_ID = 1

    def __init__(self, petit_nom: str, poids: float):
        if not petit_nom or not petit_nom.strip():
            raise InvalidVacheException()

        if not (0 <= self.AGE_NAISSANCE <= self.AGE_MAX):
            raise InvalidVacheException()

        if poids < 0:
            raise InvalidVacheException()

        self.id = Vache._NEXT_ID
        Vache._NEXT_ID += 1

        self.petit_nom = petit_nom
        self.poids = float(poids)
        self.age = self.AGE_NAISSANCE
        self.panse = self.PENSE_VIDE


    def brouter(self, quantite: float, nourriture=None):
        if nourriture is not None:
            raise InvalidVacheException()

        if quantite <= 0:
            raise InvalidVacheException()

        if self.panse + quantite > self.PANSE_MAX:
            raise InvalidVacheException()

        self.panse += quantite

    def ruminer(self):
        if self.panse <= 0:
            raise InvalidVacheException()

        gain = self.panse * self.RENDEMENT_RUMINATION
        self.poids += gain

        self.panse = 0.0

    def vieillir(self):
        if self.age >= self.AGE_MAX:
            raise InvalidVacheException()

        self.age += 1