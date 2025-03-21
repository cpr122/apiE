class Nodo:
    def __init__(self, datos, padre=None, hijos=None):
        self.datos = datos  # Store the state
        self.padre = padre  # Store the parent node
        self.costo = None
        self.set_hijos(hijos)

    def set_hijos(self, hijos):
        self.hijos = hijos if hijos is not None else []
        for h in self.hijos:
            h.padre = self  # Ensure each child knows its parent

    def get_hijos(self):
        return self.hijos

    def get_datos(self):  # ✅ FIXED: Add this method
        return self.datos

    def set_datos(self, datos):
        self.datos = datos

    def get_padre(self):  # ✅ FIXED: Ensure we can retrieve the parent
        return self.padre

    def igual(self, nodo):
        return self.get_datos() == nodo.get_datos()

    def en_lista(self, lista_nodos):
        return any(self.igual(n) for n in lista_nodos)

    def __str__(self):
        return str(self.get_datos())
