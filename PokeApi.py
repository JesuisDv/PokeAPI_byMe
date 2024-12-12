import tkinter as tk
from tkinter import messagebox
import requests
from tkinter import font

#* Obtener busqueda del usuario
def buscar_pokemon():
    pokemon = entrada.get().lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"

#* Solicitar a la API
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        #* Extraer la info de la API
        nombre = data['name'].capitalize()
        habilidades = [ability['ability']['name']for ability in data['abilities']]
        stats = {stat['stat']['name']:stat['base_stat']for stat in data['stats']}
        image_url = data['sprites']['front_default']
        
        #* Mostrar info en cuadro de texto
        resultado.delete(1.0, tk.END)
        resultado.insert(tk.END, f"Nombre: {nombre}\n")
        resultado.insert(tk.END, f"Habilidades: {', '.join(habilidades)}\n")
        resultado.insert(tk.END, f"Estadisticas:\n")
        for stat, value in stats.items():
            resultado.insert(tk.END, f"  {stat.capitalize()}: {value}\n")
            
        
        #* mostrar imagen
        if image_url:
            mostrar_imagen(image_url)
            
    else:
        messagebox.showerror('Error', f'{pokemon} no fue encontrado')
    
def mostrar_imagen(url):
    try:
        from PIL import Image, ImageTk
        import requests
        from io import BytesIO
        
        response = requests.get(url)
        if response.status_code == 200:
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img = img.resize((200,200))
            img_tk = ImageTk.PhotoImage(img)
            
            image_label.config(image=img_tk)
            image_label.image = img_tk
            
    except ImportError:
        resultado.insert(tk.END, "\n(No se pudo mostrar la imagen)")
        
        
        
#* Creacion de la ventana
root = tk.Tk()
root.title('PokeAPI')
root.geometry('400x500')
root.configure( bg="#d22b2b")

try:
    fuente_pokemon = font.Font(file="Arial", size=12)
except Exception as e:
    print(f"No se pudo cargar la fuente: {e}")
    fuente_pokemon = font.nametofont("TkDefaultFont")

#* Barra de busqueda
entrada = tk.Entry(root, width=30, font=fuente_pokemon)
entrada.pack(pady=10)

#* Boton de busqueda
boton = tk.Button(root, text='Buscar Pokemon', command=buscar_pokemon , font=fuente_pokemon, bg='#ffff42')
boton.pack(pady=10)

#* Mostrar resultados
resultado = tk.Text(root, height=10, width= 40,font=fuente_pokemon ,bg= '#43cbf8' )
resultado.pack(pady= 10)

#* Mostrar imagen
image_label = tk.Label(root,  bg= "#d22b2b")
image_label.pack(pady=5)

root.mainloop()    
    