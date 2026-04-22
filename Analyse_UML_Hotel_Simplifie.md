# Analyse UML — Gestion d'Hôtel (Version Simplifiée)

---

## 1. Diagramme de Cas d'Utilisation

| Acteur | Cas d'utilisation |
|--------|------------------|
| **Visiteur** | Consulter les hôtels · Consulter les chambres · Voir les prix · S'inscrire |
| **Client** *(hérite du Visiteur)* | Se connecter · Rechercher un hôtel · Réserver une chambre · Effectuer un paiement · Annuler une réservation |
| **Administrateur** | Gérer les hôtels · Gérer les chambres · Gérer les réservations · Gérer les utilisateurs |

```mermaid
graph LR
    V((Visiteur)) --- UC1(Consulter les hôtels)
    V --- UC2(S'inscrire)
    V -->|hérite| C((Client))
    C --- UC3(Se connecter)
    C --- UC4(Rechercher un hôtel)
    C --- UC5(Réserver une chambre)
    C --- UC6(Effectuer un paiement)
    A((Administrateur)) --- UC7(Gérer les hôtels)
    A --- UC8(Gérer les réservations)
    A --- UC9(Gérer les utilisateurs)
```

---

## 2. Descriptions Textuelles

### CU1 — S'inscrire
| | |
|---|---|
| **Acteur** | Visiteur |
| **Pré-condition** | Utilisateur non inscrit |
| **Post-condition** | Compte client créé |

1. Cliquer sur « S'inscrire » → formulaire affiché
2. Remplir (nom, email, mot de passe, téléphone)
3. Système vérifie les données → compte créé → redirection connexion

**Alternative :** Email existant → erreur affichée

---

### CU2 — Rechercher un hôtel
| | |
|---|---|
| **Acteur** | Visiteur / Client |
| **Pré-condition** | Hôtels enregistrés dans le système |
| **Post-condition** | Liste d'hôtels affichée |

1. Saisir ville + dates → cliquer « Rechercher »
2. Système retourne la liste des hôtels disponibles
3. Sélectionner un hôtel → voir les détails

**Alternative :** Aucun résultat → message d'erreur

---

### CU3 — Réserver une chambre
| | |
|---|---|
| **Acteur** | Client |
| **Pré-condition** | Client connecté, chambre sélectionnée |
| **Post-condition** | Réservation créée (En attente de paiement) |

1. Cliquer « Réserver » → système vérifie disponibilité
2. Afficher récapitulatif → client confirme
3. Réservation enregistrée → redirection paiement

**Alternative :** Chambre indisponible → autres chambres proposées

---

### CU4 — Effectuer un paiement
| | |
|---|---|
| **Acteur** | Client |
| **Pré-condition** | Réservation en attente de paiement |
| **Post-condition** | Réservation confirmée, client notifié |

1. Choisir mode : Carte bancaire ou Mobile Money
2. Saisir informations → système valide la transaction
3. Réservation → « Confirmée » + envoi confirmation

**Alternative :** Paiement refusé → message d'erreur, réessayer

---

## 3. Diagrammes de Séquences

### DS1 — S'inscrire
```mermaid
sequenceDiagram
    actor V as Visiteur
    participant S as Système
    participant BD as Base de données
    V->>S: Cliquer S'inscrire
    S-->>V: Afficher formulaire
    V->>S: Soumettre données
    S->>BD: Vérifier email
    alt Email existant
        BD-->>S: Trouvé
        S-->>V: Erreur email
    else Disponible
        BD-->>S: OK
        S->>BD: Créer compte
        S-->>V: Redirection connexion
    end
```

### DS2 — Rechercher un hôtel
```mermaid
sequenceDiagram
    actor U as Utilisateur
    participant S as Système
    participant BD as Base de données
    U->>S: Saisir ville + dates
    S->>BD: Requête hôtels disponibles
    alt Aucun résultat
        BD-->>S: Liste vide
        S-->>U: Aucun hôtel trouvé
    else Résultats
        BD-->>S: Liste hôtels
        S-->>U: Afficher hôtels
        U->>S: Sélectionner hôtel
        S-->>U: Afficher détails
    end
```

### DS3 — Réserver une chambre
```mermaid
sequenceDiagram
    actor C as Client
    participant S as Système
    participant BD as Base de données
    C->>S: Cliquer Réserver
    S->>BD: Vérifier disponibilité
    alt Indisponible
        BD-->>S: Indisponible
        S-->>C: Autres chambres
    else Disponible
        BD-->>S: OK
        S-->>C: Récapitulatif
        C->>S: Confirmer
        S->>BD: Enregistrer réservation
        S-->>C: Redirection paiement
    end
```

