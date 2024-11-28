import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import sqlite3


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

#  Metodo para actualizar los pasos del estado del ahorcado
def update_hangman_image():
    global hangman_step
    hangman_step += 1
    if hangman_step < len(hangman_images):
        hangman_label.config(image=hangman_images[hangman_step])
    if hangman_step == max_steps:
        messagebox.showinfo("Fin del juego", f"¡Perdiste! La palabra era: {word}")
        save_game_result(won=False)
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

# Configuración inicial
init_db()
select_random_word()

# Creacion de la ventana principal
root = tk.Tk()
root.title("Juego del Ahorcado") #titulo
root.geometry("420x700") #tamaño ventana
root.resizable(False, False) #redimensionamiento desactivado
root.configure(bg="#fdf5e6")

# Cargar las imágenes
hangman_images = load_hangman_images()

# Crear el formulario para el nombre
name_frame = tk.Frame(root, bg="#fdf5e6")
name_frame.pack(pady=20)
tk.Label(name_frame, text="Introduce tu nombre:", font=("Arial", 16), bg="#fdf5e6").pack(pady=10)
name_entry = tk.Entry(name_frame, font=("Arial", 14))
name_entry.pack(pady=10)

def start_game():
    global player_name
    player_name = name_entry.get().strip()
    if player_name:
        show_game()
    else:
        messagebox.showerror("Error", "Por favor, introduce tu nombre.")


tk.Button(name_frame, text="Comenzar Juego", font=("Arial", 14), bg="#ffccbc", fg="#bf360c",
          command=start_game).pack(pady=10)

# Crear el marco del juego
game_frame = tk.Frame(root, bg="#fdf5e6")  #contenedor del juego con el color de fondo pastel
image_frame = tk.Frame(game_frame, bg="#fce4ec", highlightbackground="#f48fb1", highlightthickness=3)
image_frame.pack(pady=10) #creamos un subcontenedor para colocarle las imagenes del ahorcado
hangman_label = tk.Label(image_frame, image=hangman_images[0], bg="#fce4ec") #colocamos la imagen del ahorcado dentro de ese subcontenedor
hangman_label.pack()

category_label = tk.Label(game_frame, text=f"Categoría: {category}", font=("Arial", 18), bg="#fdf5e6", fg="#5c6bc0") #etiqueta para mostrar la categoria
category_label.pack(pady=10)

guess_label = tk.Label(game_frame, text=" ".join(guessed_word), font=("Arial", 24), bg="#fdf5e6", fg="#66bb6a") #label para mostrar el progreso de la palabra
guess_label.pack(pady=10)

wrong_letters_label = tk.Label(game_frame, text="Letras incorrectas: ", font=("Arial", 14), bg="#fdf5e6", fg="#ef5350") #label para mostrar las letras incorrectas
wrong_letters_label.pack(pady=10)

frame = tk.Frame(game_frame, bg="#fdf5e6")
frame.pack(pady=10)

letter_buttons = []
for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"): #creamos el teclado introduciendo las letras en una lista
    button = tk.Button(frame, text=letter, width=4, bg="#d1c4e9", fg="#212121", font=("Arial", 10),
                       activebackground="#b39ddb", command=lambda l=letter: button_click(l))
    button.grid(row=i // 9, column=i % 9) #usamos un grid para organizarlos dentro del frame
    letter_buttons.append(button)

# Iniciar el bucle principal
root.mainloop()