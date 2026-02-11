from src.vaches.domain.strategies.rumination_strategy import RuminationStrategy
from src.vaches.domain.errors.exceptions import InvalidVacheException

class StandardMilkStrategy(RuminationStrategy):
    RENDEMENT_LAIT = 1.1
    PRODUCTION_LAIT_MAX = 40.0

    def calculer_lait(self, vache: 'Vache', panse_avant: float) -> float:
        return panse_avant * self.RENDEMENT_LAIT

    def stocker_lait(self, vache: 'Vache', lait: float) -> None:
        if vache.lait_disponible + lait > self.PRODUCTION_LAIT_MAX:
            raise InvalidVacheException()

        vache.lait_disponible += lait
        vache.lait_total_produit += lait

    def post_rumination(self, vache: 'Vache', panse_avant: float, lait: float) -> None:
        pass