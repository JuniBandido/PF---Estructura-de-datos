import math
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QScrollArea, QFrame,
    QFileDialog, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, QPointF, QRectF

from logica import ArbolBinario, ArbolBST, ArbolAVL

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

class CanvasArbol(QWidget):

    RADIO    = 24
    RADIO_HJ = 20
    GAP_V    = 82
    MARGEN   = 56
    INICIO_Y = 52

    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet(f"background: {P['fondo_deep']};")
        self.arbol      = None
        self.resaltados = []
        self.encontrado = None
        self._pos_cache = {}

    def actualizar(self, arbol, resaltados=None, encontrado=None):
        self.arbol      = arbol
        self.resaltados = resaltados or []
        self.encontrado = encontrado
        self._recalcular_tamano()
        self.update()

    def _recalcular_tamano(self):
        if not self.arbol or not self.arbol.raiz:
            self.setMinimumSize(400, 300)
            return
        W = max(self.width(), 800)
        pos = {}
        self._calcular(self.arbol.raiz, pos, W, self.INICIO_Y, self.GAP_V)
        self._pos_cache = pos
        if pos:
            max_y = max(y for (_, _, y) in pos.values())
            max_x = max(x for (_, x, _) in pos.values())
            min_x = min(x for (_, x, _) in pos.values())
            needed_h = int(max_y + self.RADIO + 40)
            needed_w = int(max(max_x + self.RADIO + self.MARGEN, 400))
            self.setMinimumSize(needed_w, needed_h)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if not self.arbol or not self.arbol.raiz:
            self._pintar_vacio(painter)
            return

        W = self.width()
        pos = {}
        self._calcular(self.arbol.raiz, pos, W, self.INICIO_Y, self.GAP_V)

        if pos:
            max_y = max(y for (_, _, y) in pos.values())
            needed_h = int(max_y + self.RADIO + 40)
            max_x = max(x for (_, x, _) in pos.values())
            needed_w = int(max(max_x + self.RADIO + self.MARGEN, 400))
            if self.minimumHeight() < needed_h or self.minimumWidth() < needed_w:
                self.setMinimumSize(needed_w, needed_h)

        self._pintar_aristas(painter, self.arbol.raiz, pos)
        self._pintar_nodos(painter, pos)

    def _pintar_vacio(self, p):
        p.setPen(QColor(P["texto_apag"]))
        p.setFont(QFont("Segoe UI", 12))
        p.drawText(self.rect(), Qt.AlignCenter,"Árbol vacío\nInserta un valor para comenzar")

    def _calcular(self, raiz, pos, W, top, gap):
        SEP = self.RADIO * 2 + 24

        col = [0]
        def asignar_col(n):
            if n is None: return
            asignar_col(n.izq)
            n._col = float(col[0])
            col[0] += 1
            asignar_col(n.der)
        asignar_col(raiz)

        def centrar(n):
            if n is None: return
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
        centrar(raiz)

        todos_col = []
        def recoger(n, p):
            if n is None: return
            todos_col.append((n, p))
            recoger(n.izq, p+1)
            recoger(n.der, p+1)
        recoger(raiz, 0)

        min_col = min(n._col for n, _ in todos_col)
        for n, _ in todos_col:
            n._col -= min_col

        cx = W / 2.0
        rc = raiz._col

        for n, prof in todos_col:
            px = cx + (n._col - rc) * SEP
            py = top + prof * gap
            pos[id(n)] = (n.valor, px, py)

    def _pintar_aristas(self, painter, nodo, pos):
        if nodo is None: return
        entry = pos.get(id(nodo))
        if not entry: return
        _, x1, y1 = entry

        for hijo in (nodo.izq, nodo.der):
            if hijo:
                hijo_entry = pos.get(id(hijo))
                if not hijo_entry: continue
                _, x2, y2 = hijo_entry
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
            encontr = valor == self.encontrado
            nodo_real = self._buscar_nodo_por_id(self.arbol.raiz, nid)
            es_hoja = (nodo_real is not None and not nodo_real.izq and not nodo_real.der)

            if encontr:
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

            if resalt or encontr:
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
            painter.drawText(
                QRectF(x - R, y - R, R * 2, R * 2),
                Qt.AlignCenter, str(valor)
            )

            if isinstance(self.arbol, ArbolAVL):
                if nodo_real:
                    bf = self.arbol._bf(nodo_real)
                    color_bf = QColor(P["lila"]) if abs(bf) > 1 else QColor(P["texto_apag"])
                    painter.setPen(color_bf)
                    painter.setFont(QFont("Segoe UI", 7))
                    painter.drawText(int(x + R + 4), int(y - R + 10), f"bf{bf:+d}")

    def _buscar_nodo_por_id(self, nodo, nid):
        if nodo is None: return None
        if id(nodo) == nid: return nodo
        izq = self._buscar_nodo_por_id(nodo.izq, nid)
        if izq: return izq
        return self._buscar_nodo_por_id(nodo.der, nid)

