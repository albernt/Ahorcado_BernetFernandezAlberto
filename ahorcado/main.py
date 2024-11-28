# Diccionarios de palabras organizadas en categorías
word_categories = {
    "Frutas": [
        "Guayaba", "Cereza", "Ciruela", "Papaya", "Lima", "Melon", "Tamarindo", "Granada",
        "Kiwi", "Mandarina", "Mango", "Naranja", "Pera", "Manzana", "Frambuesa", "Arandano",
        "Higo", "Chirimoya", "Uva", "Piña", "Sandia", "Durazno", "Pomelo", "Maracuya"
    ],
    "Conceptos Informáticos": [
        "Algoritmo", "Compilador", "Iteracion", "Metodo", "Variable", "Enlace", "Recursion", "Segmento",
        "Funcion", "Objeto", "Clase", "Encapsulamiento", "Herencia", "Polimorfismo", "Framework", "Depuracion",
        "Script", "Modulo", "Inteligencia", "Interfaz", "Repositorio", "Servidor", "Cliente", "Protocolo"
    ],
    "Nombres de Personas": [
        "Elena", "Marcos", "Julia", "Carlos", "Ana", "Luis", "Sofia", "Fernando",
        "Maria", "Javier", "Camila", "Pedro", "Isabel", "Rafael", "Lucia", "Miguel",
        "Valeria", "Daniel", "Gabriela", "Sergio", "Claudia", "Jorge", "Natalia", "Alberto"
    ]
}


# Creamos la conexion a SQLite y creamos tabla. En este caso he modelado solo una tabla de jugadores, en la cual guardaré las victorias y derrotas
def init_db():
    conn = sqlite3.connect("ahorcado.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jugadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ganadas INTEGER DEFAULT 0,
            perdidas INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
