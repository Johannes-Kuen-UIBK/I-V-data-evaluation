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
        folder_label.config(text=f"folder: {ordner_pfad}")
        update_file_count()
        update_graph_count()  # Aktualisiere die Graphenanzahl nach der Ordnerauswahl
    else:
        folder_label.config(text="no folder selected")

def update_file_count():
    # Zähle die Anzahl der .txt-Dateien im ausgewählten Ordner
    if ordner_pfad:
        txt_dateien = glob.glob(os.path.join(ordner_pfad, '*.txt'))
        file_count_label.config(text=f"found .txt-Dateien: {len(txt_dateien)}")
    else:
        file_count_label.config(text="found .txt-Dateien: 0")

def update_graph_count():
    # Zähle die Anzahl der Graphen, die erstellt werden könnten
    if ordner_pfad:
        txt_dateien = glob.glob(os.path.join(ordner_pfad, '*.txt'))
        deviceArray = []
        for datei in txt_dateien:
            with open(datei, 'r') as file:
                for i, line in enumerate(file):
                    if i == 3:
                        _, device = line.strip().split('\t')

                    if 37 <= i:
                        values = line.strip().split('\t')
                        if len(values) == 4:
                            break

            for i in deviceArray:
                if device in i:
                    index = deviceArray.index(i)
                    deviceArray[index].append(device)
            counter = 0
            for i in deviceArray:
                if device in i:
                    counter -= 1
                counter += 1
            if counter == len(deviceArray) or len(deviceArray) == 0:
                deviceArray.append([device])

        graph_count_label.config(text=f"graph count: {len(deviceArray)}")
    else:
        graph_count_label.config(text="graph count: 0")

def show_graph():
    if not ordner_pfad:
        messagebox.showerror("Error", "first select a folder!")
        return

    # Alle .txt-Dateien im Ordner finden
    txt_dateien = glob.glob(os.path.join(ordner_pfad, '*.txt'))

    if not txt_dateien:
        messagebox.showerror("Error", "no .txt-Data in selected folder!")
        return

    # Gerätedaten als Dictionary organisieren: {device_name: [[x_values, inverted_y_values, last_value]]}
    device_dict = {}

    for datei in txt_dateien:
        x_values = []
        y_values = []
        last_value = None  # Nur der letzte Wert aus Zeile 34

        with open(datei, 'r') as file:
            for i, line in enumerate(file):
                if i == 3:
                    _, device = line.strip().split('\t')  # Gerät in Zeile 3
                elif i == 32:
                    headers = line.strip().split('\t')  # Header aus Zeile 32
                elif i == 34:
                    values = line.strip().split('\t')  # Werte aus Zeile 34
                    last_value = values[-1]  # Letzter Wert aus Zeile 34

                if 37 <= i:
                    data = line.strip().split('\t')
                    if len(data) == 4:
                        x, y, _, _ = data
                        x_values.append(float(x))
                        y_values.append(float(y))

        # Invertierte y-Werte für das Diagramm
        inverted_y_values = [-1 * x for x in y_values]

        # Gerätedaten in Dictionary speichern
        if device not in device_dict:
            device_dict[device] = []
        device_dict[device].append([x_values, inverted_y_values, last_value])

    # Graphenanzahl aktualisieren
    graph_count_label.config(text=f"graph count: {len(device_dict)}")

    # Plots für jedes Gerät erstellen
    for device, curves in device_dict.items():
        fig, ax = plt.subplots(figsize=(10, 6))  # Größe des Fensters anpassen: Breiter machen
        plt.subplots_adjust(right=0.75)  # Platz für den Text auf der rechten Seite lassen

    # Alle Kurven für das Gerät in einem Diagramm anzeigen
        for curve in curves:
            x_values, inverted_y_values, last_value = curve
            ax.plot(x_values, inverted_y_values, linestyle='-', marker='o', markersize=3,
                    label=f"efficiency: {last_value}%")

        ax.set_xlim(-0.2, 1)
        ax.axvline(x=0, color='black', linewidth=1)
        ax.axhline(y=0, color='black', linewidth=1)
        ax.set_title(f"j/V HTL Perovskite cell, device: {device}")
        ax.set_xlabel("U [V]")
        ax.set_ylabel("j [mA / cm2]")
        ax.grid(True)

        # Legende für jeden letzten Wert aus Zeile 34 als "efficiency: xx%"
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Efficiency Values")
        plt.show()

# Hauptfenster erstellen
root = tk.Tk()
root.title("j/V Graph Plotter")

# Fenstergröße festlegen
root.geometry("600x400")  # Setzt das Fenster auf 600x400 Pixel

ordner_pfad = ""

# GUI-Elemente
folder_label = tk.Label(root, text="no folder selected", wraplength=400)
folder_label.pack(pady=10)

select_button = tk.Button(root, text="folder select", command=select_folder)
select_button.pack(pady=5)

file_count_label = tk.Label(root, text="found .txt-files: 0")
file_count_label.pack(pady=5)

# Anzeige der Graphenanzahl vor dem Plotten
graph_count_label = tk.Label(root, text="graph count: 0")
graph_count_label.pack(pady=5)

plot_button = tk.Button(root, text="Show Graph", command=show_graph)
plot_button.pack(pady=20)

# Versionsnummer und Datum unten im Fenster
footer_label = tk.Label(root, text="ver 1.0 | 08.2024")
footer_label.pack(side="bottom", pady=5)  # Setzt das Label an den unteren Rand

# GUI starten
root.mainloop()
