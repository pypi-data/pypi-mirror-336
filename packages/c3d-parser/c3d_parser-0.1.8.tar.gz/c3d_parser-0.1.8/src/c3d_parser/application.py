
import sys

from PySide6.QtWidgets import QApplication

from c3d_parser.view.main_window import MainWindow


# TODO: Britney is having issues with Qt...
#   Suggests the following code to avoid manual env-var setting.
# import PySide6
#
# dirname = os.path.dirname(PySide6.__file__)
# plugin_path = os.path.join(dirname, 'plugins', 'platforms')
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
#
# from PySide6.QtWidgets import QApplication

# TODO: This code is in the MAP-Client.
#   Not sure if it might be related to solving the issue above...?
# os.environ['ETS_TOOLKIT'] = 'qt'


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Auckland Bioengineering Institute")
    app.setApplicationName("C3D Parser")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
