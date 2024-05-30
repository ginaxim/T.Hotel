import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect('reservas.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS reservas (
             id INTEGER PRIMARY KEY,
             hora TEXT NOT NULL,
             tempo_espera TEXT NOT NULL,
             matricula TEXT NOT NULL,
             camas INTEGER NOT NULL
             )''')
conn.commit()

def validar_hora(hora):
    if len(hora) != 5 or hora[2] != ":":
        return False
    try:
        horas, minutos = map(int, hora.split(":"))
        if horas < 0 or horas > 23 or minutos < 0 or minutos > 59:
            return False
    except ValueError:
        return False
    return True

def reservar_quarto():
    hora = entry_hora.get()
    tempo_espera = int(entry_tempo_espera.get())
    matricula = entry_matricula.get()
    camas = entry_camas.get()

    if not validar_hora(hora):
        messagebox.showerror("Reserva de Quarto no Hotel Estácio", "Formato de hora inválido. Use o formato HH:MM (00:00 - 23:59).")
        return
    
    hora = int(hora.split(":")[0])

    if not camas.isdigit() or int(camas) < 1 or int(camas) > 5:
        messagebox.showerror("Reserva de Quarto no Hotel Estácio", "O número de quartos deve estar entre 1 e 5.")
        return
    
    c.execute("SELECT * FROM reservas WHERE camas=? AND hora =? ", (camas,hora))
    if c.fetchone():
        messagebox.showerror("Reserva de Quarto no Hotel Estácio", "Este quarto já está reservado.")
    else:
        if matricula == "123456":
            messagebox.showinfo("Reserva de Quarto no Hotel Estácio", f"Hora da reserva: {hora}\nTempo esperado: {tempo_espera}\nO aluno é matriculado e a matrícula é válida.\nNúmero de quartos: {camas}")

            for horario in range(tempo_espera):
                print(hora+horario)
                c.execute("INSERT INTO reservas (hora, tempo_espera, matricula, camas) VALUES (?, ?, ?, ?)", (hora+horario, tempo_espera, matricula, camas))
                conn.commit()
        else:
            messagebox.showerror("Reserva de Quarto no Hotel Estácio", "A matrícula não é válida.")

root = tk.Tk()
root.title("Reserva de Quarto no Hotel Estácio")

frame = tk.Frame(root, bg="#ADD8E6")
frame.pack(padx=10, pady=10)

label_hora = tk.Label(frame, text="Hora da reserva:", bg="#ADD8E6", font=("Arial", 12))
label_hora.grid(row=0, column=0, padx=(0, 10))

entry_hora = tk.Entry(frame, font=("Arial", 12))
entry_hora.grid(row=0, column=1)

label_tempo_espera = tk.Label(frame, text="Tempo esperado:", bg="#ADD8E6", font=("Arial", 12))
label_tempo_espera.grid(row=1, column=0, padx=(0, 10))

entry_tempo_espera = tk.Entry(frame, font=("Arial", 12))
entry_tempo_espera.grid(row=1, column=1)

label_matricula = tk.Label(frame, text="Matricula:", bg="#ADD8E6", font=("Arial", 12))
label_matricula.grid(row=2, column=0, padx=(0, 10))

entry_matricula = tk.Entry(frame, font=("Arial", 12))
entry_matricula.grid(row=2, column=1)

label_camas = tk.Label(frame, text="Número do Quarto:", bg="#ADD8E6", font=("Arial", 12))
label_camas.grid(row=3, column=0, padx=(0, 10))

entry_camas = tk.Entry(frame, font=("Arial", 12))
entry_camas.grid(row=3, column=1)

button_reservar = tk.Button(frame, text="Reservar Quarto", command=reservar_quarto, bg="#ADD8E6", font=("Arial", 12))
button_reservar.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()