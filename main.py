#Principal

import sys
from PyQt5.QtWidgets import QApplication
from ui import FlowTree

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ventana = FlowTree()
    ventana.show()
    sys.exit(app.exec_())