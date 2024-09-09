from matplotlib import pyplot as plt
import numpy as np
import os
import glob



# Pfad zum Ordner mit den .txt-Dateien
ordner_pfad = f'C:/Users/c8461464/Documents/Re__new_ITO_Cu_NiOx_samples_for_FlexPecs (2)'

# Alle .txt-Dateien im Ordner finden
txt_dateien = glob.glob(os.path.join(ordner_pfad, '*.txt'))
# Jede Datei einlesen und verarbeiten
deviceArray = []
for datei in txt_dateien:
    x_values = []
    y_values = []
    x_values2 = []
    y_values2 = []

    with open(datei, 'r') as file:

        # Datei Zeile für Zeile durchgehen
        for i, line in enumerate(file):
            if i == 3:
                _, device = line.strip().split('\t')

            # Überprüfen, ob wir uns im gewünschten Zeilenbereich befinden
            if 37 <= i:
                # Zeile nach Tabulator getrennt in x- und y-Wert aufteilen
                values = line.strip().split('\t')
                # y, rest = rest.strip().split('\t')
                # x_2 , y_2 = rest.strip().split('\t')
                # Werte zu den Listen hinzufügen

                if len(values) == 4:  # Überprüfen, ob genau 4 Werte vorhanden sind
                    x, y, x_2, y_2 = values
                    # Werte zu den Listen hinzufügen
                    x_values.append(float(x))
                    y_values.append(float(y))
                    x_values2.append(float(x_2))
                    y_values2.append(float(y_2))

    #x_values.extend(x_values2)
    #y_values.extend(y_values2)

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
            plt.axvline(x=0, color='black', linewidth=1)  # Vertikale Linie bei x=0
            plt.axhline(y=0, color='black', linewidth=1)  # Horizontale Linie bei y=0
            plt.title(f"I/V HTL Perovskite cell, device: {i[0]}")
            plt.xlabel("V")
            plt.ylabel("j [mV / cm2]")
            plt.grid(True)
    plt.show()

