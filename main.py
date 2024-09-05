
from controllers.main_controller import MainController


def main():
    try:
        controller = MainController()
        controller.run_main_menu()
    except KeyboardInterrupt:
        print("\nFermeture de l'application...")


if __name__ == "__main__":
    main()
