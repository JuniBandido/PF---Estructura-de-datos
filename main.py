import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QLabel, QPushButton, QLineEdit, QFrame)
from PyQt5.QtCore import Qt

class CanvasPlaceholder(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: #15132A;")
        self.label = QLabel("Árbol vacío\n(Los botones aún no insertan nodos reales)", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #6B6890; font-size: 14px;")

    def resizeEvent(self, event):
        self.label.resize(self.size())
        super().resizeEvent(event)

class FlowTreeV2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FlowTree v2 - Esqueleto de operaciones")
        self.setMinimumSize(900, 600)

        central = QWidget()
        central.setStyleSheet("background: #1C1A2E;")
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.canvas = CanvasPlaceholder()
        main_layout.addWidget(self.canvas, 1)

        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("background: #211F35; border-left: 1px solid #2D2B45;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 20, 12, 20)
        sidebar_layout.setSpacing(12)

        lbl_ins = QLabel("INSERTAR NODO")
        lbl_ins.setStyleSheet("color: #8B87B8; font-size: 10px;")
        self.ent_insertar = QLineEdit()
        self.ent_insertar.setPlaceholderText("Valor entero...")
        self.ent_insertar.setStyleSheet("background: #2D2B45; border-radius: 6px; padding: 6px;")
        btn_insertar = QPushButton("Insertar")
        btn_insertar.clicked.connect(self.mock_insertar)

        lbl_be = QLabel("BUSCAR / ELIMINAR")
        lbl_be.setStyleSheet("color: #8B87B8; font-size: 10px; margin-top: 10px;")
        self.ent_buscar = QLineEdit()
        self.ent_buscar.setPlaceholderText("Valor...")
        self.ent_buscar.setStyleSheet("background: #2D2B45; border-radius: 6px; padding: 6px;")
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.mock_buscar)
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self.mock_eliminar)

        for btn in (btn_insertar, btn_buscar, btn_eliminar):
            btn.setStyleSheet("""
                QPushButton {
                    background: #7C3AED; color: white; border: none;
                    border-radius: 6px; padding: 8px; font-weight: bold;
                }
                QPushButton:hover { background: #6D28D9; }
            """)

        sidebar_layout.addWidget(lbl_ins)
        sidebar_layout.addWidget(self.ent_insertar)
        sidebar_layout.addWidget(btn_insertar)
        sidebar_layout.addWidget(lbl_be)
        sidebar_layout.addWidget(self.ent_buscar)
        sidebar_layout.addWidget(btn_buscar)
        sidebar_layout.addWidget(btn_eliminar)
        sidebar_layout.addStretch()

        main_layout.addWidget(sidebar)

    def mock_insertar(self):
        print("Mock: insertar", self.ent_insertar.text())
        self.ent_insertar.clear()

    def mock_buscar(self):
        print("Mock: buscar", self.ent_buscar.text())

    def mock_eliminar(self):
        print("Mock: eliminar", self.ent_buscar.text())
        self.ent_buscar.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ventana = FlowTreeV2()
    ventana.show()
    sys.exit(app.exec_())