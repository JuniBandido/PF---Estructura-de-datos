#Logica
import json
from collections import deque
class NodoBST:
    def __init__(self, v):
        self.val  = v
        self.izq  = None
        self.der  = None


class NodoAVL:
    def __init__(self, v):
        self.val   = v
        self.izq   = None
        self.der   = None
        self.altura = 1


class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, val):
        if not self.raiz:
            self.raiz = NodoBST(val)
            return []

        cola = deque([self.raiz])

        while cola:
            n = cola.popleft()
            if not n.izq:
                n.izq = NodoBST(val)
                return []

            else:
                cola.append(n.izq)
            if not n.der:
                n.der = NodoBST(val)
                return []

            else:
                cola.append(n.der)

    def buscar(self, val, nodo=None, primero=True):
        if primero:
            nodo = self.raiz

        if nodo is None:
            return None, []

        if nodo.val == val:
            return nodo, [nodo.val]

        izq, pi = self.buscar(val, nodo.izq, False)
        if izq:
            return izq, [nodo.val] + pi

        der, pd = self.buscar(val, nodo.der, False)
        if der:
            return der, [nodo.val] + pd

        return None, [nodo.val]

    def eliminar(self, val):
        self.raiz, elim = self._elim(self.raiz, val)
        return elim

    def _elim(self, nodo, val):
        if nodo is None:
            return None, False

        if nodo.val == val:
            if not nodo.izq and not nodo.der:
                return None, True

            if not nodo.izq:
                return nodo.der, True

            if not nodo.der:
                return nodo.izq, True

            s = self._min(nodo.der)
            nodo.val = s.val
            nodo.der, _ = self._elim(nodo.der, s.val)
            return nodo, True

        nodo.izq, ei = self._elim(nodo.izq, val)
        if ei:
            return nodo, True

        nodo.der, ed = self._elim(nodo.der, val)
        return nodo, ed

    def _min(self, n):
        while n.izq:
            n = n.izq
        return n

    def preorden(self, n=None, f=True):
        if f:
            n = self.raiz
        if n is None:
            return []
        return [n.val] + self.preorden(n.izq, False) + self.preorden(n.der, False)

    def inorden(self, n=None, f=True):
        if f:
            n = self.raiz
        if n is None:
            return []

        return self.inorden(n.izq, False) + [n.val] + self.inorden(n.der, False)

    def postorden(self, n=None, f=True):
        if f:
            n = self.raiz
        if n is None:
            return []
        return self.postorden(n.izq, False) + self.postorden(n.der, False) + [n.val]

    def altura(self, n=None, f=True):
        if f:
            n = self.raiz
        if n is None:
            return 0
        return 1 + max(self.altura(n.izq, False), self.altura(n.der, False))

    def contar(self, n=None, f=True):
        if f:
            n = self.raiz
        if n is None:
            return 0
        return 1 + self.contar(n.izq, False) + self.contar(n.der, False)

    def a_lista(self, n=None, f=True):
        if f:
            n = self.raiz
        if n is None:
            return []
        return [n.val] + self.a_lista(n.izq, False) + self.a_lista(n.der, False)

    def limpiar(self):
        self.raiz = None

    def guardar(self, ruta):
        with open(ruta, "w") as arch:
            json.dump({"tipo": self.__class__.__name__,
                       "valores": self.a_lista()}, arch, indent=2)

    @classmethod
    def cargar(cls, ruta):
        with open(ruta) as arch:
            datos = json.load(arch)
        return datos.get("tipo", "BST"), datos.get("valores", [])


class BST(ArbolBinario):

    def insertar(self, val):
        self.raiz, camino = self._ins(self.raiz, val, [])
        return camino

    def _ins(self, nodo, val, camino):
        if nodo is None:
            camino.append(val)
            return NodoBST(val), camino
        camino.append(nodo.val)

        if val < nodo.val:
            nodo.izq, camino = self._ins(nodo.izq, val, camino)

        elif val > nodo.val:
            nodo.der, camino = self._ins(nodo.der, val, camino)

        return nodo, camino

    def buscar(self, val, nodo=None, f=True):
        if f: nodo = self.raiz
        if nodo is None:
            return None, []

        if nodo.val == val:
            return nodo, [nodo.val]

        if val < nodo.val:
            n, p = self.buscar(val, nodo.izq, False)

        else:
            n, p = self.buscar(val, nodo.der, False)

        return n, [nodo.val] + p

    def eliminar(self, val):
        self.raiz, elim = self._elim_bst(self.raiz, val)
        return elim

    def _elim_bst(self, nodo, val):
        if nodo is None:
            return None, False

        if val < nodo.val:
            nodo.izq, e = self._elim_bst(nodo.izq, val)
            return nodo, e

        if val > nodo.val:
            nodo.der, e = self._elim_bst(nodo.der, val)
            return nodo, e

        if not nodo.izq and not nodo.der:
            return None, True

        if not nodo.izq:
            return nodo.der, True

        if not nodo.der:
            return nodo.izq, True

        s = self._min(nodo.der)
        nodo.val = s.val
        nodo.der, _ = self._elim_bst(nodo.der, s.val)
        return nodo, True


