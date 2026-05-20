import sys
import math
import json
from collections import deque
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QLabel, QPushButton, QLineEdit, QScrollArea, QFrame,QFileDialog, QMessageBox, QSizePolicy)
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, QPointF, QRectF

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
        self.altura = 1

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if not self.raiz:
            self.raiz = Nodo(valor)
            return []
        cola = deque([self.raiz])
        while cola:
            n = cola.popleft()
            if not n.izq:
                n.izq = Nodo(valor)
                return []
            cola.append(n.izq)
            if not n.der:
                n.der = Nodo(valor)
                return []
            cola.append(n.der)

    def buscar(self, valor, nodo=None, primero=True):
        if primero:
            nodo = self.raiz
        if not nodo:
            return None, []
        if nodo.valor == valor:
            return nodo, [nodo.valor]
        izq, pi = self.buscar(valor, nodo.izq, False)
        if izq:
            return izq, [nodo.valor] + pi
        der, pd = self.buscar(valor, nodo.der, False)
        if der:
            return der, [nodo.valor] + pd
        return None, [nodo.valor]

    def eliminar(self, valor):
        self.raiz, ok = self._eliminar(self.raiz, valor)
        return ok

    def _eliminar(self, nodo, valor):
        if not nodo:
            return None, False
        if nodo.valor == valor:
            if not nodo.izq and not nodo.der:
                return None, True
            if not nodo.izq:
                return nodo.der, True
            if not nodo.der:
                return nodo.izq, True
            s = self._minimo(nodo.der)
            nodo.valor = s.valor
            nodo.der, _ = self._eliminar(nodo.der, s.valor)
            return nodo, True
        nodo.izq, di = self._eliminar(nodo.izq, valor)
        if di:
            return nodo, True
        nodo.der, dd = self._eliminar(nodo.der, valor)
        return nodo, dd

    def _minimo(self, n):
        while n.izq:
            n = n.izq
        return n

    def preorden(self, n=None, p=True):
        if p:
            n = self.raiz
        if not n:
            return []
        return [n.valor] + self.preorden(n.izq, False) + self.preorden(n.der, False)

    def inorden(self, n=None, p=True):
        if p:
            n = self.raiz
        if not n:
            return []
        return self.inorden(n.izq, False) + [n.valor] + self.inorden(n.der, False)

    def postorden(self, n=None, p=True):
        if p:
            n = self.raiz
        if not n:
            return []
        return self.postorden(n.izq, False) + self.postorden(n.der, False) + [n.valor]

    def altura(self, n=None, p=True):
        if p:
            n = self.raiz
        if not n:
            return 0
        return 1 + max(self.altura(n.izq, False), self.altura(n.der, False))

    def total(self, n=None, p=True):
        if p:
            n = self.raiz
        if not n:
            return 0
        return 1 + self.total(n.izq, False) + self.total(n.der, False)

    def a_lista(self, n=None, p=True):
        if p:
            n = self.raiz
        if not n:
            return []
        return [n.valor] + self.a_lista(n.izq, False) + self.a_lista(n.der, False)

    def limpiar(self):
        self.raiz = None

