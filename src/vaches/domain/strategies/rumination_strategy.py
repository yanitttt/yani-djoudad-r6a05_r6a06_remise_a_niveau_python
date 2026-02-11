from abc import ABC, abstractmethod

class RuminationStrategy(ABC):
    @abstractmethod
    def calculer_lait(self, vache: 'Vache', panse_avant: float) -> float:
        pass

    @abstractmethod
    def stocker_lait(self, vache: 'Vache', lait: float) -> None:
        pass

    @abstractmethod
    def post_rumination(self, vache: 'Vache', panse_avant: float, lait: float) -> None:
        pass
