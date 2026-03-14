def main():
    import sys

    from PySide6.QtGui import QGuiApplication
    from PySide6.QtWidgets import QApplication

    from ui.MainMenuWindow import MainMenuWindow

    app = QApplication(sys.argv)
    app.setApplicationName("AoC3TechnologiesEditor")
    app.setOrganizationName("Ariesviel's Editor")

    screen = QGuiApplication.primaryScreen()
    screen_size = screen.size()

    mainMenu = MainMenuWindow(screen_size)

    mainMenu.show()

    app.exec()

if __name__ == "__main__":
    main()