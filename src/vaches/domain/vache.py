from src.vaches.domain.errors.exceptions import InvalidVacheException

class Vache:
    AGE_MAX = 25
    PANSE_MAX = 50.0
    RENDEMENT_RUMINATION = 0.25

    def __init__(self, petit_nom: str, poids: float, age: int):
        if not petit_nom or not petit_nom.strip():
            raise InvalidVacheException()

        if not (0 <= age <= self.AGE_MAX):
            raise InvalidVacheException()

        if poids < 0:
            raise InvalidVacheException()

        self.petit_nom = petit_nom
        self.poids = float(poids)
        self.age = age
        self.panse = 0.0

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