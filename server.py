from flask import Flask, render_template, url_for, request, redirect
from grapher import Graph

'''

Servidor del proyecto

'''

# Creación del servidor
app = Flask(__name__)

# Creación e inicialización del grafo
graph = Graph()
graph.start()


#* Ruta princpal al idice de la página
@app.route('/')
def index():
    return render_template('index.html')

#-----------------------------------------------------------------------------------

#* Ruta para añadir estudiantes al grafo
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    
    # Se detecta una llamada tipo POST al enviar el formulario para añadir estudiante
    if request.method == "POST":
        
        # Se registran los datos (Nombre, carrera y semestre)
        st = request.form["student"]
        dg = request.form["degree"]
        sm = request.form["semester"]
        
        # Se llama la función para añadir nodos de alumno, de la clase "Graph"
        graph.add_student_vertex(st, dg, sm)
        
        return redirect(url_for('index'))
    return render_template('index.html')

#-----------------------------------------------------------------------------------

@app.route('/add_skill', methods=['GET', 'POST'])
def add_skill():
    error_message_skill = None

    if request.method == "POST":
        try:
            st = request.form["student"]
            sk = request.form["skill"]

            graph.add_skill_vertex(st, sk)

        except ValueError as e:
            error_message_skill = str(e)

        return render_template('index.html',
                                error_message_skill=error_message_skill)
    
    return render_template('index.html')



#-----------------------------------------------------------------------------------

#* Ruta para añadir habilidades al grafo
@app.route('/search_path', methods=['GET', 'POST'])
def search_path():  
    
    # Se declaran variables para guardar la siguiente información
    path_result = None          # Camino resultante (array)
    student_found = None        # Alumno con la habilidad encontrado
    semester = None             # Semestre del alumno encontrado
    error_message = None        # Errores
    
    # Se detecta una llamada tipo POST al enviar el formulario para hacer la busqueda
    if request.method == "POST":
        try:
            
            # Se obtienen registran los datos (Nombre y habilidad)
            st = request.form["student"]
            sk = request.form["skill"]
            path_result, student_found, semester = graph.find_best_path_to_skill(st, sk)
           
        # Manejo de errores
        except ValueError as e:
            error_message = str(e)
        
        # Se modifica el html para mostrar los datos de camino encontrado
        return render_template('index.html', 
                              path_result=path_result,
                              student_found=student_found, 
                              semester=semester,
                              error_message=error_message)
    
    return render_template('index.html')

#-----------------------------------------------------------------------------------

#* Ruta para manejar la muestra del grafo
@app.route('/graph')
def show_graph():
    
    # Se genera una figura para mostrar en la página
    fig = graph.getGraph()
    
    # Se convierte la figura en html
    graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    return render_template('graph.html', graph_html=graph_html)

#-----------------------------------------------------------------------------------

@app.route('/prim', methods=['GET'])
def show_prim():
    
    fig = graph.getMST()  # Llamamos al método que aplica el algoritmo de Prim
    
    graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')  # Convertimos el gráfico a HTML
    
    return render_template("graph.html", graph_html=graph_html)

#-----------------------------------------------------------------------------------


#* Inicio del servidor
if __name__ == "__main__":
    app.run(debug=True, port=8080)
