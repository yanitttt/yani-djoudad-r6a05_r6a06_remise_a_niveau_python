from src.vaches.domain.errors.exceptions import InvalidVacheException
from src.vaches.domain.vache import Vache

class VacheALait(Vache):
    RENDEMENT_LAIT = 1.1
    PRODUCTION_LAIT_MAX = 40.0

    def __init__(self, petitNom: str, poids: float, age: int):
        super().__init__(petit_nom=petitNom, poids=poids, age=age)
        self.lait_disponible = 0.0
        self.lait_total_produit = 0.0
        self.lait_total_traite = 0.0

    def ruminer(self):
        if self.panse <= 0:
            raise InvalidVacheException()

        production = self.panse * self.RENDEMENT_LAIT

        if self.lait_disponible + production > self.PRODUCTION_LAIT_MAX:
            raise InvalidVacheException()

        super().ruminer()

        self.lait_disponible += production
        self.lait_total_produit += production

    def traire(self, litres: float) -> float:
        if litres <= 0 or litres > self.lait_disponible:
            raise InvalidVacheException()

        self.lait_disponible -= litres
        self.lait_total_traite += litres
        return litres

    def __str__(self):
        return f"{super().__str__()} Lait disponible : {self.lait_disponible} L, Lait total trait : {self.lait_total_traite} L"