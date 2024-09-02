
class BaseView:

    def display_message(self, message_type, tournament=None):
        if message_type == "invalid_option":
            print("❌ Option non valide. Veuillez réessayer")
        elif message_type == "invalid_selection":
            print("❌ Sélection invalide. Veuillez réessayer.")
