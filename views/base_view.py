
class BaseView:

    def display_feedback(self, message_type, error_message=None):
        if message_type == "invalid_option":
            print("❌ Option non valide. Veuillez réessayer")
        elif message_type == "invalid_selection":
            print("❌ Sélection invalide. Veuillez réessayer.")
        elif message_type == "operation_cancelled":
            print("⚠️  Operation annulée. Retour au menu précédent.")
        elif message_type == "invalid_player_data" and error_message:
            print(f"❌ Erreur dans les données du joueur : {error_message}")
        elif message_type == "database_io_error" and error_message:
            print(f"❌ Erreur d'accès à la base de données : {error_message}")
        elif message_type == "no_players_selected":
            print("⚠️ Aucun joueur sélectionné.")
        elif message_type == "empty_field":
            print("❌ Le champ ne doit pas être vide.")


