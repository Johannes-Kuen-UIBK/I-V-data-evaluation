import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib import pyplot as plt
import numpy as np
import os
import glob

# Globale Variable für das Speicherverzeichnis
save_directory = ""

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
    if ordner_pfad:
        txt_dateien = glob.glob(os.path.join(ordner_pfad, '*.txt'))
        file_count_label.config(text=f"found .txt-Dateien: {len(txt_dateien)}")
    else:
        file_count_label.config(text="found .txt-Dateien: 0")

def update_graph_count():
    if ordner_pfad:
        txt_dateien = glob.glob(os.path.join(ordner_pfad, '*.txt'))
        deviceArray = []
        for datei in txt_dateien:
            with open(datei, 'r', encoding='iso-8859-1') as file:
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

    txt_dateien = glob.glob(os.path.join(ordner_pfad, '*.txt'))

    if not txt_dateien:
        messagebox.showerror("Error", "no .txt-Data in selected folder!")
        return

    device_dict = {}

    for datei in txt_dateien:
        x_values = []
        y_values = []
        last_value = None  # Nur der letzte Wert aus Zeile 34

        with open(datei, 'r', encoding='iso-8859-1') as file:
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

        inverted_y_values = [-1 * x for x in y_values]

        if device not in device_dict:
            device_dict[device] = []
        device_dict[device].append([x_values, inverted_y_values, last_value])

    graph_count_label.config(text=f"graph count: {len(device_dict)}")

    for device, curves in device_dict.items():
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.subplots_adjust(right=0.75)

        for curve in curves:
            x_values, inverted_y_values, last_value = curve
            ax.plot(x_values, inverted_y_values, linestyle='-', marker='o', markersize=3,
                    label=f"efficiency: {last_value}%")

        ax.set_xlim(-0.2, 1.1)
        ax.set_ylim(-22, 5)
        ax.axvline(x=0, color='black', linewidth=1)
        ax.axhline(y=0, color='black', linewidth=1)
        ax.set_title(f"j/V HTL Perovskite cell, device: {device}")
        ax.set_xlabel("U [V]")
        ax.set_ylabel("j [mA / cm2]")
        ax.grid(True)

        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Efficiency Values")
        plt.show()

def save_plot():
    global save_directory
    save_directory = filedialog.askdirectory()
    if save_directory:
        save_directory_label.config(text=f"Save Directory: {save_directory}")
    else:
        save_directory_label.config(text="No save directory selected")

def save_all_graphs():
    if not ordner_pfad:
        messagebox.showerror("Error", "first select a folder!")
        return

    if not save_directory:
        messagebox.showerror("Error", "first select a save directory!")
        return

    txt_dateien = glob.glob(os.path.join(ordner_pfad, '*.txt'))

    if not txt_dateien:
        messagebox.showerror("Error", "no .txt-Data in selected folder!")
        return

    device_dict = {}

    for datei in txt_dateien:
        x_values = []
        y_values = []
        last_value = None

        with open(datei, 'r', encoding='iso-8859-1') as file:
            for i, line in enumerate(file):
                if i == 3:
                    _, device = line.strip().split('\t')
                elif i == 32:
                    headers = line.strip().split('\t')
                elif i == 34:
                    values = line.strip().split('\t')
                    last_value = values[-1]

                if 37 <= i:
                    data = line.strip().split('\t')
                    if len(data) == 4:
                        x, y, _, _ = data
                        x_values.append(float(x))
                        y_values.append(float(y))

        inverted_y_values = [-1 * x for x in y_values]

        if device not in device_dict:
            device_dict[device] = []
        device_dict[device].append([x_values, inverted_y_values, last_value])

    graph_count_label.config(text=f"graph count: {len(device_dict)}")

    # Speichere alle Graphen
    for device, curves in device_dict.items():
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.subplots_adjust(right=0.75)

        for curve in curves:
            x_values, inverted_y_values, last_value = curve
            ax.plot(x_values, inverted_y_values, linestyle='-', marker='o', markersize=3,
                    label=f"efficiency: {last_value}%")

        ax.set_xlim(-0.2, 1.1)
        ax.set_ylim(-22, 5)
        ax.axvline(x=0, color='black', linewidth=1)
        ax.axhline(y=0, color='black', linewidth=1)
        ax.set_title(f"j/V HTL Perovskite cell, device: {device}")
        ax.set_xlabel("U [V]")
        ax.set_ylabel("j [mA / cm2]")
        ax.grid(True)

        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Efficiency Values")

        # Speichern in das ausgewählte Verzeichnis
        save_path = os.path.join(save_directory, f"{device}_graph.png")
        plt.savefig(save_path)
        plt.close()  # Schließe den Plot nach dem Speichern

    messagebox.showinfo("Success", f"All graphs saved in {save_directory}")

# Hauptfenster erstellen
root = tk.Tk()
root.title("j/V Graph Plotter")

# Fenstergröße festlegen

# Bildschirmauflösung abrufen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Fenstergröße auf 50% der Bildschirmauflösung setzen
width = int(screen_width * 0.3)
height = int(screen_height * 0.4)

# Zentrieren des Fensters auf dem Bildschirm
x = int((screen_width - width) / 2)
y = int((screen_height - height) / 2)

# Setze die Größe und Position des Fensters
root.geometry(f'{width}x{height}+{x}+{y}')

ordner_pfad = ""

# GUI-Elemente
folder_label = tk.Label(root, text="no folder selected", wraplength=400)
folder_label.pack(pady=10)

select_button = tk.Button(root, text="Select Folder", command=select_folder)
select_button.pack(pady=5)

file_count_label = tk.Label(root, text="found .txt-files: 0")
file_count_label.pack(pady=5)

graph_count_label = tk.Label(root, text="graph count: 0")
graph_count_label.pack(pady=5)

plot_button = tk.Button(root, text="Show Graph", command=show_graph)
plot_button.pack(pady=20)

# Button und Label für das Speichern von Graphen
save_button = tk.Button(root, text="Select Save Directory", command=save_plot)
save_button.pack(pady=10)

save_directory_label = tk.Label(root, text="No save directory selected")
save_directory_label.pack(pady=5)

# Button zum automatischen Speichern aller Graphen
save_all_button = tk.Button(root, text="Save All Graphs", command=save_all_graphs)
save_all_button.pack(pady=10)

footer_label = tk.Label(root, text="ver 1.0 | 09.2024")
footer_label.pack(side="bottom", pady=5)

# GUI starten
root.mainloop()
