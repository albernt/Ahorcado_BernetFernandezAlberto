# Diccionarios de palabras organizadas en categorías
import random
import sqlite3
from tkinter import messagebox

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
    # Reinicio variables
    guessed_word = "_" * len(word)  # palabra oculta
    hangman_step = 0  # pasos del ahorcado
    wrong_letters.clear()  # las letras erroneas
    hangman_label.config(image=hangman_images[0])  # la imagen que muestra el avance del ahorcado
    guess_label.config(text=" ".join(guessed_word))  # progreso de la palabra
    category_label.config(text=f"Categoría: {category}")  # muestra la categoria a la que pertenece la palabra
    update_wrong_letters()  # llamamos a un metodo que desarrollamos mas abajo
    for button in letter_buttons:  # Creamos teclado
        button.config(state="normal")

    # Mostrar los widgets del juego
    game_frame.pack()

# Actualizar el texto del campo de "adivinanza"
def update_guess(letter):
    global guessed_word
    guessed_word = "".join([letter if word[i] == letter else guessed_word[i] for i in range(len(word))])
    guess_label.config(text=" ".join(guessed_word))
    if guessed_word == word:
        messagebox.showinfo("¡Felicidades!", "¡Has ganado!")
        save_game_result(won=True)
        disable_buttons()

# Desactivar los botones de las letras
def disable_buttons():
    for button in letter_buttons:
        button.config(state="disabled")

# Metodo para actualizar la etiqueta de letras incorrectas
def update_wrong_letters():
    wrong_letters_label.config(text=f"Letras incorrectas: {', '.join(sorted(wrong_letters))}")

# Metodo para cargar las imagenes de la 1 a la 8 en funcion de los pasos
def load_hangman_images():
    images = []
    for i in range(1, 9):
        img = Image.open(f"hangman{i}.png")
        img = img.resize((200, 200), Image.Resampling.LANCZOS)
        images.append(ImageTk.PhotoImage(img))
    return images


# Función para manejar el clic en los botones de las letras
def button_click(letter):
    if letter in word:
        update_guess(letter)
    else:
        wrong_letters.add(letter)
        update_wrong_letters()
        update_hangman_image()

