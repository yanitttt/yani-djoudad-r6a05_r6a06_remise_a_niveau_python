from src.vaches.domain.errors.exceptions import InvalidVacheException
from src.vaches.domain.nourriture.TypeNourriture import TypeNourriture
from src.vaches.domain.vache import Vache
from src.vaches.domain.vache_a_lait import VacheALait

class PieNoire(VacheALait):

    COEFFICIENT_NUTRITIONNEL = {
        TypeNourriture.HERBE: 1.0,
        TypeNourriture.FOIN: 1.0,
        TypeNourriture.MARGUERITE: 1.0,
        TypeNourriture.PAILLE: 0.5,
        TypeNourriture.CEREALES: 2.0
    }

    def __init__(self, petit_nom: str, poids: float, age: int, nb_taches_blanches: int, nb_taches_noires: int):

        if type(nb_taches_blanches) is not int or type(nb_taches_noires) is not int:
            raise InvalidVacheException()

        if nb_taches_blanches <= 0 or nb_taches_noires <= 0:
            raise InvalidVacheException()

        super().__init__(petitNom=petit_nom, poids=poids, age=age)

        self.nb_taches_blanches = nb_taches_blanches
        self._nb_taches_noires = nb_taches_noires
        self._ration = {}

    @property
    def nb_taches_noires(self):
        return self._nb_taches_noires

    @property
    def ration(self):
        return self._ration.copy()

    def brouter(self, quantite: float, nourriture=None):

        super().brouter(quantite, nourriture=None)

        if nourriture:
            q_actuelle = self._ration.get(nourriture, 0.0)
            self._ration[nourriture] = q_actuelle + quantite

    def ruminer(self):
        if self.panse <= 0:
            raise InvalidVacheException()

        if not self._ration:
            production = self.panse * self.RENDEMENT_LAIT
        else:
            facteur_nutritionnel = 0.0
            for type_n, qte in self._ration.items():
                coeff = self.COEFFICIENT_NUTRITIONNEL.get(type_n, 0.0)
                facteur_nutritionnel += qte * coeff

            production = facteur_nutritionnel * self.RENDEMENT_LAIT

        if self.lait_disponible + production > self.PRODUCTION_LAIT_MAX:
            raise InvalidVacheException()

        Vache.ruminer(self)

        self.lait_disponible += production
        self.lait_total_produit += production

        self._ration = {}