def crear_boton(texto, variante="principal"):
    btn = QPushButton(texto)
    btn.setCursor(Qt.PointingHandCursor)

    estilos = {
        "principal": f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {P['violeta']}, stop:1 {P['violeta_med']});
                color: {P['lila_claro']};
                border: none;
                border-radius: 8px;
                padding: 9px 14px;
                font-size: 12px;
                font-weight: 600;
                text-align: center;
                letter-spacing: 0.03em;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #8B5CF6, stop:1 {P['violeta']});
            }}
            QPushButton:pressed {{ background: #5B21B6; padding-top: 10px; }}
        """,
        "secundario": f"""
            QPushButton {{
                background: {P['fondo_card']};
                color: {P['lila']};
                border: 1.5px solid {P['borde_normal']};
                border-radius: 8px;
                padding: 9px 14px;
                font-size: 12px;
                font-weight: 600;
                text-align: center;
                letter-spacing: 0.03em;
            }}
            QPushButton:hover {{
                background: #352F60;
                border-color: {P['violeta']};
                color: {P['lila_claro']};
            }}
            QPushButton:pressed {{ background: {P['borde_normal']}; padding-top: 10px; }}
        """,
        "neutro": f"""
            QPushButton {{
                background: transparent;
                color: {P['texto_apag']};
                border: 1px solid {P['borde_sb']};
                border-radius: 8px;
                padding: 9px 14px;
                font-size: 12px;
                font-weight: 500;
                text-align: center;
                letter-spacing: 0.03em;
            }}
            QPushButton:hover {{ background: {P['fondo_sb']}; color: {P['texto_med']}; border-color: {P['borde_normal']}; }}
            QPushButton:pressed {{ background: {P['borde_sb']}; }}
        """,
    }
    btn.setStyleSheet(estilos.get(variante, estilos["neutro"]))
    return btn


def crear_entrada(placeholder):
    e = QLineEdit()
    e.setPlaceholderText(placeholder)
    e.setStyleSheet(f"""
        QLineEdit {{
            background: {P['borde_sb']};
            border: 1px solid {P['borde_normal']};
            border-radius: 7px;
            padding: 7px 10px;
            font-size: 11px;
            color: {P['lila_claro']};
            font-family: Consolas, monospace;
        }}
        QLineEdit:focus {{
            border: 1.5px solid {P['violeta']};
            background: {P['fondo_card']};
        }}
    """)
    return e


def label_seccion(texto):
    lbl = QLabel(texto.upper())
    lbl.setStyleSheet(f"""
        color: {P['texto_apag']};
        font-size: 9px;
        font-weight: 500;
        letter-spacing: 0.1em;
        padding: 12px 6px 3px;
    """)
    return lbl


def separador():
    linea = QFrame()
    linea.setFrameShape(QFrame.HLine)
    linea.setStyleSheet(f"color: {P['borde_sb']}; margin: 3px 6px;")
    return linea


class SelectorTipoHorizontal(QWidget):
    OPCIONES = [
        ("Binario", "Por nivel"),
        ("BST",     "Búsqueda"),
        ("AVL",     "Balanceado"),
    ]

    def __init__(self, al_cambiar):
        super().__init__()
        self.seleccion = "BST"
        self.al_cambiar = al_cambiar
        self.chips = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        for nombre, desc in self.OPCIONES:
            chip = self._hacer_chip(nombre, desc)
            layout.addWidget(chip)
            self.chips[nombre] = chip

        self._refrescar()

    def _hacer_chip(self, nombre, desc):
        chip = QFrame()
        chip.setObjectName(nombre)
        chip.setCursor(Qt.PointingHandCursor)
        chip.setFixedHeight(34)

        layout = QHBoxLayout(chip)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(6)

        dot = QLabel()
        dot.setFixedSize(8, 8)
        dot.setObjectName(f"dot_{nombre}")

        lbl_n = QLabel(nombre)
        lbl_n.setObjectName(f"lbl_{nombre}")

        layout.addWidget(dot)
        layout.addWidget(lbl_n)

        for w in (chip, dot, lbl_n):
            w.mousePressEvent = lambda e, n=nombre: self._seleccionar(n)

        return chip

    def _seleccionar(self, nombre):
        self.seleccion = nombre
        self._refrescar()
        self.al_cambiar()

    def _refrescar(self):
        for nombre, chip in self.chips.items():
            activo = nombre == self.seleccion
            dot = chip.findChild(QLabel, f"dot_{nombre}")
            lbl = chip.findChild(QLabel, f"lbl_{nombre}")

            if activo:
                chip.setStyleSheet(f"""
                    QFrame {{
                        background: {P['fondo_card']};
                        border: 1px solid {P['violeta']};
                        border-radius: 7px;
                    }}
                """)
                if dot: dot.setStyleSheet(f"background: {P['violeta']}; border-radius: 4px;")
                if lbl: lbl.setStyleSheet(f"font-size: 11px; font-weight: 500; color: {P['lila']};")
            else:
                chip.setStyleSheet(f"""
                    QFrame {{
                        background: transparent;
                        border: 1px solid {P['borde_sb']};
                        border-radius: 7px;
                    }}
                    QFrame:hover {{ background: {P['fondo_sb']}; }}
                """)
                if dot: dot.setStyleSheet(f"background: transparent; border: 1.5px solid {P['texto_apag']}; border-radius: 4px;")
                if lbl: lbl.setStyleSheet(f"font-size: 11px; font-weight: 500; color: {P['texto_med']};")


class FlowTree(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FlowTree — Visualizador de Árboles")
        self.setMinimumSize(980, 660)
        self.resize(1260, 740)

        self.arbol = ArbolBST()
        self.resaltados = []
        self.encontrado = None
        self._timer = QTimer()
        self._timer.timeout.connect(self._limpiar_resaltado)

        self._construir_ui()
        self._redibujar()
        self.showMaximized()

    def _construir_ui(self):
        QApplication.setFont(QFont("Segoe UI", 10))

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
        cuerpo.addWidget(self._area_canvas())
        cuerpo.addWidget(self._sidebar())
        raiz.addLayout(cuerpo)

    def _topbar(self):
        bar = QFrame()
        bar.setFixedHeight(52)
        bar.setStyleSheet(f"""
            QFrame {{
                background: {P['fondo_panel']};
                border-bottom: 1px solid {P['borde_sb']};
            }}
        """)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(10)

        icono = QLabel("🌿")
        icono.setStyleSheet("font-size: 18px; background: transparent;")

        titulo = QLabel("FlowTree")
        titulo.setStyleSheet(f"""
            color: {P['texto_base']};
            font-size: 15px;
            font-weight: 600;
            background: transparent;
        """)

        layout.addWidget(icono)
        layout.addWidget(titulo)
        layout.addSpacing(16)

        self.selector = SelectorTipoHorizontal(self._cambiar_tipo)
        layout.addWidget(self.selector)

        layout.addStretch()
        return bar

    def _sidebar(self):
        contenedor = QFrame()
        contenedor.setFixedWidth(210)
        contenedor.setStyleSheet(f"""
            QFrame {{
                background: {P['fondo_sb']};
                border-left: 1px solid {P['borde_sb']};
            }}
        """)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent; border: none;")
        scroll.verticalScrollBar().setStyleSheet(f"""
            QScrollBar:vertical {{
                background: {P['fondo_sb']};
                width: 5px; border-radius: 3px;
            }}
            QScrollBar::handle:vertical {{
                background: {P['borde_normal']};
                border-radius: 3px;
            }}
        """)

        interior = QWidget()
        interior.setStyleSheet(f"background: {P['fondo_sb']};")
        layout = QVBoxLayout(interior)
        layout.setContentsMargins(10, 10, 10, 20)
        layout.setSpacing(6)

        layout.addWidget(self._label_grupo("Operaciones Individuales"))

        card_ins = self._card()
        cl = card_ins.layout()
        cl.addWidget(self._label_sub("Insertar Nodo"))
        self.ent_insertar = crear_entrada("Valor entero...")
        self.ent_insertar.returnPressed.connect(self._insertar)
        cl.addWidget(self.ent_insertar)
        b_ins = crear_boton("Insertar", "principal")
        b_ins.clicked.connect(self._insertar)
        cl.addWidget(b_ins)
        layout.addWidget(card_ins)

        card_be = self._card()
        cl2 = card_be.layout()
        cl2.addWidget(self._label_sub("Buscar / Eliminar Nodo"))
        self.ent_buscar = crear_entrada("Valor...")
        cl2.addWidget(self.ent_buscar)
        fila = QHBoxLayout()
        fila.setSpacing(6)
        b_bus = crear_boton("Buscar", "principal")
        b_bus.clicked.connect(self._buscar)
        b_eli = crear_boton("Eliminar", "secundario")
        b_eli.clicked.connect(self._eliminar)
        fila.addWidget(b_bus)
        fila.addWidget(b_eli)
        cl2.addLayout(fila)
        layout.addWidget(card_be)

        layout.addSpacing(4)

        layout.addWidget(self._label_grupo("Herramientas"))

        card_multi = self._card()
        cl3 = card_multi.layout()
        cl3.addWidget(self._label_sub("Inserción Múltiple"))
        hint = QLabel("Separados por coma (ej: 10, 20, 5)")
        hint.setStyleSheet(f"font-size: 9px; color: {P['texto_apag']};")
        hint.setWordWrap(True)
        cl3.addWidget(hint)
        self.ent_multi = crear_entrada("10, 20, 30...")
        cl3.addWidget(self.ent_multi)
        b_multi = crear_boton("Insertar todos", "principal")
        b_multi.clicked.connect(self._insertar_multi)
        cl3.addWidget(b_multi)
        layout.addWidget(card_multi)

        layout.addSpacing(4)

        layout.addWidget(self._label_grupo("Historial de Cambios"))
        card_hist = self._card()
        ch = card_hist.layout()
        self.lbl_historial = QLabel("Sin acciones aún.")
        self.lbl_historial.setStyleSheet(f"""
            font-size: 12px;
            color: {P['texto_med']};
            font-family: Consolas, monospace;
        """)
        self.lbl_historial.setWordWrap(True)
        ch.addWidget(self.lbl_historial)
        layout.addWidget(card_hist)

        layout.addStretch()
        scroll.setWidget(interior)

        sb_layout = QVBoxLayout(contenedor)
        sb_layout.setContentsMargins(0, 0, 0, 0)
        sb_layout.addWidget(scroll)
        return contenedor

    def _label_grupo(self, texto):
        lbl = QLabel(texto)
        lbl.setStyleSheet(f"""
            color: {P['texto_base']};
            font-size: 11px;
            font-weight: 600;
            padding: 6px 2px 2px;
            background: transparent;
        """)
        return lbl

    def _label_sub(self, texto):
        lbl = QLabel(texto)
        lbl.setStyleSheet(f"""
            color: {P['texto_med']};
            font-size: 10px;
            font-weight: 500;
            padding-bottom: 2px;
            background: transparent;
        """)
        return lbl

    def _card(self):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: {P['fondo_panel']};
                border: 1px solid {P['borde_sb']};
                border-radius: 8px;
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 8, 10, 10)
        layout.setSpacing(6)
        return frame

    def _area_canvas(self):
        contenedor = QWidget()
        contenedor.setStyleSheet(f"background: {P['fondo_deep']};")

        raiz_layout = QVBoxLayout(contenedor)
        raiz_layout.setContentsMargins(0, 0, 0, 0)
        raiz_layout.setSpacing(0)

        raiz_layout.addWidget(self._barra_stats())

        self.scroll_canvas = QScrollArea()
        self.scroll_canvas.setWidgetResizable(True)
        self.scroll_canvas.setFrameShape(QFrame.NoFrame)
        self.scroll_canvas.setStyleSheet(f"""
            QScrollArea {{ background: {P['fondo_deep']}; border: none; }}
            QScrollBar:vertical {{
                background: {P['fondo_sb']}; width: 6px; border-radius: 3px;
            }}
            QScrollBar::handle:vertical {{
                background: {P['borde_normal']}; border-radius: 3px;
            }}
            QScrollBar:horizontal {{
                background: {P['fondo_sb']}; height: 6px; border-radius: 3px;
            }}
            QScrollBar::handle:horizontal {{
                background: {P['borde_normal']}; border-radius: 3px;
            }}
        """)

        self.canvas = CanvasArbol()
        self.scroll_canvas.setWidget(self.canvas)

        raiz_layout.addWidget(self.scroll_canvas, 1)
        raiz_layout.addWidget(self._barra_resultado())
        raiz_layout.addWidget(self._panel_overlay())

        return contenedor

    def _barra_stats(self):
        barra = QFrame()
        barra.setFixedHeight(44)
        barra.setStyleSheet(f"""
            QFrame {{
                background: transparent;
                border-bottom: 1px solid {P['borde_sb']};
            }}
        """)
        layout = QHBoxLayout(barra)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)

        layout.addStretch()

        self.stat_altura = self._chip_stat("ALTURA", "-")
        self.stat_nodos = self._chip_stat("NODOS", "-")
        self.stat_raiz = self._chip_stat("RAÍZ", "-")
        self.stat_tipo = self._chip_stat("TIPO", "BST", acento=True)

        for chip in (self.stat_altura, self.stat_nodos, self.stat_raiz, self.stat_tipo):
            layout.addWidget(chip)

        return barra

    def _chip_stat(self, label, valor, acento=False):
        chip = QFrame()
        color_borde = P["violeta"] if acento else P["borde_normal"]
        chip.setStyleSheet(f"""
            QFrame {{
                background: {P['fondo_card']};
                border: 1px solid {color_borde};
                border-radius: 6px;
            }}
        """)
        layout = QHBoxLayout(chip)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(6)

        lbl = QLabel(label + ":")
        lbl.setStyleSheet(f"font-size: 9px; color: {P['texto_apag']}; font-weight: 500; background: transparent;")

        val = QLabel(valor)
        color_val = P["lila"] if acento else P["texto_base"]
        val.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {color_val}; background: transparent;")
        val._color = color_val
        chip._lbl_valor = val

        layout.addWidget(lbl)
        layout.addWidget(val)
        return chip

    def _panel_overlay(self):
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background: {P['fondo_panel']};
                border-top: 1px solid {P['borde_sb']};
            }}
        """)
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        log_frame = QFrame()
        log_frame.setStyleSheet(f"""
            QFrame {{
                background: {P['fondo_sb']};
                border: 1px solid {P['borde_sb']};
                border-radius: 8px;
            }}
        """)
        log_layout = QVBoxLayout(log_frame)
        log_layout.setContentsMargins(10, 8, 10, 10)
        log_layout.setSpacing(4)

        log_titulo = QLabel("Registro de Actividad")
        log_titulo.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {P['texto_base']}; background: transparent;")
        log_layout.addWidget(log_titulo)

        self._log_labels = []
        for _ in range(4):
            lbl_log = QLabel("—")
            lbl_log.setStyleSheet(f"font-size: 9px; color: {P['texto_apag']}; background: transparent; padding: 1px 0;")
            lbl_log.setWordWrap(True)
            log_layout.addWidget(lbl_log)
            self._log_labels.append(lbl_log)

        layout.addWidget(log_frame, 1)

        rec_frame = QFrame()
        rec_frame.setFixedWidth(290)
        rec_frame.setStyleSheet(f"""
            QFrame {{
                background: {P['fondo_sb']};
                border: 1px solid {P['borde_sb']};
                border-radius: 8px;
            }}
        """)
        rec_layout = QVBoxLayout(rec_frame)
        rec_layout.setContentsMargins(10, 8, 10, 10)
        rec_layout.setSpacing(6)

        rec_titulo = QLabel("Recorridos")
        rec_titulo.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {P['texto_base']}; background: transparent;")
        rec_layout.addWidget(rec_titulo)

        fila_rec = QHBoxLayout()
        fila_rec.setSpacing(6)
        for texto, metodo in [("Preorden", self._preorden),("Inorden", self._inorden),("Postorden", self._postorden),]:
            b = QPushButton(texto)
            b.setCursor(Qt.PointingHandCursor)
            b.setFixedHeight(36)
            b.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {P['fondo_card']}, stop:1 #252245);
                    color: {P['lila']};
                    border: 1.5px solid {P['borde_normal']};
                    border-radius: 8px;
                    font-size: 10px;
                    font-weight: 600;
                    text-align: center;
                    letter-spacing: 0.04em;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3D3470, stop:1 {P['fondo_card']});
                    border-color: {P['violeta']};
                    color: {P['lila_claro']};
                }}
                QPushButton:pressed {{
                    background: {P['borde_normal']};
                    padding-top: 2px;
                }}
            """)
            b.clicked.connect(metodo)
            fila_rec.addWidget(b)
        rec_layout.addLayout(fila_rec)

        arch_titulo = QLabel("Archivo")
        arch_titulo.setStyleSheet(f"font-size: 10px; font-weight: 600; color: {P['texto_apag']}; background: transparent; padding-top:4px;")
        rec_layout.addWidget(arch_titulo)
        fila_arch = QHBoxLayout()
        fila_arch.setSpacing(6)
        for texto, metodo in [("Guardar", self._guardar), ("Cargar", self._cargar), ("Limpiar", self._limpiar)]:
            b2 = QPushButton(texto)
            b2.setCursor(Qt.PointingHandCursor)
            b2.setFixedHeight(30)
            b2.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {P['texto_apag']};
                    border: 1px solid {P['borde_sb']};
                    border-radius: 7px;
                    font-size: 9px;
                    font-weight: 500;
                    text-align: center;
                    letter-spacing: 0.03em;
                }}
                QPushButton:hover {{
                    background: {P['fondo_sb']};
                    color: {P['texto_med']};
                    border-color: {P['borde_normal']};
                }}
                QPushButton:pressed {{ background: {P['borde_sb']}; }}
            """)
            b2.clicked.connect(metodo)
            fila_arch.addWidget(b2)
        rec_layout.addLayout(fila_arch)

        layout.addWidget(rec_frame)
        return panel

    def _barra_resultado(self):
        barra = QFrame()
        barra.setFixedHeight(32)
        barra.setStyleSheet(f"""
            QFrame {{
                background: {P['fondo_panel']};
                border-top: 1px solid {P['borde_sb']};
            }}
        """)
        layout = QHBoxLayout(barra)
        layout.setContentsMargins(14, 0, 14, 0)
        layout.setSpacing(8)

        tag = QLabel("Resultado:")
        tag.setStyleSheet(f"font-size: 9px; color: {P['texto_apag']}; font-weight: 500; background: transparent;")

        self.lbl_resultado = QLabel("—")
        self.lbl_resultado.setStyleSheet(f"""
            font-size: 10px;
            color: {P['texto_med']};
            font-family: Consolas, monospace;
            background: transparent;
        """)

        layout.addWidget(tag)
        layout.addWidget(self.lbl_resultado)
        layout.addStretch()
        return barra

    def _insertar(self):
        txt = self.ent_insertar.text().strip()
        if not txt:
            return
        try:
            valor = int(txt)
        except:
            QMessageBox.warning(self, "Error", "Ingresa un número entero válido.")
            return

        camino = self.arbol.insertar(valor)
        self.ent_insertar.clear()
        self.resaltados = camino if isinstance(camino, list) else []
        self.encontrado = valor
        self._redibujar()
        self._mostrar(f"Insertado: {valor}   Camino: {' > '.join(map(str, self.resaltados))}")
        self._auto_limpiar(1800)

    def _insertar_multi(self):
        txt = self.ent_multi.text().strip()
        if not txt:
            return
        insertados = []
        for parte in txt.split(","):
            try:
                self.arbol.insertar(int(parte.strip()))
                insertados.append(parte.strip())
            except:
                pass
        self.ent_multi.clear()
        self.resaltados = []
        self.encontrado = None
        self._redibujar()
        self._mostrar(f"Insertados: {', '.join(insertados)}")

    def _buscar(self):
        txt = self.ent_buscar.text().strip()
        if not txt:
            return
        try:
            valor = int(txt)
        except:
            QMessageBox.warning(self, "Error", "Ingresa un número entero válido.")
            return

        nodo, camino = self.arbol.buscar(valor)
        self.resaltados = camino
        self.encontrado = valor if nodo else None
        self._redibujar()
        if nodo:
            self._mostrar(f"Nodo {valor} encontrado   Camino: {' > '.join(map(str, camino))}")
        else:
            self._mostrar(f"Nodo {valor} no encontrado   Visitados: {' > '.join(map(str, camino))}")
        self._auto_limpiar(2500)

    def _eliminar(self):
        txt = self.ent_buscar.text().strip()
        if not txt:
            return
        try:
            valor = int(txt)
        except:
            QMessageBox.warning(self, "Error", "Ingresa un número entero válido.")
            return

        ok = self.arbol.eliminar(valor)
        self.ent_buscar.clear()
        self.resaltados = []
        self.encontrado = None
        self._redibujar()
        self._mostrar(f"Nodo {valor} {'eliminado.' if ok else 'no existe en el árbol.'}")

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
            self._mostrar(f"{nombre}: árbol vacío.")
            return
        valores = " → ".join(map(str, resultado))
        self._mostrar(f"{nombre}: {valores}")

    def _limpiar(self):
        if QMessageBox.question(self, "Limpiar", "¿Deseas limpiar el árbol?",QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.arbol.limpiar()
            self.resaltados = []
            self.encontrado = None
            self._redibujar()
            self._mostrar("Árbol limpiado.")

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

    def _guardar(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar árbol", "", "JSON (*.json);;Todos (*.*)")
        if not ruta:
            return
        with open(ruta, "w") as f:
            json.dump({"tipo": self.selector.seleccion,"valores": self.arbol.a_lista()}, f, indent=2)
        self._mostrar(f"Guardado: {ruta}")

    def _cargar(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Cargar árbol", "", "JSON (*.json);;Todos (*.*)")
        if not ruta:
            return
        try:
            with open(ruta) as f:
                datos = json.load(f)
            tipo = datos.get("tipo", "BST")
            valores = datos.get("valores", [])
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
            self._mostrar(f"Cargado: {ruta}  ({len(valores)} nodos)")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar:\n{e}")

    def _redibujar(self):
        self.stat_altura._lbl_valor.setText(str(self.arbol.altura()))
        self.stat_nodos._lbl_valor.setText(str(self.arbol.total()))
        raiz = self.arbol.raiz.valor if self.arbol.raiz else "-"
        self.stat_raiz._lbl_valor.setText(str(raiz))
        self.canvas.actualizar(self.arbol, self.resaltados, self.encontrado)

    def _mostrar(self, texto):
        self.lbl_resultado.setText(texto)
        if hasattr(self, '_log_labels'):
            for i in range(len(self._log_labels) - 1, 0, -1):
                self._log_labels[i].setText(self._log_labels[i - 1].text())
            self._log_labels[0].setText(texto[:60] + ("..." if len(texto) > 60 else ""))
        if hasattr(self, 'lbl_historial'):
            actual = self.lbl_historial.text()
            if actual == "Sin acciones aún.":
                self.lbl_historial.setText(texto[:70])
            else:
                lineas = actual.split("\n")[:4]
                self.lbl_historial.setText("\n".join([texto[:70]] + lineas))

    def _auto_limpiar(self, ms):
        self._timer.stop()
        self._timer.start(ms)

    def _limpiar_resaltado(self):
        self._timer.stop()
        self.resaltados = []
        self.encontrado = None
        self._redibujar()