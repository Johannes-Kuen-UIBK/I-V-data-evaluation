import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib import pyplot as plt
import numpy as np
import os
import glob

def select_folder():
    global ordner_pfad
    ordner_pfad = filedialog.askdirectory()
    if ordner_pfad:
        folder_label.config(text=f"Ordner: {ordner_pfad}")
    else:
        folder_label.config(text="Kein Ordner ausgewählt")

def show_graph():
    if not ordner_pfad:
        messagebox.showerror("Fehler", "Bitte wähle zuerst einen Ordner aus!")
        return

    # Alle .txt-Dateien im Ordner finden
    txt_dateien = glob.glob(os.path.join(ordner_pfad, '*.txt'))

    if not txt_dateien:
        messagebox.showerror("Fehler", "Keine .txt-Dateien im ausgewählten Ordner gefunden!")
        return

    # Jede Datei einlesen und verarbeiten
    deviceArray = []
    for datei in txt_dateien:
        x_values = []
        y_values = []
        x_values2 = []
        y_values2 = []

        with open(datei, 'r') as file:
            for i, line in enumerate(file):
                if i == 3:
                    _, device = line.strip().split('\t')

                if 37 <= i:
                    values = line.strip().split('\t')
                    if len(values) == 4:
                        x, y, x_2, y_2 = values
                        x_values.append(float(x))
                        y_values.append(float(y))
                        x_values2.append(float(x_2))
                        y_values2.append(float(y_2))

        inverted_y_values = [-1 * x for x in y_values]
        for i in deviceArray:
            if device in i:
                index = deviceArray.index(i)
                deviceArray[index].append([x_values, inverted_y_values])
        counter = 0
        for i in deviceArray:
            if device in i:
                counter -= 1
            counter += 1
        if counter == len(deviceArray) or len(deviceArray) == 0:
            deviceArray.append([device, [x_values, inverted_y_values]])

    print(len(deviceArray))

    for i in deviceArray:
        for j in i:
            if i.index(j) >= 1:
                plt.plot(j[0], j[1], linestyle='-', marker='o', markersize=3)
                plt.xlim(-0.2, 1)
                plt.axvline(x=0, color='black', linewidth=1)
                plt.axhline(y=0, color='black', linewidth=1)
                plt.title(f"I/V HTL Perovskite cell, device: {i[0]}")
                plt.xlabel("V")
                plt.ylabel("j [mV / cm2]")
                plt.grid(True)
        plt.show()

# Hauptfenster erstellen
root = tk.Tk()
root.title("I/V Graph Plotter ver. 23.08.2024")

# Fenstergröße festlegen (Breite x Höhe)
root.geometry("600x400")  # Hier wird das Fenster auf 600x400 Pixel gesetzt

ordner_pfad = ""

# GUI-Elemente
folder_label = tk.Label(root, text="no folder selected", wraplength=400)
folder_label.pack(pady=10)


select_button = tk.Button(root, text="select folder", command=select_folder)
select_button.pack(pady=5)

plot_button = tk.Button(root, text="Show Graph", command=show_graph)
plot_button.pack(pady=20)

# Versionsnummer und Datum unten im Fenster
footer_label = tk.Label(root, text="ver 1.0 | 08.2024")
footer_label.pack(side="bottom", pady=5)  # Setzt das Label an den unteren Rand

# GUI starten
root.mainloop()