class ArbolBST(ArbolBinario):
    def insertar(self, valor):
        self.raiz, camino = self._insertar(self.raiz, valor, [])
        return camino

    def _insertar(self, nodo, valor, camino):
        if not nodo:
            camino.append(valor)
            return Nodo(valor), camino
        camino.append(nodo.valor)
        if valor < nodo.valor:
            nodo.izq, camino = self._insertar(nodo.izq, valor, camino)
        elif valor > nodo.valor:
            nodo.der, camino = self._insertar(nodo.der, valor, camino)
        return nodo, camino

    def buscar(self, valor, nodo=None, p=True):
        if p:
            nodo = self.raiz
        if not nodo:
            return None, []
        if nodo.valor == valor:
            return nodo, [nodo.valor]
        if valor < nodo.valor:
            n, c = self.buscar(valor, nodo.izq, False)
        else:
            n, c = self.buscar(valor, nodo.der, False)
        return n, [nodo.valor] + c

    def eliminar(self, valor):
        self.raiz, ok = self._elim(self.raiz, valor)
        return ok

    def _elim(self, nodo, valor):
        if not nodo:
            return None, False
        if valor < nodo.valor:
            nodo.izq, d = self._elim(nodo.izq, valor)
            return nodo, d
        if valor > nodo.valor:
            nodo.der, d = self._elim(nodo.der, valor)
            return nodo, d
        if not nodo.izq and not nodo.der:
            return None, True
        if not nodo.izq:
            return nodo.der, True
        if not nodo.der:
            return nodo.izq, True
        s = self._minimo(nodo.der)
        nodo.valor = s.valor
        nodo.der, _ = self._elim(nodo.der, s.valor)
        return nodo, True

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def _h(self, n):
        return n.altura if n else 0

    def _bf(self, n):
        return self._h(n.izq) - self._h(n.der) if n else 0

    def _act(self, n):
        if n:
            n.altura = 1 + max(self._h(n.izq), self._h(n.der))

    def _rot_der(self, y):
        x = y.izq
        T = x.der
        x.der = y
        y.izq = T
        self._act(y)
        self._act(x)
        return x

    def _rot_izq(self, x):
        y = x.der
        T = y.izq
        y.izq = x
        x.der = T
        self._act(x)
        self._act(y)
        return y

    def _bal(self, n):
        self._act(n)
        bf = self._bf(n)
        if bf > 1:
            if self._bf(n.izq) < 0:
                n.izq = self._rot_izq(n.izq)
            return self._rot_der(n)
        if bf < -1:
            if self._bf(n.der) > 0:
                n.der = self._rot_der(n.der)
            return self._rot_izq(n)
        return n

    def insertar(self, valor):
        self.raiz, camino = self._insertar(self.raiz, valor, [])
        return camino

    def _insertar(self, nodo, valor, camino):
        if not nodo:
            camino.append(valor)
            return Nodo(valor), camino
        camino.append(nodo.valor)
        if valor < nodo.valor:
            nodo.izq, camino = self._insertar(nodo.izq, valor, camino)
        elif valor > nodo.valor:
            nodo.der, camino = self._insertar(nodo.der, valor, camino)
        else:
            return nodo, camino
        return self._bal(nodo), camino

    def buscar(self, valor, nodo=None, p=True):
        if p:
            nodo = self.raiz
        if not nodo:
            return None, []
        if nodo.valor == valor:
            return nodo, [nodo.valor]
        if valor < nodo.valor:
            n, c = self.buscar(valor, nodo.izq, False)
        else:
            n, c = self.buscar(valor, nodo.der, False)
        return n, [nodo.valor] + c

    def eliminar(self, valor):
        self.raiz, ok = self._elim(self.raiz, valor)
        return ok

    def _elim(self, nodo, valor):
        if not nodo:
            return None, False
        if valor < nodo.valor:
            nodo.izq, d = self._elim(nodo.izq, valor)
            return self._bal(nodo), d
        if valor > nodo.valor:
            nodo.der, d = self._elim(nodo.der, valor)
            return self._bal(nodo), d
        if not nodo.izq and not nodo.der:
            return None, True
        if not nodo.izq:
            return nodo.der, True
        if not nodo.der:
            return nodo.izq, True
        s = self._minimo(nodo.der)
        nodo.valor = s.valor
        nodo.der, _ = self._elim(nodo.der, s.valor)
        return self._bal(nodo), True

    def _minimo(self, n):
        while n.izq:
            n = n.izq
        return n

    def preorden(self, n=None, p=True):
        if p:
            n = self.raiz
        if not n:
            return []
        return [n.valor] + self.preorden(n.izq, False) + self.preorden(n.der, False)

    def inorden(self, n=None, p=True):
        if p:
            n = self.raiz
        if not n:
            return []
        return self.inorden(n.izq, False) + [n.valor] + self.inorden(n.der, False)

    def postorden(self, n=None, p=True):
        if p:
            n = self.raiz
        if not n:
            return []
        return self.postorden(n.izq, False) + self.postorden(n.der, False) + [n.valor]

    def altura(self, n=None, p=True):
        if p:
            return self._h(self.raiz)
        return self._h(n)

    def total(self, n=None, p=True):
        if p:
            n = self.raiz
        if not n:
            return 0
        return 1 + self.total(n.izq, False) + self.total(n.der, False)

    def a_lista(self, n=None, p=True):
        if p:
            n = self.raiz
        if not n:
            return []
        return [n.valor] + self.a_lista(n.izq, False) + self.a_lista(n.der, False)

    def limpiar(self):
        self.raiz = None

