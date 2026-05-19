import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont, QFont
from PyQt5.QtCore import Qt, QPointF, QRectF

P = {
    "fondo_deep":   "#15132A",
    "fondo_panel":  "#1C1A2E",
    "fondo_sb":     "#211F35",
    "fondo_card":   "#2D2A50",
    "borde_sb":     "#2D2B45",
    "borde_normal": "#3D3B58",
    "violeta":      "#7C3AED",
    "violeta_med":  "#6D28D9",
    "lila":         "#A78BFA",
    "lila_claro":   "#C4B5FD",
    "texto_base":   "#E2E0F0",
    "texto_med":    "#8B87B8",
    "texto_apag":   "#6B6890",
    "nodo_normal":  "#211F35",
}

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None

class ArbolBST:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if not self.raiz:
            self.raiz = Nodo(valor)
            return [valor]
        camino = []
        self.raiz = self._insertar(self.raiz, valor, camino)
        return camino

    def _insertar(self, nodo, valor, camino):
        camino.append(nodo.valor)
        if valor < nodo.valor:
            if not nodo.izq:
                nodo.izq = Nodo(valor)
                camino.append(valor)
            else:
                nodo.izq = self._insertar(nodo.izq, valor, camino)
        elif valor > nodo.valor:
            if not nodo.der:
                nodo.der = Nodo(valor)
                camino.append(valor)
            else:
                nodo.der = self._insertar(nodo.der, valor, camino)
        return nodo

    def buscar(self, valor):
        camino = []
        nodo = self._buscar(self.raiz, valor, camino)
        return nodo, camino

    def _buscar(self, nodo, valor, camino):
        if not nodo:
            return None
        camino.append(nodo.valor)
        if valor == nodo.valor:
            return nodo
        elif valor < nodo.valor:
            return self._buscar(nodo.izq, valor, camino)
        else:
            return self._buscar(nodo.der, valor, camino)

    def eliminar(self, valor):
        self.raiz, ok = self._eliminar(self.raiz, valor)
        return ok

    def _eliminar(self, nodo, valor):
        if not nodo:
            return None, False
        if valor < nodo.valor:
            nodo.izq, ok = self._eliminar(nodo.izq, valor)
            return nodo, ok
        elif valor > nodo.valor:
            nodo.der, ok = self._eliminar(nodo.der, valor)
            return nodo, ok
        else:
            if not nodo.izq:
                return nodo.der, True
            if not nodo.der:
                return nodo.izq, True
            s = self._min(nodo.der)
            nodo.valor = s.valor
            nodo.der, _ = self._eliminar(nodo.der, s.valor)
            return nodo, True

    def _min(self, n):
        while n.izq:
            n = n.izq
        return n

    def limpiar(self):
        self.raiz = None

class CanvasArbol(QWidget):
    RADIO = 24
    GAP_V = 70
    INICIO_Y = 50

    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        self.setStyleSheet(f"background: {P['fondo_deep']};")
        self.arbol = None
        self.resaltados = []
        self.encontrado = None

    def actualizar(self, arbol, resaltados, encontrado):
        self.arbol = arbol
        self.resaltados = resaltados
        self.encontrado = encontrado
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if not self.arbol or not self.arbol.raiz:
            painter.setPen(QColor(P["texto_apag"]))
            painter.setFont(QFont("Segoe UI", 12))
            painter.drawText(self.rect(), Qt.AlignCenter, "Árbol vacío\nInserta un valor")
            return
        pos = self._calcular_posiciones()
        self._pintar_aristas(painter, self.arbol.raiz, pos)
        self._pintar_nodos(painter, pos)

    def _calcular_posiciones(self):
        niveles = {}
        self._recorrer_pos(self.arbol.raiz, 0, 0, niveles)
        if not niveles:
            return {}
        min_x = min(x for _, _, x, _ in niveles.values())
        max_x = max(x for _, _, x, _ in niveles.values())
        offset = (self.width() - (max_x - min_x)) / 2 - min_x
        pos = {}
        for nid, (n, y, x, _) in niveles.items():
            pos[nid] = (n.valor, x + offset, y)
        return pos

    def _recorrer_pos(self, nodo, prof, x, niveles):
        if not nodo:
            return
        niveles[id(nodo)] = (nodo, self.INICIO_Y + prof * self.GAP_V, x, prof)
        self._recorrer_pos(nodo.izq, prof + 1, x - 50 - prof * 10, niveles)
        self._recorrer_pos(nodo.der, prof + 1, x + 50 + prof * 10, niveles)

    def _pintar_aristas(self, painter, nodo, pos):
        if not nodo:
            return
        datos = pos.get(id(nodo))
        if not datos:
            return
        _, x1, y1 = datos
        for hijo in (nodo.izq, nodo.der):
            if hijo:
                datos_h = pos.get(id(hijo))
                if datos_h:
                    _, x2, y2 = datos_h
                    painter.setPen(QPen(QColor(P["borde_sb"]), 2))
                    ang = math.atan2(y2 - y1, x2 - x1)
                    r = self.RADIO
                    painter.drawLine(
                        QPointF(x1 + r * math.cos(ang), y1 + r * math.sin(ang)),
                        QPointF(x2 - r * math.cos(ang), y2 - r * math.sin(ang))
                    )
                    self._pintar_aristas(painter, hijo, pos)

    def _pintar_nodos(self, painter, pos):
        for nid, (valor, x, y) in pos.items():
            resalt = valor in self.resaltados
            encontrado = (valor == self.encontrado)
            color_fondo = QColor(P["violeta"]) if encontrado else (QColor(P["fondo_card"]) if resalt else QColor(P["nodo_normal"]))
            color_borde = QColor(P["lila"]) if encontrado or resalt else QColor(P["borde_normal"])
            color_texto = QColor(P["lila_claro"]) if encontrado else (QColor(P["lila"]) if resalt else QColor(P["texto_med"]))
            painter.setPen(QPen(color_borde, 1.5))
            painter.setBrush(QBrush(color_fondo))
            painter.drawEllipse(QPointF(x, y), self.RADIO, self.RADIO)
            painter.setPen(color_texto)
            painter.setFont(QFont("Segoe UI", 11))
            painter.drawText(QRectF(x - self.RADIO, y - self.RADIO, self.RADIO*2, self.RADIO*2), Qt.AlignCenter, str(valor))

