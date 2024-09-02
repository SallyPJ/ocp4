
class BaseView:

    def display_message(self, message_type):
        if message_type == "invalid_option":
            print(f"❌ Option non valide. Veuillez réessayer")
        elif message_type == "invalid_selection":
            print(f"❌ Sélection invalide. Veuillez réessayer.")