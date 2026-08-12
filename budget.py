import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#dati
try:
    df = pd.read_csv("budget.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["descrizione", "denaro", "categoria"])

#finestra
root = tk.Tk()
root.title("💰 Budget Tracker")
root.geometry("850x550")

frame_sinistro = tk.Frame(root, padx=15, pady=15)
frame_sinistro.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

frame_destro = tk.Frame(root, padx=15, pady=15)
frame_destro.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

#input
tk.Label(frame_sinistro, text="Descrizione:").pack(anchor="w", pady=(0, 2))
entry_desc = tk.Entry(frame_sinistro, width=30)
entry_desc.pack(fill=tk.X, pady=(0, 10))

tk.Label(frame_sinistro, text="Importo (€):").pack(anchor="w", pady=(0, 2))
entry_denaro = tk.Entry(frame_sinistro, width=30)
entry_denaro.pack(fill=tk.X, pady=(0, 10))

tk.Label(frame_sinistro, text="Categoria:").pack(anchor="w", pady=(0, 2))
combo_cat = ttk.Combobox(frame_sinistro, values=["Cibo", "Svago", "Trasporti", "Casa", "Altro"])
combo_cat.current(0)
combo_cat.pack(fill=tk.X, pady=(0, 15))

#funzione per aggiornare il grafico e le statistiche
fig, ax = plt.subplots(figsize=(4, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_destro)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

lbl_stats = tk.Label(frame_sinistro, text="", justify=tk.LEFT, font=("Arial", 10, "bold"))
lbl_stats.pack(anchor="w", pady=10)

def aggiorna_vista():
    global df
    ax.clear()
    
    if not df.empty:
        #calcolo statistiche
        tot = df["denaro"].sum()
        med = df["denaro"].mean()
        mass = df["denaro"].max()
        lbl_stats.config(text=f"Totale: {tot:.2f} €\nMedia: {med:.2f} €\nMax: {mass:.2f} €")
        
        #grafico a torta
        spese_cat = df.groupby("categoria")["denaro"].sum()
        spese_cat.plot(kind="pie", autopct="%1.1f%%", ax=ax)
        ax.set_ylabel("")
        ax.set_title("Spese per Categoria")
    else:
        lbl_stats.config(text="Nessuna spesa registrata.")
        
    canvas.draw()

#funzione per salvare la spesa
def aggiungi_spesa():
    global df
    desc = entry_desc.get().strip()
    cat = combo_cat.get().strip()
    
    try:
        denaro = float(entry_denaro.get().replace(",", "."))
    except ValueError:
        messagebox.showerror("Errore", "Inserisci un numero valido per l'importo.")
        return

    if not desc:
        messagebox.showwarning("Attenzione", "Inserisci una descrizione.")
        return

    #aggiungi riga e salva CSV
    nuova_riga = pd.DataFrame({"descrizione": [desc], "denaro": [denaro], "categoria": [cat]})
    df = pd.concat([df, nuova_riga], ignore_index=True)
    df.to_csv("budget.csv", index=False)

    #pulisci i campi
    entry_desc.delete(0, tk.END)
    entry_denaro.delete(0, tk.END)

    aggiorna_vista()

#bottone invio
btn_aggiungi = tk.Button(frame_sinistro, text="➕ Aggiungi Spesa", command=aggiungi_spesa, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn_aggiungi.pack(fill=tk.X, pady=10)

#avvio iniziale
aggiorna_vista()
root.mainloop()