# Diccionarios de palabras organizadas en categorías
import random
import sqlite3

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

# Declaración de variables que vamos a usar en el proyecto
word = ""
guessed_word = ""
category = ""
max_steps = 7
hangman_step = 0
letter_buttons = []
wrong_letters = set()
player_name = ""


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


# Metodo para guardar las partidas ganadas/perdidas en la bbdd
def save_game_result(won):
    conn = sqlite3.connect("ahorcado.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, ganadas, perdidas FROM jugadores WHERE nombre = ?", (player_name,))
    result = cursor.fetchone()
    if result:
        player_id, ganadas, perdidas = result
        if won:
            ganadas += 1
        else:
            perdidas += 1
        cursor.execute("UPDATE jugadores SET ganadas = ?, perdidas = ? WHERE id = ?", (ganadas, perdidas, player_id))
    else:
        cursor.execute("INSERT INTO jugadores (nombre, ganadas, perdidas) VALUES (?, ?, ?)",
                       (player_name, 1 if won else 0, 0 if won else 1))
    conn.commit()
    conn.close()

# Metodo para seleccionar una de las palabras entre las tres categorias disponibles
def select_random_word():
    global word, guessed_word, category
    category = random.choice(list(word_categories.keys()))
    word = random.choice(word_categories[category]).upper()  #La transformamos en mayusculas
    guessed_word = "_" * len(word) #Creamos una variable en la que guardaremos la palabra oculta, escrita con guiones bajos

# Mostrar el juego
def show_game():
    global guessed_word, hangman_step, wrong_letters

    name_frame.pack_forget() #ocultamos el formulario usado para ingresar el nombre del jugador