class FlowTree(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FlowTree")
        self.setMinimumSize(980, 660)
        self.resize(1260, 740)

        self.arbol = ArbolBST()
        self.resaltados = []
        self.encontrado = None

        central = QWidget()
        central.setStyleSheet(f"background: {P['fondo_panel']};")
        self.setCentralWidget(central)

        raiz = QVBoxLayout(central)
        raiz.setContentsMargins(0, 0, 0, 0)
        raiz.setSpacing(0)
        raiz.addWidget(self._topbar())

        cuerpo = QHBoxLayout()
        cuerpo.setContentsMargins(0, 0, 0, 0)
        cuerpo.setSpacing(0)

        self.canvas = CanvasArbol()
        cuerpo.addWidget(self.canvas, 1)
        cuerpo.addWidget(self._sidebar())

        raiz.addLayout(cuerpo)
        self.showMaximized()
        self._redibujar()

    def _topbar(self):
        bar = QFrame()
        bar.setFixedHeight(52)
        bar.setStyleSheet(f"background: {P['fondo_panel']}; border-bottom: 1px solid {P['borde_sb']};")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.addWidget(QLabel("🌿"))
        titulo = QLabel("FlowTree")
        titulo.setStyleSheet(f"color: {P['texto_base']}; font-size: 15px; font-weight: 600;")
        layout.addWidget(titulo)
        layout.addStretch()
        badge = QLabel("PyQt5 Usuario")
        badge.setStyleSheet(f"background: {P['fondo_sb']}; color: {P['texto_apag']}; font-size: 10px; padding: 4px 12px; border-radius: 16px;")
        layout.addWidget(badge)
        return bar

    def _sidebar(self):
        contenedor = QFrame()
        contenedor.setFixedWidth(210)
        contenedor.setStyleSheet(f"background: {P['fondo_sb']}; border-left: 1px solid {P['borde_sb']};")
        layout = QVBoxLayout(contenedor)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(12)

        lbl_ins = QLabel("INSERTAR NODO")
        lbl_ins.setStyleSheet(f"color: {P['texto_apag']}; font-size: 10px;")
        self.ent_insertar = QLineEdit()
        self.ent_insertar.setPlaceholderText("Valor entero...")
        self.ent_insertar.returnPressed.connect(self._insertar)
        self.ent_insertar.setStyleSheet(f"background: {P['borde_sb']}; border-radius: 6px; padding: 6px; color: white;")
        btn_insertar = QPushButton("Insertar")
        btn_insertar.clicked.connect(self._insertar)

        lbl_be = QLabel("BUSCAR / ELIMINAR")
        lbl_be.setStyleSheet(f"color: {P['texto_apag']}; font-size: 10px; margin-top: 10px;")
        self.ent_buscar = QLineEdit()
        self.ent_buscar.setPlaceholderText("Valor...")
        self.ent_buscar.setStyleSheet(f"background: {P['borde_sb']}; border-radius: 6px; padding: 6px; color: white;")
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self._buscar)
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self._eliminar)

        for btn in (btn_insertar, btn_buscar, btn_eliminar):
            btn.setStyleSheet(f"background: {P['violeta']}; color: white; border: none; border-radius: 6px; padding: 8px; font-weight: bold;")
            btn.setStyleSheet(btn.styleSheet() + f"QPushButton:hover {{ background: {P['violeta_med']}; }}")

        layout.addWidget(lbl_ins)
        layout.addWidget(self.ent_insertar)
        layout.addWidget(btn_insertar)
        layout.addWidget(lbl_be)
        layout.addWidget(self.ent_buscar)
        layout.addWidget(btn_buscar)
        layout.addWidget(btn_eliminar)
        layout.addStretch()
        return contenedor

    def _insertar(self):
        try:
            valor = int(self.ent_insertar.text())
        except:
            QMessageBox.warning(self, "Error", "Valor entero válido")
            return
        camino = self.arbol.insertar(valor)
        self.ent_insertar.clear()
        self.resaltados = camino
        self.encontrado = valor
        self._redibujar()

    def _buscar(self):
        try:
            valor = int(self.ent_buscar.text())
        except:
            QMessageBox.warning(self, "Error", "Valor entero válido")
            return
        nodo, camino = self.arbol.buscar(valor)
        self.resaltados = camino
        self.encontrado = valor if nodo else None
        self._redibujar()

    def _eliminar(self):
        try:
            valor = int(self.ent_buscar.text())
        except:
            QMessageBox.warning(self, "Error", "Valor entero válido")
            return
        ok = self.arbol.eliminar(valor)
        self.ent_buscar.clear()
        self.resaltados = []
        self.encontrado = None
        self._redibujar()
        QMessageBox.information(self, "Eliminar", f"Eliminado: {ok}")

    def _redibujar(self):
        self.canvas.actualizar(self.arbol, self.resaltados, self.encontrado)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    QApplication.setFont(QFont("Segoe UI", 10))
    ventana = FlowTree()
    ventana.show()
    sys.exit(app.exec_())