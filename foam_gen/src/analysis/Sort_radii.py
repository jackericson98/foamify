import numpy as np
import tkinter as tk
from tkinter import filedialog
from foam_gen.src.system import System


if __name__ == '__main__':

    # Set up the window
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)

    # Get the pdb
    my_pdb = filedialog.askopenfilename()

    # Get the radii of the balls
    radii = []
    with open(my_pdb, 'r') as pdb_file:
        for i, line in enumerate(pdb_file.readlines()):
            if i == 0:
                continue
            radii.append(float(line[62:66]))
            # print(line[62:66])
    num_cols = len(radii) ** 0.5
    if not num_cols.is_integer():
        num_cols += 1
    x_ticks = np.linspace(0, num_cols * 2 * max(radii), int(num_cols))
    coordinates = []
    for _ in x_ticks:
        for __ in x_ticks:
            coordinates.append([0, _, __])

    my_sys = System(bubbles=[(coordinates[i], radii[i]) for i in range(len(radii))], output_directory='C:/Users/jacke/PycharmProjects/foam_gen/Data/user_data')
