import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import json


class Graph:
    def __init__(self):
        self.matrix = np.array([])                                  # Matriz de adyacencia
        self.degrees = self.load_degrees()                          # Carreras
        self.categories = self.load_categories()                    # Categorías de las carreras
        self.students = {}                                          # Diccionario para guardar los estudiante
        self.skills = {}                                            # Diccionario para guardar las habilidades
        self.num_nodes = len(self.categories) + len(self.degrees)   # Nodos iniciales
        self.students_semesters = {}                                # Diccionario para guardar los semetres
    
    
    # Método para cargar las carreras desde degrees.json
    def load_degrees(self):
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
    
    
    
    # Método para cargar las categorías desde degrees.json
    def load_categories(self):
        # Se abre el archivo Json
        with open('../proyectoFinal/degrees.json', 'r') as f:
            data = json.load(f)
        
        # Se añade un índice a cada categoría
        categories = {i: cat for i, cat in enumerate(data.keys())}
        return categories
        
        
    # Método para imprimir la matriz del grafo (utilizado para test y debug)
    def get_graph_matrix(self):
        print(self.matrix)
        
        
    # Método para añadir un estudiante a la matriz de adyacencia
    def add_student_vertex(self, student, degree, year):
        
        # Se busca el inddice de la carrera en la matriz de adyacencia
        degree_index = next((k for k, v in self.degrees.items() if v == degree), None)
        
        # Si no se encuentra el index de la carrera, significa que no existe o se escribió mal
        if degree_index is None:
            print(f'Error: La carrera {degree} no existe.')
            return

        # Asignar índice al estudiante
        student_index = self.num_nodes
        
        # Se gurade el nombre del estudiante
        self.students[student_index] = student
        
        # Se guarda el semestre del estudiante
        self.students_semesters[student_index] = year
          
        # Agregar nodo para el estudiante
        self.add_vertex(1)
        
        # Se aumenta el numero de nodos del grafo, para futuras adiciones a la matriz
        self.num_nodes += 1
        
        # Conectar el estudiante a su carrera
        self.add_edge(student_index, degree_index, year)
        
        
    # Método para añadir una habilidad a la matriz de adyacencia
    def add_skill_vertex(self, student, skill):  
         
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
        
        
    # Método para añadir una conexión entre dos nodos
    def add_edge(self, vertex1, vertex2, weight=1.0):
        
        #Se añade un 1 entre dos vertices de la matriz de adyacencia (2D), esto genera un enlace entre los nodos
        self.matrix[vertex1][vertex2] = weight
        self.matrix[vertex2][vertex1] = weight
        
    
    # Método para añadir un vertice (nodo)
    def add_vertex(self, num_vertices):
        
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

        
    # Método para inicializar el grafo
    def getGraph(self):
        # Se genera un nuevo grafo a partir de la matriz de adyacencia
        G1 = nx.from_numpy_array(self.matrix, create_using=nx.Graph)

        # Se renombran los nodos utilizando los diccionarios de categorías, carreras, estudiantes y habilidades
        relabel_dict = {**self.categories, **self.degrees, **self.students, **self.skills}
        G1 = nx.relabel_nodes(G1, relabel_dict)

        # Lista de colores para los nodos
        colors = []
        for node in G1.nodes():
            if node in self.categories.values():
                colors.append("yellow")
            elif node in self.degrees.values():
                colors.append("lightgreen")
            elif node in self.skills.values():
                colors.append("lightcoral")
            else:
                colors.append("lightblue")

        # Posiciones de los nodos
        pos = nx.spring_layout(G1)  # Puedes usar otro layout si gustas

        # Dibujar el grafo
        plt.figure(figsize=(10, 8))
        nx.draw(G1, pos, with_labels=True, font_size=12, node_size=1000, node_color=colors, edge_color='grey')

        # Añadir etiquetas de los pesos
        edge_labels = nx.get_edge_attributes(G1, 'weight')
        nx.draw_networkx_edge_labels(G1, pos, edge_labels=edge_labels, font_size=10)

        # Mostrar grafo
        plt.title('Grafo de estudiantes y carreras')
        plt.tight_layout()
        plt.show()


    # Algortimo de Dijkstra
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

        # Buscar nodos por nombre
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
        if objective_student in graph.students.values():
                student_index = next((k for k, v in graph.students.items() if v == student), None)
            
        # Se encuenetra el semestre del estudiante encontrado    
        objective_semester = self.students_semesters[student_index]

        return best_path, objective_student, objective_semester

    
    # Método para inicializar la estructura del grafo
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
                    
                    
                    
                    
# Crear objeto de la clase Graph
graph = Graph()
graph.start()


#! App en terminal
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
            
        except ValueError as e:
            print(f"❌ {e}")
    
    elif option == '5':
        run = False
        
    else:
        print('Opción no válida. Intente de nuevo.')

