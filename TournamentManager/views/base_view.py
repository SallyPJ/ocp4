
class BaseView:

    def display_feedback(self, message_type, tournament=None):
        if message_type == "invalid_option":
            print("❌ Option non valide. Veuillez réessayer")
        elif message_type == "invalid_selection":
            print("❌ Sélection invalide. Veuillez réessayer.")
        elif message_type == "operation_cancelled":
            print("⚠️  Operation annulée. Retour au menu précédent.")
        elif message_type == "no_players_selected":
            print("⚠️ Aucun joueur sélectionné.")
