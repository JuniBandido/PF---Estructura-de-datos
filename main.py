#Logica
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
