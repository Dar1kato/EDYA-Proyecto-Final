import numpy as np
import networkx as nx
import plotly.graph_objects as go
import json

'''

Estructuras de Datos y Algoritmos

Proyecto Final
        
"Buscador de Alumnos para Proyectos Multidiciplinares"
        
Por: Daniel Peña Cruz

'''

#* Clase principal para el uso y manejo del grafo
class Graph:
    def __init__(self):
        self.matrix = np.array([])                                  # Matriz de adyacencia
        self.degrees = self.load_degrees()                          # Carreras
        self.categories = self.load_categories()                    # Categorías de las carreras
        self.students = {}                                          # Diccionario para guardar los estudiante
        self.skills = {}                                            # Diccionario para guardar las habilidades
        self.students_semesters = {}                                # Diccionario para guardar los semetres
        self.num_nodes = len(self.categories) + len(self.degrees)   # Nodos iniciales
        
        
    #-----------------------------------------------------------------------------
    
    #* Método para cargar las carreras desde degrees.json
    def load_degrees(self) -> dict:
        # Se abre el archivo Json
        with open('../proyectoFinal/degrees.json', 'r') as f:
            data = json.load(f)
        
        labels = {}
        index = len(data.keys())  # Comienza después de las categorías

        # Asignar índices a las carreras
        for deg_list in data.values():
            for degree in deg_list:
                labels[index] = degree
                index += 1
                
        return labels
    
    #-----------------------------------------------------------------------------
    
    #* Método para cargar las categorías desde degrees.json
    def load_categories(self) -> dict:
        # Se abre el archivo Json
        with open('../proyectoFinal/degrees.json', 'r') as f:
            data = json.load(f)
        
        # Se añade un índice a cada categoría
        categories = {i: cat for i, cat in enumerate(data.keys())}
        
        return categories
        
    #----------------------------------------------------------------------------- 
        
    #* Método para imprimir la matriz del grafo (utilizado para test y debug)
    def get_graph_matrix(self) -> None:
        print(self.matrix)
        
        return
        
    #-----------------------------------------------------------------------------
        
    #* Método para añadir un vertice (nodo)
    def add_vertex(self, num_vertices) -> None:
        
        # Si la matriz esta vacia, se genera la matriz
        if self.matrix.size == 0:
            self.matrix = np.zeros((num_vertices, num_vertices), dtype=int)
            
        # De lo contrario,
        else:
            
            # Se aumenta obtiene el tamaño actual de la matriz
            current_size = self.matrix.shape[0]
            
            # Se extiende el tamaño de la matriz, sumando el tamaño actual + el numero de nuevos nodos
            new_size = current_size + num_vertices
            
            # Se genera la nueva matriz
            new_matrix = np.zeros((new_size, new_size), dtype=int)
            
            # Se añaden los valores de la matriz actual a la nueva
            new_matrix[:current_size, :current_size] = self.matrix
            
            # Se guarda la nueva matriz como la actual
            self.matrix = new_matrix    
            
        return
            
    #-----------------------------------------------------------------------------        
            
    #* Método para añadir una conexión entre dos nodos
    def add_edge(self, vertex1, vertex2, weight=1.0) -> None:
        
        #Se añade el valor del peso entre dos vertices de la matriz de adyacencia (2D), esto genera un enlace entre los nodos
        self.matrix[vertex1][vertex2] = weight
        self.matrix[vertex2][vertex1] = weight    
        
        return
              
    #-----------------------------------------------------------------------------            
        
    #* Método para añadir un estudiante a la matriz de adyacencia
    def add_student_vertex(self, student, degree, year) -> None:
        try:
            # Se busca el inddice de la carrera en la matriz de adyacencia
            degree_index = next((k for k, v in self.degrees.items() if v == degree), None)
            
            # Si no se encuentra el index de la carrera, significa que no existe o se escribió mal
            if degree_index is None:
                raise ValueError(f'Error: La carrera {degree} no existe.')
            
        except ValueError as e:
            print(e)
            return

        # Asignar índice al estudiante
        student_index = self.num_nodes
        
        # Se gurada el nombre del estudiante
        self.students[student_index] = student
        
        # Se guarda el semestre del estudiante
        self.students_semesters[student_index] = year
          
        # Agregar nodo para el estudiante
        self.add_vertex(1)
        
        # Se aumenta el numero de nodos del grafo, para futuras adiciones a la matriz
        self.num_nodes += 1
        
        # Conectar el estudiante a su carrera
        self.add_edge(student_index, degree_index, year)
        
        return
        
    #-----------------------------------------------------------------------------
        
    #* Método para añadir una habilidad a la matriz de adyacencia
    def add_skill_vertex(self, student, skill) -> None:  
         
        try:
            # Si se encuentra el estudiante el el array de estudiantes, se obtiene el index del estudiante
            if student in self.students.values():
                student_index = next((k for k, v in self.students.items() if v == student), None)
                
            # De lo contrario, se retorna un error
            else:
                raise ValueError(f'Error: El estudiante {student} no existe.')
        except ValueError as e:
            print(e)
            return
        
        # Se obtiene un idex para la habilidad
        skill_index = next((k for k, v in self.skills.items() if v == skill), None)
        
        # Asignar índice a la habilidad
        skill_index = self.num_nodes
        self.skills[skill_index] = skill
        
        # Agregar nodo para la habilidad
        self.add_vertex(1)
        
        # Se aumenta el numero de nodos del grafo, para futuras adiciones a la matriz
        self.num_nodes += 1
        
        # Conectar el estudiante con la habilidad
        self.add_edge(student_index, skill_index)
        
        return
        
    #----------------------------------------------------------------------------- 
        
    #* Método para inicializar el grafo con Plotly   
    def getGraph(self):
        # Se genera un nuevo grafo a partir de la matriz de adyacencia
        G1 = nx.from_numpy_array(self.matrix, create_using=nx.Graph)

        # Se renombran los nodos utilizando los diccionarios de categorías, carreras, estudiantes y habilidades
        relabel_dict = {**self.categories, **self.degrees, **self.students, **self.skills}
        G1 = nx.relabel_nodes(G1, relabel_dict)

        # Posiciones de los nodos usando el layout de spring
        pos = nx.spring_layout(G1, seed=42)  # Añadimos seed para consistencia

        # Crear listas para nodos y aristas
        edge_x = []
        edge_y = []
        
        # Añadir coordenadas para las aristas
        for edge in G1.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
        # Crear trazado de aristas
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines')
        
        # Crear listas para nodos
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        
        # Añadir coordenadas e información para los nodos
        for node in G1.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(str(node))
            
            # Asignar colores según el tipo de nodo
            if node in self.categories.values():
                node_colors.append("yellow")
            elif node in self.degrees.values():
                node_colors.append("lightgreen")
            elif node in self.skills.values():
                node_colors.append("lightcoral")
            else:
                node_colors.append("lightblue")
        
        # Crear trazado de nodos
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="top center",
            hoverinfo='text',
            marker=dict(
                showscale=False,
                color=node_colors,
                size=15,
                line_width=2))
        
        # Crear etiquetas de peso para las aristas
        edge_labels_x = []
        edge_labels_y = []
        edge_labels_text = []
        
        for u, v, data in G1.edges(data=True):
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            # Posicionar la etiqueta en el medio de la arista
            edge_labels_x.append((x0 + x1) / 2)
            edge_labels_y.append((y0 + y1) / 2)
            edge_labels_text.append(str(data.get('weight', '')))
        
        edge_labels_trace = go.Scatter(
            x=edge_labels_x, y=edge_labels_y,
            mode='text',
            text=edge_labels_text,
            textposition="middle center",
            hoverinfo='none')
            
        # Crear la figura
        fig = go.Figure(data=[edge_trace, node_trace, edge_labels_trace],
                     layout=go.Layout(
                        title='Grafo de estudiantes y carreras',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )
        
        # Mostrar la figura (Para purebas o debug)
        #fig.show()
        
        return fig

    #-----------------------------------------------------------------------------
    
    #* Algortimo de Dijkstra
    def find_best_path_to_skill(self, student_name, skill_name):
        
        # Verificar existencia del estudiante
        student_index = next((k for k, v in self.students.items() if v == student_name), None)
        if student_index is None:
            raise ValueError(f"Estudiante '{student_name}' no encontrado")

        # Verificar existencia de la habilidad
        target_nodes = [k for k, v in self.skills.items() if v == skill_name]
        if not target_nodes:
            raise ValueError(f"Habilidad '{skill_name}' no encontrada")
        

        # Crear grafo NetworkX desde la matriz
        G = nx.from_numpy_array(self.matrix, create_using=nx.Graph)
        relabel_dict = {**self.categories, **self.degrees, **self.students, **self.skills}
        G = nx.relabel_nodes(G, relabel_dict)

        # Declara las condiciones iniciales para usar el algoritmo de Dijkstra
        start_node = student_name
        best_path = None
        best_cost = float('inf')

        # Dijkstra (con networkx)
        for target_skill_node in [skill_name]:
            try:
                path = nx.dijkstra_path(G, start_node, target_skill_node, weight='weight')
                cost = nx.dijkstra_path_length(G, start_node, target_skill_node, weight='weight')
                if cost < best_cost:
                    best_cost = cost
                    best_path = path
            except nx.NetworkXNoPath:
                continue
            
        # Si no se encuentra un camino valido, se retorna un error
        if best_path is None:
            raise ValueError("No se encontró un camino válido entre el estudiante y la habilidad.")
        
        # Se guarda el nombre del estudiante encontrado con el algoritmo
        objective_student = best_path[-2]
        
        # Se encuentra el indice del estudiante encontrado
        if objective_student in self.students.values():
                student_index = next((k for k, v in self.students.items() if v == student_name), None)
            
        # Se encuenetra el semestre del estudiante encontrado    
        objective_semester = self.students_semesters[student_index]

        # La función regresa el mejor camino, el nombre del estudiante encontrado y su semestre
        return best_path, objective_student, objective_semester
    
    #-----------------------------------------------------------------------------
    
    #* Método para inicializar la estructura del grafo
    def start(self):
        
        # Se agregar nodos de categorías
        self.add_vertex(len(self.categories))   
        
        # Se agregar nodos de carreras
        self.add_vertex(len(self.degrees))     
         
        # Se abre el archivo Json
        with open('../proyectoFinal/degrees.json', 'r') as f:
            data = json.load(f)
            
        # Conectar categorías con carreras
        for cat_index, category in self.categories.items():
            for deg_index, degree in self.degrees.items():
                if degree in data[category]:  
                    # Se conecta categoría con carrera
                    self.add_edge(cat_index, deg_index)  
                    
#-----------------------------------------------------------------------------------                          

'''
Creación del Grafo (para la exportación a server.py)

graph = Graph()
graph.start()


Correr la app en terminal

run = True
while run:
    print('Menú:')
    print('1. Añadir estudiante')
    print('2. Mostrar grafo')
    print('3. Añadir habilidad')
    print('4. Dijkstra')
    print('5. Salir')
    
    option = input('Seleccione una opción: ')
    
    if option == '1':
        student = input('Ingrese el nombre del estudiante: ')
        degree = input('Ingrese la carrera del estudiante: ')
        year = input('Ingresa el semestre del estudiante: ')
      
        graph.add_student_vertex(student, degree, year)
        
    elif option == '2':
        graph.getGraph()
        
    elif option == '3':
        student = input('Ingrese el nombre del estudiante: ')
        skill = input('Ingrese el nombre de la habilidad: ')
        graph.add_skill_vertex(student, skill)
        
    elif option == '4':
        student = input('Ingrese el nombre del estudiante: ')
        skill = input('Ingrese el nombre de la habilidad: ')
        try:
            path, student, semester = graph.find_best_path_to_skill(student, skill)
            print("Camino más corto:", " -> ".join(str(p) for p in path))
            
            print(f"El alumno con la habilidad de {skill} más cercano es: {student} de {semester}° semestre\n")
            
            # Visualizar el camino con Plotly
            graph.visualize_path(path)
            
        except ValueError as e:
            print(f"Error: no se encontró un camino valido {e}")
    
    elif option == '5':
        run = False
        
    else:
        print('Opción no válida. Intente de nuevo.')
        
'''