class CanvasArbol(QWidget):
    RADIO = 24
    RADIO_HJ = 20
    GAP_V = 82
    MARGEN = 56
    INICIO_Y = 52

    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet(f"background: {P['fondo_deep']};")
        self.arbol = None
        self.resaltados = []
        self.encontrado = None

    def actualizar(self, arbol, resaltados, encontrado):
        self.arbol = arbol
        self.resaltados = resaltados or []
        self.encontrado = encontrado
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if not self.arbol or not self.arbol.raiz:
            self._pintar_vacio(painter)
            return
        pos = self._calcular()
        self._pintar_aristas(painter, self.arbol.raiz, pos)
        self._pintar_nodos(painter, pos)

    def _pintar_vacio(self, p):
        p.setPen(QColor(P["texto_apag"]))
        p.setFont(QFont("Segoe UI", 12))
        p.drawText(self.rect(), Qt.AlignCenter, "Árbol vacío\nInserta un valor")

    def _calcular(self):
        SEP = self.RADIO * 2 + 24
        col = [0]
        def asignar_col(n):
            if not n: return
            asignar_col(n.izq)
            n._col = float(col[0])
            col[0] += 1
            asignar_col(n.der)
        asignar_col(self.arbol.raiz)

        def centrar(n):
            if not n: return
            centrar(n.izq)
            centrar(n.der)
            if n.izq and n.der:
                n._col = (n.izq._col + n.der._col) / 2.0
            elif n.izq:
                n._col = n.izq._col - 0.5
                n.izq._col = n._col - 0.5
            elif n.der:
                n._col = n.der._col - 0.5
                n.der._col = n._col + 0.5
        centrar(self.arbol.raiz)

        niveles = []
        def recoger(n, prof):
            if not n: return
            niveles.append((n, prof))
            recoger(n.izq, prof+1)
            recoger(n.der, prof+1)
        recoger(self.arbol.raiz, 0)

        min_col = min(n._col for n, _ in niveles)
        for n, _ in niveles:
            n._col -= min_col

        cx = self.width() / 2.0
        rc = self.arbol.raiz._col
        pos = {}
        for n, prof in niveles:
            px = cx + (n._col - rc) * SEP
            py = self.INICIO_Y + prof * self.GAP_V
            pos[id(n)] = (n.valor, px, py)
        return pos

    def _pintar_aristas(self, painter, nodo, pos):
        if not nodo: return
        datos = pos.get(id(nodo))
        if not datos: return
        _, x1, y1 = datos
        for hijo in (nodo.izq, nodo.der):
            if hijo:
                hdat = pos.get(id(hijo))
                if hdat:
                    _, x2, y2 = hdat
                    resalt = nodo.valor in self.resaltados and hijo.valor in self.resaltados
                    color = QColor(P["violeta"]) if resalt else QColor(P["borde_sb"])
                    grosor = 2.2 if resalt else 1.4
                    ang = math.atan2(y2 - y1, x2 - x1)
                    R = self.RADIO
                    painter.setPen(QPen(color, grosor, Qt.SolidLine, Qt.RoundCap))
                    painter.drawLine(
                        QPointF(x1 + R * math.cos(ang), y1 + R * math.sin(ang)),
                        QPointF(x2 - R * math.cos(ang), y2 - R * math.sin(ang))
                    )
                    self._pintar_aristas(painter, hijo, pos)

    def _pintar_nodos(self, painter, pos):
        for nid, (valor, x, y) in pos.items():
            resalt = valor in self.resaltados
            encontrado = (valor == self.encontrado)
            nodo_real = self._buscar_nodo_por_id(self.arbol.raiz, nid)
            es_hoja = nodo_real and not nodo_real.izq and not nodo_real.der
            if encontrado:
                relleno = QColor(P["violeta"])
                borde = QColor(P["lila"])
                txt = QColor(P["lila_claro"])
                grosor = 2.5
                R = self.RADIO
            elif resalt:
                relleno = QColor(P["fondo_card"])
                borde = QColor(P["violeta"])
                txt = QColor(P["lila"])
                grosor = 2.0
                R = self.RADIO
            else:
                relleno = QColor(P["nodo_normal"])
                borde = QColor(P["borde_normal"])
                txt = QColor(P["texto_med"])
                grosor = 1.5
                R = self.RADIO_HJ if es_hoja else self.RADIO
            if resalt or encontrado:
                glow = QColor(P["violeta"])
                glow.setAlpha(30)
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(glow))
                painter.drawEllipse(QPointF(x, y), R + 7, R + 7)
            painter.setPen(QPen(borde, grosor))
            painter.setBrush(QBrush(relleno))
            painter.drawEllipse(QPointF(x, y), R, R)
            painter.setPen(txt)
            painter.setFont(QFont("Segoe UI", 11, QFont.Medium))
            painter.drawText(QRectF(x - R, y - R, R*2, R*2), Qt.AlignCenter, str(valor))
            if isinstance(self.arbol, ArbolAVL) and nodo_real:
                bf = self.arbol._bf(nodo_real)
                painter.setPen(QColor(P["lila"]) if abs(bf)>1 else QColor(P["texto_apag"]))
                painter.setFont(QFont("Segoe UI", 7))
                painter.drawText(int(x + R + 4), int(y - R + 10), f"bf{bf:+d}")

    def _buscar_nodo_por_id(self, nodo, nid):
        if not nodo: return None
        if id(nodo) == nid: return nodo
        izq = self._buscar_nodo_por_id(nodo.izq, nid)
        if izq: return izq
        return self._buscar_nodo_por_id(nodo.der, nid)

