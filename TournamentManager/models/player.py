import uuid


class Player:
    def __init__(self, last_name, first_name, date_of_birth, national_id, total_points=0):
        self.id = str(uuid.uuid4())
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.national_id = national_id
        self.total_points = total_points
        self.opponents = []

    def __lt__(self, other):
        return self.last_name.lower() < other.last_name.lower()

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.date_of_birth} {self.national_id}"

    def to_dict(self):
        # Convert Player object to dictionary
        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "national_id": self.national_id,
            "total_points": self.total_points,

        }

    @classmethod
    def from_dict(cls, data):
        # Create Player object from dictionary
        return cls(
            data.get("last_name", "Unknown"),
            data.get("first_name", "Unknown"),
            data.get("date_of_birth", "01/01/1900"),  # Fournissez une date par défaut ou gérez l'absence autrement
            data.get("national_id", "000000"),
            data.get("total_points", 0)
        )

    def add_opponent(self, opponent):
        # Ajoute un adversaire à la liste
        if opponent not in self.opponents:
            self.opponents.append(opponent)

    def has_played_against(self, opponent):
        # Vérifie si le joueur a déjà joué contre l'adversaire
        return opponent in self.opponents
