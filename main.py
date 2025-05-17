import tkinter as tk
from tkinter import simpledialog, messagebox
from pytz import timezone
from datetime import datetime, timedelta


def atualizar_relogio():
  brasilia = timezone('America/Sao_Paulo')
  sao_paulo_time = datetime.now(brasilia)
  hora_atual = sao_paulo_time.strftime("%H:%M:%S")

  label_relogio.config(text=hora_atual)

  proximo_segundo = sao_paulo_time.replace(microsecond=0) + timedelta(
      seconds=1)
  tempo_ate_proximo_segundo = (proximo_segundo -
                               sao_paulo_time).total_seconds() * 1000

  root.after(int(tempo_ate_proximo_segundo), atualizar_relogio)


def definir_alarme():
  hora_alarme_str = simpledialog.askstring("DEFINIR ALARME",
                                           "Digite a hora do alarme (HH:MM):")

  if hora_alarme_str is not None:
    try:
      hora_alarme = datetime.strptime(hora_alarme_str, "%H:%M")
      botao_alarme.config(state="disabled")
      botao_soneca.config(state="normal")
      botao_parar.config(state="normal")
      root.after(1000, verificar_alarme, hora_alarme)
    except ValueError:
      tk.messagebox.showerror("Erro", "Formato de hora inválido. Use HH:MM.")


def verificar_alarme(hora_alarme):
  hora_atual = datetime.now(brasilia).strftime("%H:%M")
  if hora_atual == hora_alarme.strftime("%H:%M"):
    tk.messagebox.showinfo("Alarme", "Hora do alarme!")
    botao_alarme.config(state="normal")
    botao_soneca.config(state="disabled")
    botao_parar.config(state="disabled")
  else:
    root.after(1000, verificar_alarme, hora_alarme)


def soneca():
  hora_atual = datetime.now(brasilia)
  novo_hora_alarme = hora_atual + timedelta(minutes=10)
  tk.messagebox.showinfo(
      "SONECA", f"Alarme adiado para {novo_hora_alarme.strftime('%H:%M')}")
  root.after(1000, verificar_alarme, novo_hora_alarme)


def parar_alarme():
  botao_alarme.config(state="normal")
  botao_soneca.config(state="disabled")
  botao_parar.config(state="disabled")


root = tk.Tk()
root.title("Despertador do Wagner")
root.geometry("600x300")
root.configure(bg="white")
root.resizable(False, False)

brasilia = timezone('America/Sao_Paulo')

frame_controle = tk.Frame(root, bg="white")
frame_controle.pack(anchor="ne", padx=10, pady=5)

label_relogio = tk.Label(root,
                         text="",
                         font=("Times New Roman", 24),
                         fg="black")
label_relogio.configure(bg="White")
label_relogio.pack(pady=20, padx=10, fill='both', expand=True)

botao_alarme = tk.Button(root, text="DEFINIR ALARME", command=definir_alarme)
botao_alarme.config(bg="red")
botao_alarme.pack(pady=10)

botao_soneca = tk.Button(root,
                         text="SONECA (10min)",
                         command=soneca,
                         state="disabled")
botao_soneca.config(bg="red")
botao_soneca.pack(pady=10)

botao_parar = tk.Button(root,
                        text="PARAR ALARME",
                        command=parar_alarme,
                        state="disabled")
botao_parar.config(bg="red")
botao_parar.pack(pady=10)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

atualizar_relogio()

root.mainloop()

