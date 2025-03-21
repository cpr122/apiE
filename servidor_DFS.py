from flask import Flask, render_template, request, jsonify
from arbol import Nodo
from collections import deque

app = Flask(__name__)

# Funciones de búsqueda (sin cambios)
def buscar_solucion_BFS(nodo_inicial, solucion):
    visitados = set()
    cola = deque([nodo_inicial])
    
    while cola:
        nodo_actual = cola.popleft()
        if nodo_actual.get_datos() == solucion:
            return nodo_actual
        visitados.add(tuple(nodo_actual.get_datos()))
        
        for hijo in generar_hijos(nodo_actual):
            if tuple(hijo.get_datos()) not in visitados:
                cola.append(hijo)
    return None

def buscar_solucion_DFS_iterativo(nodo_inicial, solucion):
    visitados = set()
    pila = [nodo_inicial]
    
    while pila:
        nodo_actual = pila.pop()
        if nodo_actual.get_datos() == solucion:
            return nodo_actual
        visitados.add(tuple(nodo_actual.get_datos()))
        
        for hijo in reversed(generar_hijos(nodo_actual)):
            if tuple(hijo.get_datos()) not in visitados:
                pila.append(hijo)
    return None

def buscar_solucion_DFS_recursivo(nodo_actual, solucion, visitados):
    if nodo_actual.get_datos() == solucion:
        return nodo_actual
    
    visitados.add(tuple(nodo_actual.get_datos()))
    for hijo in generar_hijos(nodo_actual):
        if tuple(hijo.get_datos()) not in visitados:
            resultado = buscar_solucion_DFS_recursivo(hijo, solucion, visitados)
            if resultado:
                return resultado
    return None

# Función que genera los hijos de un nodo
def generar_hijos(nodo):
    dato_nodo = nodo.get_datos()
    return [
        Nodo([dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]], nodo),
        Nodo([dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]], nodo),
        Nodo([dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]], nodo)
    ]

# Ruta para la página principal
@app.route("/")
def index():
    return render_template("index.html")

# Ruta para la búsqueda
@app.route("/buscar", methods=["POST"])
def buscar():
    data = request.get_json()
    estado_inicial = data.get("estado_inicial")
    solucion = data.get("solucion")
    
    if not estado_inicial or not solucion:
        return jsonify({"error": "Faltan datos en la petición"}), 400
    
    nodo_inicial = Nodo(estado_inicial)
    visitados = set()
    
    # Buscar con los tres algoritmos
    resultados = {
        "bfs": None,
        "dfs_iterativo": None,
        "dfs_recursivo": None
    }
    
    # BFS
    nodo_solucion_bfs = buscar_solucion_BFS(nodo_inicial, solucion)
    if nodo_solucion_bfs:
        resultado_bfs = []
        while nodo_solucion_bfs:
            resultado_bfs.append(nodo_solucion_bfs.get_datos())
            nodo_solucion_bfs = nodo_solucion_bfs.get_padre()
        resultados["bfs"] = resultado_bfs[::-1]  # Invertir el orden de la solución

    # DFS Iterativo
    nodo_solucion_dfs_iterativo = buscar_solucion_DFS_iterativo(nodo_inicial, solucion)
    if nodo_solucion_dfs_iterativo:
        resultado_dfs_iterativo = []
        while nodo_solucion_dfs_iterativo:
            resultado_dfs_iterativo.append(nodo_solucion_dfs_iterativo.get_datos())
            nodo_solucion_dfs_iterativo = nodo_solucion_dfs_iterativo.get_padre()
        resultados["dfs_iterativo"] = resultado_dfs_iterativo[::-1]

    # DFS Recursivo
    nodo_solucion_dfs_recursivo = buscar_solucion_DFS_recursivo(nodo_inicial, solucion, visitados)
    if nodo_solucion_dfs_recursivo:
        resultado_dfs_recursivo = []
        while nodo_solucion_dfs_recursivo:
            resultado_dfs_recursivo.append(nodo_solucion_dfs_recursivo.get_datos())
            nodo_solucion_dfs_recursivo = nodo_solucion_dfs_recursivo.get_padre()
        resultados["dfs_recursivo"] = resultado_dfs_recursivo[::-1]

    # Si los tres algoritmos no encuentran una solución
    if not any(resultados.values()):
        return jsonify({"mensaje": "No se encontró una solución en ninguno de los algoritmos"})

    return jsonify(resultados)

# Iniciar la aplicación Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

