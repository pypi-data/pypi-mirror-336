class Curso:

    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link
    
    def __repr__(self): # Representación en forma de cadena del objeto Curso
        return f"- {self.name} [{self.duration} horas] ({self.link})"

cursos = [
    Curso("Introducción a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/"),
    Curso("Personalización de Linux", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/"),
    Curso("Introducción al Hacking", 53, "https://hack4u.io/cursos/introduccion-al-hacking/"),
    Curso("Python Ofensivo", 35, "https://hack4u.io/cursos/python-ofensivo/")
]

def list_cursos():
    for curso in cursos:
        print(curso) # Se ejecuta __repr__ al intentar obtener una representación en cadena de un objeto Curso

def get_curso_by_name(name):
    for curso in cursos:
        if curso.name == name:
            return curso
        
    return None
