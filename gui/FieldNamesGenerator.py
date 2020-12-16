from PyQt5.QtWidgets import QApplication
from gui.Wizard import Wizard
import sys


def generateFieldNames(path):
    app = QApplication(sys.argv)
    wizard = Wizard(database=None)
    with open(path, 'w') as file:
        for name in wizard.getFieldsNames():
            file.write(name + '\n')
    print(wizard.getFieldsNames())


if __name__ == "__main__":
    try:
        generateFieldNames('field_names.txt')
    except Exception as e:
        print("Cannot generate field names list: {}".format(e))