### DS4 — Effectuer un paiement
```mermaid
sequenceDiagram
    actor C as Client
    participant S as Système
    participant P as Passerelle
    participant BD as Base de données
    S-->>C: Afficher modes de paiement
    C->>S: Choisir mode + infos
    S->>P: Traiter paiement
    alt Refusé
        P-->>S: Refusé
        S-->>C: Erreur paiement
    else Accepté
        P-->>S: Accepté
        S->>BD: Confirmer réservation
        S-->>C: Confirmation envoyée
    end
```

---

## 4. Diagrammes d'Activités

### DA1 — S'inscrire
```mermaid
flowchart LR
    A([Début]) --> B[Remplir formulaire]
    B --> C{Valide ?}
    C -- Non --> B
    C -- Oui --> D{Email existant ?}
    D -- Oui --> B
    D -- Non --> E[Créer compte]
    E --> F([Fin])
```

### DA2 — Rechercher un hôtel
```mermaid
flowchart LR
    A([Début]) --> B[Saisir ville + dates]
    B --> C{Résultats ?}
    C -- Non --> B
    C -- Oui --> D[Afficher hôtels]
    D --> E[Sélectionner hôtel]
    E --> F([Fin])
```

### DA3 — Réserver une chambre
```mermaid
flowchart LR
    A([Début]) --> B[Choisir chambre]
    B --> C{Connecté ?}
    C -- Non --> G[Se connecter] --> B
    C -- Oui --> D{Disponible ?}
    D -- Non --> B
    D -- Oui --> E[Confirmer réservation]
    E --> F([Fin])
```

### DA4 — Effectuer un paiement
```mermaid
flowchart LR
    A([Début]) --> B[Choisir mode paiement]
    B --> C[Saisir informations]
    C --> D{Validé ?}
    D -- Non --> B
    D -- Oui --> E[Confirmer réservation]
    E --> F[Envoyer confirmation]
    F --> G([Fin])
```

---

## 5. Diagramme de Classes

```mermaid
classDiagram
    class Utilisateur {
        +id : int
        +nom : String
        +email : String
        +motDePasse : String
        +telephone : String
        +seConnecter()
        +sInscrire()
    }
    class Client {
        +adresse : String
        +reserver()
        +payer()
    }
    class Administrateur {
        +gererHotels()
        +gererReservations()
    }
    class Hotel {
        +id : int
        +nom : String
        +ville : String
        +nbEtoiles : int
    }
    class Chambre {
        +id : int
        +type : String
        +prix : float
        +statut : String
        +verifierDispo()
    }
    class Reservation {
        +id : int
        +dateArrivee : Date
        +dateDepart : Date
        +prixTotal : float
        +statut : String
    }
    class Paiement {
        +id : int
        +montant : float
        +mode : String
        +statut : String
        +traiter()
    }
    Utilisateur <|-- Client
    Utilisateur <|-- Administrateur
    Client "1" --> "0..*" Reservation
    Reservation "1" --> "1" Chambre
    Chambre "1..*" --> "1" Hotel
    Reservation "1" --> "1" Paiement
```

---

## 6. Dictionnaire de Données

### `utilisateur`
| Champ | Type | Description |
|-------|------|-------------|
| id | INT (PK) | Identifiant unique |
| nom | VARCHAR(50) | Nom |
| email | VARCHAR(100) | Email unique |
| mot_de_passe | VARCHAR(255) | Mot de passe haché |
| telephone | VARCHAR(20) | Téléphone |
| role | ENUM(client, admin) | Rôle |

### `hotel`
| Champ | Type | Description |
|-------|------|-------------|
| id | INT (PK) | Identifiant unique |
| nom | VARCHAR(100) | Nom de l'hôtel |
| ville | VARCHAR(100) | Ville |
| nb_etoiles | TINYINT | Classement 1-5 |

### `chambre`
| Champ | Type | Description |
|-------|------|-------------|
| id | INT (PK) | Identifiant unique |
| id_hotel | INT (FK) | Hôtel parent |
| type | VARCHAR(50) | Simple / Double / Suite |
| prix_par_nuit | DECIMAL | Prix par nuit |
| statut | ENUM | disponible / occupée |

### `reservation`
| Champ | Type | Description |
|-------|------|-------------|
| id | INT (PK) | Identifiant unique |
| id_client | INT (FK) | Client |
| id_chambre | INT (FK) | Chambre réservée |
| date_arrivee | DATE | Arrivée |
| date_depart | DATE | Départ |
| prix_total | DECIMAL | Total |
| statut | ENUM | en_attente / confirmée / annulée |

### `paiement`
| Champ | Type | Description |
|-------|------|-------------|
| id | INT (PK) | Identifiant unique |
| id_reservation | INT (FK) | Réservation |
| montant | DECIMAL | Montant payé |
| mode | ENUM | carte / mobile_money |
| statut | ENUM | en_attente / validé / refusé |
| date_paiement | DATETIME | Date du paiement |
