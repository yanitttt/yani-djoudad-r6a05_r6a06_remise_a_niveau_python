## Remise à niveau en Python objet

---
marp: false
theme: default
paginate: true
---

# R6A05 - R6A08 : Remise à niveau en Python
## B. Lemaire

---

## B — Points 2D et 3D (1/2)
### Classe `PointPlan` (écrite en Java)

```java
public class PointPlan {
    private float abscisse;
    private float ordonnee;

    public PointPlan() {
    }

    public PointPlan(float x, float y) {
        this.abscisse = x;
        this.ordonnee = y;
    }

    public PointPlan(PointPlan p) {
        this(p.abscisse, p.ordonnee);
    }

    public float getAbscisse() {
        return this.abscisse;
    }

    public float getOrdonnee() {
        return this.ordonnee;
    }

    public String toString() {
        return ("\n abscisse = " + this.abscisse +
                " ordonnee = " + this.ordonnee);
    }
}
```

Traduire cette classe en Python et prévoir des tests unitaires (`pytest`) pour valider les services de cette classe.

*Note :* Cette classe se trouvera dans la package `pointplan`.

---

## B — Points 2D et 3D (2/2)
On souhaite désormais prendre en compte une **troisième dimension** `azimut` pour représenter des points dans l

Ecrire la classe `Point3D` accompagnée des tests unitaires.


---

## C — Le monde des vaches (3/3)


**Objectif :** concevoir un mini-modèle métier orienté objet en Python en respectant strictement des règles de broutement, rumination, production de lait et traite, avec une modélisation robuste (invariants + exceptions).


⚠️ **Ce qui est fourni :**
- l’énumération `TypeNourriture` 
- les **constantes de classes** (voir tableau en fin de document)
- aucune classe métier n’est fournie (`Vache`, `VacheALait`, `PieNoire` sont à implémenter)

⚠️ **Gestion des erreurs :**
- toute violation des règles doit lever une **exception métier** `InvalidVacheException`
- l’usage de `assert` pour la logique métier est interdit

---

## 1) Diagramme de classes

Voir document accompagnant le sujet.
---

## 2) Données métier (attributs attendus)

### 2.1 Vache
- `petitNom: str` (identité métier)
- `age: int` (années)
- `poids: float` (kg)
- `panse: float` (kg)

### 2.2 VacheALait (en plus)
- `lait_disponible: float` (L)
- `lait_total_produit: float` (L)
- `lait_total_traite: float` (L)

### 2.3 PieNoire (en plus)
- `_ration: dict[TypeNourriture, float]`

---

## 3) Invariants (état toujours valide)

- `petitNom` non vide (pas seulement des espaces)
- `0 <= age <= AGE_MAX`
- `poids >= 0`
- `panse >= 0`
- `panse <= PANSE_MAX`
- si `POIDS_MAX` est utilisé : `poids <= POIDS_MAX`

Toute violation → `InvalidVacheException`.

---

## 4) Broutement

Une **seule méthode** `brouter(...)` simule une surcharge.

### 4.1 Broutement primaire (Vache et VacheALait)
- `brouter(quantite)`
- `quantite > 0`
- `panse += quantite`
- passage d’un type interdit → exception
- `panse` ne dépasse jamais `PANSE_MAX`

### 4.2 Broutement typé (PieNoire)
`PieNoire` accepte :
- `brouter(quantite)` (primaire)
- `brouter(quantite, type_nourriture)` (typé)
  - met à jour `_ration[type_nourriture] += quantite`

---

## 5) Rumination (Template Method + hooks)

`ruminer()` doit être **définie une seule fois** dans `Vache` (template method) et utiliser des hooks :
- `_calculer_lait(panse_avant) -> float`
- `_stocker_lait(lait) -> None`
- `_post_rumination(...) -> None`

Règles de rumination (communes) :
- interdit si `panse <= 0`
- `gain = RENDEMENT_RUMINATION * panse_avant`
- `poids += gain`
- `panse = 0`

---

## 6) Coefficients selon le type de nourriture (nutrition)

Une table de coefficients nutritionnels est fournie au niveau `PieNoire` :

```python
COEFFICIENT_NUTRITIONNEL: dict[TypeNourriture, float] = {
        TypeNourriture.MARGUERITE: 1.1,
        TypeNourriture.HERBE: 1.0,
        TypeNourriture.FOIN: 0.9,
        TypeNourriture.PAILLE: 0.4,
        TypeNourriture.CEREALES: 1.3,
    }
```

---

## 7) Production de lait

### 7.1 VacheALait
- `lait = RENDEMENT_LAIT * panse_avant`
- ajout à `lait_disponible` et `lait_total_produit`

### 7.2 PieNoire (si ration typée présente)
- `lait = RENDEMENT_LAIT * somme(quantite * coefficient_lait(type))`
- la ration typée est consommée après rumination

---

## 8) Fonctionnement de la rumination (Template Method)

La méthode `ruminer()` est une **Template Method** définie exclusivement dans la classe `Vache`.
Elle décrit le déroulement complet d’un cycle de rumination. Les sous-classes
(`VacheALait`, `PieNoire`) personnalisent uniquement certaines étapes via des **hooks protégés**.

### Étapes métier d’un cycle de rumination

1. Vérifier que la rumination est possible (`panse > 0`)
2. Mémoriser la panse avant rumination
3. Calculer et appliquer le gain de poids
4. Calculer la production de lait (*hook*)
5. Stocker le lait (*hook*)
6. Vider la panse
7. Exécuter un post-traitement éventuel (*hook*)
8. Retourner la quantité de lait produite

### Diagramme de séquence

Voir document acoompagnant le sujet.


> Règle de conception : `ruminer()` ne doit jamais être redéfinie dans les sous-classes.


## 9) Traite (VacheALait et PieNoire)

- `traire(litres) -> float`
- `litres > 0`
- `litres <= lait_disponible`
- `lait_disponible -= litres`

---


## 10) Tableau des constantes de classes (à utiliser obligatoirement)

| Catégorie de vache | Constante | Exemple de valeur | Rôle |
|---|---|---:|---|
| `Vache` | `AGE_MAX` | `25` | âge maximal autorisé (années) |
| `Vache` | `POIDS_MAX` | `1200.0` | poids maximal autorisé (kg) |
| `Vache` | `PANSE_MAX` | `200.0` | capacité maximale de panse (kg) |
| `Vache` | `RENDEMENT_RUMINATION` | `0.25` | proportion de panse convertie en poids (0 < α ≤ 1) |
| `Vache` | `COEFFICIENT_NUTRITIONNEL` | *(dict)* | coefficient nutritionnel par `TypeNourriture` |
| `VacheALait` | `RENDEMENT_LAIT` | `1.1` | litres produits par kg ruminé (λ) |
| `PieNoire` | `COEFFICIENT_LAIT_PAR_NOURRITURE` | *(dict)* | coefficient lait par `TypeNourriture` (μ) |

