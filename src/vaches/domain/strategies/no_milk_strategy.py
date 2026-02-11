from src.vaches.domain.strategies.rumination_strategy import RuminationStrategy

class NoMilkStrategy(RuminationStrategy):
    def calculer_lait(self, vache: 'Vache', panse_avant: float) -> float:
        return 0.0

    def stocker_lait(self, vache: 'Vache', lait: float) -> None:
        pass

    def post_rumination(self, vache: 'Vache', panse_avant: float, lait: float) -> None:
        pass