class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def _alt(self, n):
        return n.altura if n else 0

    def _fb(self, n):
        return (self._alt(n.izq) - self._alt(n.der)) if n else 0

    def _act(self, n):
        if n:
            n.altura = 1 + max(self._alt(n.izq), self._alt(n.der))

    def _rot_der(self, y):
        x = y.izq; t = x.der
        x.der = y; y.izq = t
        self._act(y); self._act(x)
        return x

    def _rot_izq(self, x):
        y = x.der; t = y.izq
        y.izq = x; x.der = t
        self._act(x); self._act(y)
        return y

    def _balancear(self, n):
        self._act(n)
        fb = self._fb(n)
        if fb > 1:
            if self._fb(n.izq) < 0:
                n.izq = self._rot_izq(n.izq)
            return self._rot_der(n)
        if fb < -1:
            if self._fb(n.der) > 0:
                n.der = self._rot_der(n.der)
            return self._rot_izq(n)
        return n

    def insertar(self, val):
        self.raiz, camino = self._ins(self.raiz, val, [])
        return camino

    def _ins(self, nodo, val, camino):
        if nodo is None:
            camino.append(val)
            return NodoAVL(val), camino
        camino.append(nodo.val)
        if val < nodo.val:
            nodo.izq, camino = self._ins(nodo.izq, val, camino)
        elif val > nodo.val:
            nodo.der, camino = self._ins(nodo.der, val, camino)
        else:
            return nodo, camino
        return self._balancear(nodo), camino

    def buscar(self, val, nodo=None, f=True):
        if f: nodo = self.raiz
        if nodo is None:
            return None, []
        if nodo.val == val:
            return nodo, [nodo.val]
        if val < nodo.val:
            n, p = self.buscar(val, nodo.izq, False)
        else:
            n, p = self.buscar(val, nodo.der, False)
        return n, [nodo.val] + p

    def eliminar(self, val):
        self.raiz, elim = self._elim(self.raiz, val)
        return elim

    def _elim(self, nodo, val):
        if nodo is None:
            return None, False

        if val < nodo.val:
            nodo.izq, e = self._elim(nodo.izq, val)
            return self._balancear(nodo), e

        if val > nodo.val:
            nodo.der, e = self._elim(nodo.der, val)
            return self._balancear(nodo), e

        if not nodo.izq and not nodo.der:
            return None, True

        if not nodo.izq:
            return nodo.der, True

        if not nodo.der:
            return nodo.izq, True

        s = self._min(nodo.der)
        nodo.val = s.val
        nodo.der, _ = self._elim(nodo.der, s.val)
        return self._balancear(nodo), True

    def _min(self, n):
        while n.izq:
            n = n.izq
        return n

    def preorden(self, n=None, f=True):
        if f: n = self.raiz
        if n is None: return []
        return [n.val] + self.preorden(n.izq, False) + self.preorden(n.der, False)

    def inorden(self, n=None, f=True):
        if f: n = self.raiz
        if n is None: return []
        return self.inorden(n.izq, False) + [n.val] + self.inorden(n.der, False)

    def postorden(self, n=None, f=True):
        if f: n = self.raiz
        if n is None: return []
        return self.postorden(n.izq, False) + self.postorden(n.der, False) + [n.val]

    def altura(self, n=None, f=True):
        if f: return self._alt(self.raiz)
        return self._alt(n)

    def contar(self, n=None, f=True):
        if f: n = self.raiz
        if n is None: return 0
        return 1 + self.contar(n.izq, False) + self.contar(n.der, False)

    def a_lista(self, n=None, f=True):
        if f: n = self.raiz
        if n is None: return []
        return [n.val] + self.a_lista(n.izq, False) + self.a_lista(n.der, False)

    def limpiar(self):
        self.raiz = None

    def buscar_nodo(self, nodo, val):
        if nodo is None: return None
        if nodo.val == val: return nodo
        if val < nodo.val: return self.buscar_nodo(nodo.izq, val)
        return self.buscar_nodo(nodo.der, val)

    def guardar(self, ruta):
        with open(ruta, "w") as arch:
            json.dump({"tipo": "AVL", "valores": self.a_lista()}, arch, indent=2)

    @classmethod
    def cargar(cls, ruta):
        with open(ruta) as arch:
            datos = json.load(arch)
        return datos.get("tipo", "AVL"), datos.get("valores", [])


def crear_arbol(tipo: str):
    tipos = {"Binario": ArbolBinario, "BST": BST, "AVL": ArbolAVL}
    cls = tipos.get(tipo)
    if cls is None:
        raise ValueError(f"Tipo desconocido: '{tipo}'. Usa uno de: {list(tipos)}")
    return cls()
