class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None
        self.altura = 1  # nomas pa avl


class ArbolBinario:

    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if not self.raiz:
            self.raiz = Nodo(valor)
            return []
        from collections import deque
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
        if nodo is None:
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
        if nodo is None:
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
        if n is None:
            return []
        return [n.valor] + self.preorden(n.izq, False) + self.preorden(n.der, False)

    def inorden(self, n=None, p=True):
        if p:
            n = self.raiz
        if n is None:
            return []
        return self.inorden(n.izq, False) + [n.valor] + self.inorden(n.der, False)

    def postorden(self, n=None, p=True):
        if p:
            n = self.raiz
        if n is None:
            return []
        return self.postorden(n.izq, False) + self.postorden(n.der, False) + [n.valor]

    def altura(self, n=None, p=True):
        if p:
            n = self.raiz
        if n is None:
            return 0
        return 1 + max(self.altura(n.izq, False), self.altura(n.der, False))

    def total(self, n=None, p=True):
        if p:
            n = self.raiz
        if n is None:
            return 0
        return 1 + self.total(n.izq, False) + self.total(n.der, False)

    def a_lista(self, n=None, p=True):
        if p:
            n = self.raiz
        if n is None:
            return []
        return [n.valor] + self.a_lista(n.izq, False) + self.a_lista(n.der, False)

    def limpiar(self):
        self.raiz = None

class ArbolBST(ArbolBinario):
    def insertar(self, valor):
        self.raiz, camino = self._insertar(self.raiz, valor, [])
        return camino

    def _insertar(self, nodo, valor, camino):
        if nodo is None:
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
        if nodo is None:
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
        if nodo is None:
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
        if nodo is None:
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
        if nodo is None:
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
        if nodo is None:
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
        if n is None:
            return []
        return [n.valor] + self.preorden(n.izq, False) + self.preorden(n.der, False)

    def inorden(self, n=None, p=True):
        if p:
            n = self.raiz
        if n is None:
            return []
        return self.inorden(n.izq, False) + [n.valor] + self.inorden(n.der, False)

    def postorden(self, n=None, p=True):
        if p:
            n = self.raiz
        if n is None:
            return []
        return self.postorden(n.izq, False) + self.postorden(n.der, False) + [n.valor]

    def altura(self, n=None, p=True):
        if p:
            return self._h(self.raiz)
        return self._h(n)

    def total(self, n=None, p=True):
        if p:
            n = self.raiz
        if n is None:
            return 0
        return 1 + self.total(n.izq, False) + self.total(n.der, False)

    def a_lista(self, n=None, p=True):
        if p:
            n = self.raiz
        if n is None:
            return []
        return [n.valor] + self.a_lista(n.izq, False) + self.a_lista(n.der, False)

    def limpiar(self):
        self.raiz = None