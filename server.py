from flask import Flask, render_template, url_for, request, redirect, session
from grapher import Graph
from random import randint

'''

Servidor del proyecto

Utilizado como muestra gráfica de los grafos genreados por el programa.
Se utiliza Flask para mayor conectividad con el código de Python.

'''

# Creación de la aplicación Flask
app = Flask(__name__)

# Creación e inicialización del grafo, utilizando el módulo Graph de "grapher.py"
graph = Graph()
graph.start()

#-----------------------------------------------------------------------------------

# Ruta princpal al idice de la página
@app.route('/')
def index():
    return render_template('index.html')


#-----------------------------------------------------------------------------------


# Ruta para añadir estudiantes al grafo
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    
    # Se detecta una llamada POST al enviar el formulario para añadir estudiante
    if request.method == "POST":
        
        # Se registran los datos (Nombre, carrera y semestre)
        st = request.form["student"]
        dg = request.form["degree"]
        sm = request.form["semester"]
        
        # Se llama la función para añadir nodos de alumno, de la clase "Graph"
        graph.add_student_vertex(st, dg, sm)
        
        # Se redirige al índice para refrescar el grafo
        return redirect(url_for('index'))

    # Si no hay una llamada POST, se renderiza la plantilla de índice
    return render_template('index.html')


#-----------------------------------------------------------------------------------

# Ruta para añadir habilidades al grafo
@app.route('/add_skill', methods=['GET', 'POST'])
def add_skill():
    error_message_skill = None

    # Se detecta una llamada POST al enviar el formulario para añadir habilidad
    if request.method == "POST":
        try:
            # Se registran los datos (Nombre y habilidad)
            st = request.form["student"]
            sk = request.form["skill"]

            # Se llama la función para añadir nodos de habilidad, de la clase "Graph"
            graph.add_skill_vertex(st, sk)

        # Manejo de errores
        except ValueError as e:
            error_message_skill = str(e)

        # Se redirige al índice para refrescar el grafo, con un mensaje de error si existe
        return render_template('index.html',
                                error_message_skill=error_message_skill)
    
    # Si no hay una llamada POST, se renderiza la plantilla de índice
    return render_template('index.html')


#-----------------------------------------------------------------------------------

# Ruta para añadir habilidades al grafo
@app.route('/search_path', methods=['GET', 'POST'])
def search_path():  
    # Variable para manejar errores
    error_message = None
    
    # Variable para almacenar el HTML del gráfico
    graph_html = None 

    # Se detecta una llamada POST al enviar el formulario para buscar el camino
    if request.method == "POST":
        try:
            # Se obtienen los datos del formulario (Nombre y habilidad)
            st = request.form["student"]
            sk = request.form["skill"]
            
            print("Estudiante:", st)
            print("Habilidad:", sk)

            best_path, stundet, semester = graph.find_best_path_to_skill(st, sk)  # Llamamos a la función para encontrar el mejor camino
            fig = graph.getDijkstra(best_path)
            graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')  # Convertimos el gráfico a HTML

        except Exception as e:
            error_message = str(e)  # Capturamos cualquier error y lo almacenamos

        # Renderizamos el template con el gráfico y el mensaje de error (si existe)
        return render_template('graph.html', graph_html=graph_html, error_message=error_message)
    

#-----------------------------------------------------------------------------------

# Ruta para manejar la muestra del grafo
@app.route('/graph')
def show_graph():
    
    # Se genera una figura para mostrar en la página
    fig = graph.getGraph()
    
    # Se convierte el grafo a HTML
    graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    return render_template('graph.html', graph_html=graph_html)


#-----------------------------------------------------------------------------------

# Ruta para manejar el algoritmo de Prim
@app.route('/prim', methods=['GET'])
def show_prim():
    print("Se actibo el algoritmo de Prim")
    print(f"Metodo: {request.method}")
    fig = graph.getMST()  # Llamamos al método que aplica el algoritmo de Prim
    
    # Se convierte el gráfico a HTML
    graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')  # Convertimos el gráfico a HTML
    
    return render_template("graph.html", graph_html=graph_html)


#-----------------------------------------------------------------------------------

# Ruta para manejar el algoritmo de Dijkstra
@app.route('/dijkstra_test', methods=['GET'])
def show_dijkstra():
    # Se obtienen los datos del formulario (Nombre y habilidad)
    st = request.args.get("student")
    sk = request.args.get("skill")
    
    # Se obtiene el mejor camino utilizando el algoritmo de Dijkstra
    path, student, semester = graph.find_best_path_to_skill(st, sk)
    
    # Se convierte el camino a un formato adecuado para el gráfico
    fig = graph.getDijkstra(path)  # Llamamos al método que aplica el algoritmo de Dijkstra
    
    # Se convierte el grafo a HTML
    graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')  # Convertimos el gráfico a HTML
    
    return render_template("graph.html", graph_html=graph_html)


#-----------------------------------------------------------------------------------

# Inicio del servidor
if __name__ == "__main__":
    app.run(debug=True, port=8080)