class SelectorTipo(QWidget):
    OPCIONES = [("Binario", "Por nivel"), ("BST", "Búsqueda"), ("AVL", "Balanceado")]
    def __init__(self, al_cambiar):
        super().__init__()
        self.seleccion = "BST"
        self.al_cambiar = al_cambiar
        self.chips = {}
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(4)
        for nombre, desc in self.OPCIONES:
            chip = self._hacer_chip(nombre)
            layout.addWidget(chip)
            self.chips[nombre] = chip
        self._refrescar()

    def _hacer_chip(self, nombre):
        chip = QFrame()
        chip.setCursor(Qt.PointingHandCursor)
        chip.setFixedHeight(34)
        layout = QHBoxLayout(chip)
        layout.setContentsMargins(10,0,10,0)
        layout.setSpacing(6)
        dot = QLabel()
        dot.setFixedSize(8,8)
        lbl = QLabel(nombre)
        layout.addWidget(dot)
        layout.addWidget(lbl)
        chip.mousePressEvent = lambda e, n=nombre: self._seleccionar(n)
        return chip

    def _seleccionar(self, nombre):
        self.seleccion = nombre
        self._refrescar()
        self.al_cambiar()

    def _refrescar(self):
        for nombre, chip in self.chips.items():
            activo = nombre == self.seleccion
            dot = chip.findChild(QLabel)
            lbl = chip.findChildren(QLabel)[1]
            if activo:
                chip.setStyleSheet(f"background: {P['fondo_card']}; border: 1px solid {P['violeta']}; border-radius: 7px;")
                dot.setStyleSheet(f"background: {P['violeta']}; border-radius: 4px;")
                lbl.setStyleSheet(f"font-size: 11px; font-weight: 500; color: {P['lila']};")
            else:
                chip.setStyleSheet(f"background: transparent; border: 1px solid {P['borde_sb']}; border-radius: 7px;")
                dot.setStyleSheet(f"background: transparent; border: 1.5px solid {P['texto_apag']}; border-radius: 4px;")
                lbl.setStyleSheet(f"font-size: 11px; font-weight: 500; color: {P['texto_med']};")

