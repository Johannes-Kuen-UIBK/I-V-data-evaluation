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

    # Jede Datei einlesen und verarbeiten
    deviceArray = []
    for datei in txt_dateien:
        x_values = []
        y_values = []
        x_values2 = []
        y_values2 = []
        parameter_values = {}
        headers = []
        units = []
        values = []

        with open(datei, 'r') as file:
            for i, line in enumerate(file):
                if i == 3:
                    _, device = line.strip().split('\t')
                elif i == 32:
                    headers = line.strip().split('\t')  # Header aus Zeile 32 als Liste
                elif i == 33:
                    units = line.strip().split('\t')    # Einheiten aus Zeile 33 als Liste
                elif i == 34:
                    values = line.strip().split('\t')   # Werte aus Zeile 34 als Liste

                if 37 <= i:
                    data = line.strip().split('\t')
                    if len(data) == 4:
                        x, y, x_2, y_2 = data
                        x_values.append(float(x))
                        y_values.append(float(y))
                        x_values2.append(float(x_2))
                        y_values2.append(float(y_2))

        # Erstelle die Tabelle als Text
        table_text = " | ".join([f"{header} ({unit})" for header, unit in zip(headers, units)]) + "\n"
        table_text += "-" * len(table_text) + "\n"
        table_text += " | ".join(values) + "\n"

        inverted_y_values = [-1 * x for x in y_values]
        for i in deviceArray:
            if device in i:
                index = deviceArray.index(i)
                deviceArray[index].append([x_values, inverted_y_values, table_text])
        counter = 0
        for i in deviceArray:
            if device in i:
                counter -= 1
            counter += 1
        if counter == len(deviceArray) or len(deviceArray) == 0:
            deviceArray.append([device, [x_values, inverted_y_values, table_text]])

    # Die Graphenanzahl wird hier bereits vorher berechnet und angezeigt
    graph_count_label.config(text=f"graph count: {len(deviceArray)}")

    for i in deviceArray:
        for j in i:
            if i.index(j) >= 1:
                # Plot-Bereich verkleinern, um Platz für Text rechts zu schaffen
                fig, ax = plt.subplots()
                plt.subplots_adjust(right=0.75)  # Platz für den Text auf der rechten Seite lassen

                ax.plot(j[0], j[1], linestyle='-', marker='o', markersize=3)
                ax.set_xlim(-0.2, 1)
                ax.axvline(x=0, color='black', linewidth=1)
                ax.axhline(y=0, color='black', linewidth=1)
                ax.set_title(f"j/V HTL Perovskite cell, device: {i[0]}")
                ax.set_xlabel("U [V]")
                ax.set_ylabel("j [mA / cm2]")
                ax.grid(True)

                # Parameter-Werte im Tabellenformat neben dem Graphen anzeigen
                plt.text(1.02, 0.5, j[2], transform=ax.transAxes, fontsize=10,
                         verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5),
                         family='monospace')  # Monospace für bessere Tabellenausrichtung

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

select_button = tk.Button(root, text="foler select", command=select_folder)
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
