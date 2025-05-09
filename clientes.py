import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import os

# Archivo donde se guardan los clientes
ARCHIVO = 'clientes.csv'

# Guardar un nuevo cliente
def guardar_cliente():
    nombre = entry_nombre.get()
    fecha = entry_fecha.get()

    if not nombre or not fecha:
        messagebox.showwarning("Campos vacíos", "Por favor ingrese todos los campos.")
        return

    try:
        fecha_obj = datetime.strptime(fecha, "%d/%m/%Y")
    except ValueError:
        messagebox.showerror("Error de fecha", "Por favor, ingrese la fecha en formato dd/mm/aaaa.")
        return

    with open(ARCHIVO, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nombre, fecha_obj.strftime("%d/%m/%Y")])
    
    messagebox.showinfo("Éxito", f"Cliente {nombre} registrado.")
    entry_nombre.delete(0, tk.END)
    entry_fecha.delete(0, tk.END)
    cargar_clientes()

# Cargar clientes en la lista
def cargar_clientes():
    listbox_clientes.delete(0, tk.END)
    advertencias = []

    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, newline='') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                nombre, fecha_str = row
                try:
                    fecha_obj = datetime.strptime(fecha_str, "%d/%m/%Y")
                    dias_faltantes = (fecha_obj - datetime.today()).days
                    if 0 <= dias_faltantes <= 7:
                        advertencias.append(f"{nombre} - renovación en {dias_faltantes} días")
                        listbox_clientes.insert(tk.END, f"🔔 {nombre} - {fecha_str}")
                    else:
                        listbox_clientes.insert(tk.END, f"{nombre} - {fecha_str}")
                except ValueError:
                    listbox_clientes.insert(tk.END, f"{nombre} - {fecha_str} (fecha inválida)")

    # Mostrar advertencia si hay renovaciones próximas
    if advertencias:
        mensaje = "Clientes con renovación próxima:\n\n" + "\n".join(advertencias)
        messagebox.showwarning("¡Atención!", mensaje)

# Eliminar cliente seleccionado
def eliminar_cliente():
    seleccion = listbox_clientes.curselection()
    if not seleccion:
        messagebox.showwarning("Ninguna selección", "Seleccione un cliente para eliminar.")
        return

    index = seleccion[0]
    confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?")
    if confirmar:
        with open(ARCHIVO, newline='') as file:
            rows = list(csv.reader(file))
        rows.pop(index)
        with open(ARCHIVO, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        cargar_clientes()
        messagebox.showinfo("Eliminado", "Cliente eliminado correctamente.")

# Guardar índice global para saber a quién estamos editando
indice_edicion = None

def editar_cliente():
    global indice_edicion
    seleccion = listbox_clientes.curselection()
    if not seleccion:
        messagebox.showwarning("Ninguna selección", "Seleccione un cliente para editar.")
        return

    indice_edicion = seleccion[0]

    with open(ARCHIVO, newline='') as file:
        filas = list(csv.reader(file))
        nombre, fecha = filas[indice_edicion]
        entry_nombre.delete(0, tk.END)
        entry_fecha.delete(0, tk.END)
        entry_nombre.insert(0, nombre)
        entry_fecha.insert(0, fecha)

    # Cambiar el texto y acción del botón de guardar
    boton_guardar.config(text="Actualizar Cliente", command=actualizar_cliente)

def actualizar_cliente():
    global indice_edicion
    nombre = entry_nombre.get()
    fecha = entry_fecha.get()

    if not nombre or not fecha:
        messagebox.showwarning("Campos vacíos", "Por favor ingrese todos los campos.")
        return

    try:
        fecha_obj = datetime.strptime(fecha, "%d/%m/%Y")
    except ValueError:
        messagebox.showerror("Error de fecha", "Ingrese la fecha en formato dd/mm/aaaa.")
        return

    # Leer todos los registros
    with open(ARCHIVO, newline='') as file:
        filas = list(csv.reader(file))
    
    # Actualizar solo el que se está editando
    filas[indice_edicion] = [nombre, fecha_obj.strftime("%d/%m/%Y")]

    # Guardar todos de nuevo
    with open(ARCHIVO, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(filas)

    # Limpiar los campos
    entry_nombre.delete(0, tk.END)
    entry_fecha.delete(0, tk.END)

    # Volver el botón a "Guardar Cliente"
    boton_guardar.config(text="Guardar Cliente", command=guardar_cliente)

    # Recargar lista y mensaje
    cargar_clientes()
    messagebox.showinfo("Actualizado", "Cliente actualizado correctamente.")



# Crear ventana principal
ventana = tk.Tk()
ventana.title("Gestión de Clientes")
ventana.geometry("500x450")

# Campos
tk.Label(ventana, text="Nombre del Cliente:").pack(pady=5)
entry_nombre = tk.Entry(ventana, width=40)
entry_nombre.pack(pady=5)

tk.Label(ventana, text="Fecha de Renovación (dd/mm/aaaa):").pack(pady=5)
entry_fecha = tk.Entry(ventana, width=40)
entry_fecha.pack(pady=5)

# Botón guardar
boton_guardar = tk.Button(ventana, text="Guardar Cliente", command=guardar_cliente)
boton_guardar.pack(pady=10)


# Lista de clientes
tk.Label(ventana, text="Clientes registrados:").pack(pady=5)
listbox_clientes = tk.Listbox(ventana, width=60)
listbox_clientes.pack(pady=5)

# Botón eliminar
tk.Button(ventana, text="Eliminar Cliente Seleccionado", command=eliminar_cliente).pack(pady=10)

# Botón para editar
tk.Button(ventana, text="Editar Cliente Seleccionado", command=editar_cliente).pack(pady=5)

# Cargar lista al iniciar
cargar_clientes()

# Ejecutar
ventana.mainloop()