class FlowTree(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FlowTree")
        self.setMinimumSize(1000, 700)
        self.resize(1280, 780)

        self.arbol = ArbolBST()
        self.resaltados = []
        self.encontrado = None
        self._timer = QTimer()
        self._timer.timeout.connect(self._limpiar_resaltado)

        self._construir_ui()
        self._redibujar()
        self.showMaximized()

    def _construir_ui(self):
        central = QWidget()
        central.setStyleSheet(f"background: {P['fondo_panel']};")
        self.setCentralWidget(central)
        raiz = QVBoxLayout(central)
        raiz.setContentsMargins(0,0,0,0)
        raiz.setSpacing(0)

        top = QFrame()
        top.setFixedHeight(52)
        top.setStyleSheet(f"background: {P['fondo_panel']}; border-bottom: 1px solid {P['borde_sb']};")
        top_lo = QHBoxLayout(top)
        top_lo.setContentsMargins(16,0,16,0)
        top_lo.addWidget(QLabel("🌿"))
        titulo = QLabel("FlowTree v5")
        titulo.setStyleSheet(f"color: {P['texto_base']}; font-size: 15px; font-weight: 600;")
        top_lo.addWidget(titulo)
        top_lo.addSpacing(16)
        self.selector = SelectorTipo(self._cambiar_tipo)
        top_lo.addWidget(self.selector)
        top_lo.addStretch()
        raiz.addWidget(top)

        cuerpo = QHBoxLayout()
        cuerpo.setContentsMargins(0,0,0,0)
        cuerpo.setSpacing(0)

        canvas_area = QWidget()
        canvas_area.setStyleSheet(f"background: {P['fondo_deep']};")
        canvas_lo = QVBoxLayout(canvas_area)
        canvas_lo.setContentsMargins(0,0,0,0)
        canvas_lo.setSpacing(0)
        canvas_lo.addWidget(self._barra_stats())
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setStyleSheet("background: transparent; border: none;")
        self.canvas = CanvasArbol()
        self.scroll.setWidget(self.canvas)
        canvas_lo.addWidget(self.scroll, 1)
        canvas_lo.addWidget(self._barra_resultado())
        canvas_lo.addWidget(self._panel_inferior())
        cuerpo.addWidget(canvas_area, 1)

        cuerpo.addWidget(self._sidebar())
        raiz.addLayout(cuerpo)

    def _barra_stats(self):
        barra = QFrame()
        barra.setFixedHeight(44)
        barra.setStyleSheet("background: transparent; border-bottom: 1px solid #2D2B45;")
        layout = QHBoxLayout(barra)
        layout.setContentsMargins(12,0,12,0)
        layout.addStretch()
        self.stat_altura = self._chip_stat("ALTURA", "-")
        self.stat_nodos = self._chip_stat("NODOS", "-")
        self.stat_raiz = self._chip_stat("RAÍZ", "-")
        self.stat_tipo = self._chip_stat("TIPO", "BST", True)
        for chip in (self.stat_altura, self.stat_nodos, self.stat_raiz, self.stat_tipo):
            layout.addWidget(chip)
        return barra

    def _chip_stat(self, label, valor, acento=False):
        chip = QFrame()
        color_borde = P["violeta"] if acento else P["borde_normal"]
        chip.setStyleSheet(f"background: {P['fondo_card']}; border: 1px solid {color_borde}; border-radius: 6px;")
        layout = QHBoxLayout(chip)
        layout.setContentsMargins(10,6,10,6)
        lbl = QLabel(label + ":")
        lbl.setStyleSheet(f"font-size: 9px; color: {P['texto_apag']};")
        val = QLabel(valor)
        color_val = P["lila"] if acento else P["texto_base"]
        val.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {color_val};")
        chip._lbl_valor = val
        layout.addWidget(lbl)
        layout.addWidget(val)
        return chip

    def _barra_resultado(self):
        barra = QFrame()
        barra.setFixedHeight(32)
        barra.setStyleSheet(f"background: {P['fondo_panel']}; border-top: 1px solid {P['borde_sb']};")
        layout = QHBoxLayout(barra)
        layout.setContentsMargins(14,0,14,0)
        tag = QLabel("Resultado:")
        tag.setStyleSheet(f"font-size: 9px; color: {P['texto_apag']};")
        self.lbl_resultado = QLabel("—")
        self.lbl_resultado.setStyleSheet(f"font-size: 10px; color: {P['texto_med']}; font-family: monospace;")
        layout.addWidget(tag)
        layout.addWidget(self.lbl_resultado)
        layout.addStretch()
        return barra

    def _panel_inferior(self):
        panel = QFrame()
        panel.setStyleSheet(f"background: {P['fondo_panel']}; border-top: 1px solid {P['borde_sb']};")
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(12,8,12,8)
        layout.setSpacing(12)

        log_frame = QFrame()
        log_frame.setStyleSheet(f"background: {P['fondo_sb']}; border: 1px solid {P['borde_sb']}; border-radius: 8px;")
        log_layout = QVBoxLayout(log_frame)
        log_layout.setContentsMargins(10,8,10,10)
        log_layout.addWidget(QLabel("Registro de Actividad"))
        self._log_labels = []
        for _ in range(4):
            lbl = QLabel("—")
            lbl.setStyleSheet(f"font-size: 9px; color: {P['texto_apag']};")
            log_layout.addWidget(lbl)
            self._log_labels.append(lbl)
        layout.addWidget(log_frame, 1)

        rec_frame = QFrame()
        rec_frame.setFixedWidth(280)
        rec_frame.setStyleSheet(f"background: {P['fondo_sb']}; border: 1px solid {P['borde_sb']}; border-radius: 8px;")
        rec_layout = QVBoxLayout(rec_frame)
        rec_layout.setContentsMargins(10,8,10,10)
        rec_layout.addWidget(QLabel("Recorridos"))
        btn_layout = QHBoxLayout()
        for texto, metodo in [("Preorden", self._preorden), ("Inorden", self._inorden), ("Postorden", self._postorden)]:
            b = QPushButton(texto)
            b.clicked.connect(metodo)
            b.setStyleSheet(f"background: {P['fondo_card']}; color: {P['lila']}; border: 1px solid {P['borde_normal']}; border-radius: 6px; padding: 6px;")
            btn_layout.addWidget(b)
        rec_layout.addLayout(btn_layout)
        arch_layout = QHBoxLayout()
        for texto, metodo in [("Guardar", self._guardar), ("Cargar", self._cargar), ("Limpiar", self._limpiar)]:
            b = QPushButton(texto)
            b.clicked.connect(metodo)
            b.setStyleSheet(f"background: transparent; color: {P['texto_apag']}; border: 1px solid {P['borde_sb']}; border-radius: 6px; padding: 5px;")
            arch_layout.addWidget(b)
        rec_layout.addWidget(QLabel("Archivo"))
        rec_layout.addLayout(arch_layout)
        layout.addWidget(rec_frame)
        return panel

    def _sidebar(self):
        contenedor = QFrame()
        contenedor.setFixedWidth(220)
        contenedor.setStyleSheet(f"background: {P['fondo_sb']}; border-left: 1px solid {P['borde_sb']};")
        layout = QVBoxLayout(contenedor)
        layout.setContentsMargins(10,20,10,20)
        layout.setSpacing(12)

        layout.addWidget(QLabel("INSERTAR NODO"))
        self.ent_insertar = QLineEdit()
        self.ent_insertar.setPlaceholderText("Valor entero...")
        self.ent_insertar.returnPressed.connect(self._insertar)
        self.ent_insertar.setStyleSheet(f"background: {P['borde_sb']}; border-radius: 6px; padding: 6px; color: white;")
        btn_ins = QPushButton("Insertar")
        btn_ins.clicked.connect(self._insertar)
        layout.addWidget(self.ent_insertar)
        layout.addWidget(btn_ins)

        layout.addWidget(QLabel("BUSCAR / ELIMINAR"))
        self.ent_buscar = QLineEdit()
        self.ent_buscar.setPlaceholderText("Valor...")
        self.ent_buscar.setStyleSheet(f"background: {P['borde_sb']}; border-radius: 6px; padding: 6px; color: white;")
        btn_bus = QPushButton("Buscar")
        btn_bus.clicked.connect(self._buscar)
        btn_eli = QPushButton("Eliminar")
        btn_eli.clicked.connect(self._eliminar)
        layout.addWidget(self.ent_buscar)
        hb = QHBoxLayout()
        hb.addWidget(btn_bus)
        hb.addWidget(btn_eli)
        layout.addLayout(hb)

        layout.addWidget(QLabel("INSERCIÓN MÚLTIPLE"))
        hint = QLabel("Separados por coma (ej: 10,20,5)")
        hint.setStyleSheet(f"font-size: 9px; color: {P['texto_apag']};")
        self.ent_multi = QLineEdit()
        self.ent_multi.setPlaceholderText("10,20,30...")
        self.ent_multi.setStyleSheet(f"background: {P['borde_sb']}; border-radius: 6px; padding: 6px; color: white;")
        btn_multi = QPushButton("Insertar todos")
        btn_multi.clicked.connect(self._insertar_multi)
        layout.addWidget(hint)
        layout.addWidget(self.ent_multi)
        layout.addWidget(btn_multi)

        layout.addWidget(QLabel("HISTORIAL"))
        self.lbl_historial = QLabel("Sin acciones aún.")
        self.lbl_historial.setStyleSheet(f"font-size: 11px; color: {P['texto_med']}; font-family: monospace;")
        self.lbl_historial.setWordWrap(True)
        layout.addWidget(self.lbl_historial)

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
        self._mostrar(f"Insertado: {valor}  Camino: {' > '.join(map(str, camino))}")
        self._auto_limpiar(1800)

    def _insertar_multi(self):
        txt = self.ent_multi.text().strip()
        if not txt: return
        insertados = []
        for parte in txt.split(","):
            try:
                self.arbol.insertar(int(parte.strip()))
                insertados.append(parte.strip())
            except: pass
        self.ent_multi.clear()
        self.resaltados = []
        self.encontrado = None
        self._redibujar()
        self._mostrar(f"Insertados: {', '.join(insertados)}")

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
        if nodo:
            self._mostrar(f"Nodo {valor} encontrado  Camino: {' > '.join(map(str, camino))}")
        else:
            self._mostrar(f"Nodo {valor} no encontrado  Visitados: {' > '.join(map(str, camino))}")
        self._auto_limpiar(2500)

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
        self._mostrar(f"Nodo {valor} {'eliminado' if ok else 'no existe'}")

    def _preorden(self):
        r = self.arbol.preorden()
        self.resaltados = r
        self.encontrado = None
        self._redibujar()
        self._auto_limpiar(3000)
        self._mostrar_recorrido("Preorden", r)

    def _inorden(self):
        r = self.arbol.inorden()
        self.resaltados = r
        self.encontrado = None
        self._redibujar()
        self._auto_limpiar(3000)
        self._mostrar_recorrido("Inorden", r)

    def _postorden(self):
        r = self.arbol.postorden()
        self.resaltados = r
        self.encontrado = None
        self._redibujar()
        self._auto_limpiar(3000)
        self._mostrar_recorrido("Postorden", r)

    def _mostrar_recorrido(self, nombre, resultado):
        if not resultado:
            self._mostrar(f"{nombre}: árbol vacío")
        else:
            self._mostrar(f"{nombre}: {' → '.join(map(str, resultado))}")

    def _limpiar(self):
        if QMessageBox.question(self, "Limpiar", "¿Limpiar árbol?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            self.arbol.limpiar()
            self.resaltados = []
            self.encontrado = None
            self._redibujar()
            self._mostrar("Árbol limpiado")

    def _guardar(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar árbol", "", "JSON (*.json)")
        if ruta:
            with open(ruta, "w") as f:
                json.dump({"tipo": self.selector.seleccion, "valores": self.arbol.a_lista()}, f, indent=2)
            self._mostrar(f"Guardado: {ruta}")

    def _cargar(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Cargar árbol", "", "JSON (*.json)")
        if ruta:
            try:
                with open(ruta) as f:
                    data = json.load(f)
                tipo = data.get("tipo", "BST")
                valores = data.get("valores", [])
                self.selector.seleccion = tipo
                self.selector._refrescar()
                if tipo == "Binario":
                    self.arbol = ArbolBinario()
                elif tipo == "BST":
                    self.arbol = ArbolBST()
                else:
                    self.arbol = ArbolAVL()
                for v in valores:
                    self.arbol.insertar(v)
                self.resaltados = []
                self.encontrado = None
                self.stat_tipo._lbl_valor.setText(tipo)
                self._redibujar()
                self._mostrar(f"Cargado: {ruta} ({len(valores)} nodos)")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar:\n{e}")

    def _cambiar_tipo(self):
        tipo = self.selector.seleccion
        if tipo == "Binario":
            self.arbol = ArbolBinario()
        elif tipo == "BST":
            self.arbol = ArbolBST()
        else:
            self.arbol = ArbolAVL()
        self.resaltados = []
        self.encontrado = None
        self.stat_tipo._lbl_valor.setText(tipo)
        self._redibujar()
        self._mostrar(f"Árbol cambiado a: {tipo} (vacío)")

    def _redibujar(self):
        self.stat_altura._lbl_valor.setText(str(self.arbol.altura()))
        self.stat_nodos._lbl_valor.setText(str(self.arbol.total()))
        raiz = self.arbol.raiz.valor if self.arbol.raiz else "-"
        self.stat_raiz._lbl_valor.setText(str(raiz))
        self.canvas.actualizar(self.arbol, self.resaltados, self.encontrado)

    def _mostrar(self, texto):
        self.lbl_resultado.setText(texto)
        if hasattr(self, '_log_labels'):
            for i in range(3,0,-1):
                self._log_labels[i].setText(self._log_labels[i-1].text())
            self._log_labels[0].setText(texto[:60])
        actual = self.lbl_historial.text()
        if actual == "Sin acciones aún.":
            self.lbl_historial.setText(texto[:70])
        else:
            lineas = actual.split("\n")[:4]
            self.lbl_historial.setText("\n".join([texto[:70]] + lineas))

    def _auto_limpiar(self, ms):
        self._timer.start(ms)

    def _limpiar_resaltado(self):
        self._timer.stop()
        self.resaltados = []
        self.encontrado = None
        self._redibujar()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))
    ventana = FlowTree()
    ventana.show()
    sys.exit(app.exec_())