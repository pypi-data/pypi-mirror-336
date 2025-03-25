# Hacku4 Academy Courses Library

Una biblioteca para Python para consultar cursos de la academia hack4u.

## Cursos disponibles:

- Introducción a Linux
- Personalización de Linux
- Introducción al Hacking
- Python Ofensivo

## Instalación

Instala el paquete usando `pip3`:

```python
pip3 install hack4u
```
## Uso básico

### Listar todos los cursos

```python3
from hack4u import list_cursos

for curso in list_cursos():
    print(curso)
```

### Obtener un curso por nombre

```python
from hack4u import get_curso_by_name

curso = get_curso_by_name("Python Ofensivo")
print(curso)
```

### Calcular duración total de los cursos

```python3
from hack4u.utils import total_duration

print(f"Duración total de los cursos: {total_duration()} horas")
```

