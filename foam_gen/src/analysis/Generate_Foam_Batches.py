import tkinter as tk
from tkinter import filedialog
import numpy as np
import os


if __name__ == '__main__':
    # Open the folder
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    folder = filedialog.askdirectory()
    count_dict = {}
    for rooot, folders, files in os.walk(folder):
        for folder in folders:
            folder_vals = folder.split('_')
            if len(folder_vals) < 7:
                continue
            try:
                mean, cv, number, density, olap, dist, pbc = float(folder_vals[0]), float(folder_vals[1]), int(folder_vals[2]), float(folder_vals[3]), float(folder_vals[4]), folder_vals[5], folder_vals[6]
                if (mean, cv, number, density, olap, dist, pbc) in count_dict:
                    count_dict[(mean, cv, number, density, olap, dist, pbc)] += 1
                else:
                    count_dict[(mean, cv, number, density, olap, dist, pbc)] = 1
            except ValueError:
                continue

    # Set the settings
    means = [1.0]
    cv_vals = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    density_vals = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
    olap_vals = [1.0]
    num_vals = [1000]
    pbc_vals = ['False']
    dist_vals = ['gamma']
    my_string = "python foam_gen.py mean {:.3f} cv {:.3f} num {} den {:.3f} olp {} dist {} pbc {} \n"
    number_of_foam_files = 20
    number_of_files = 10
    # Count the number of foams that need to be created
    total_number_of_foams = 0
    # Create the new strings list
    new_strings = []
    # Now loop through the cv_vals and density vals
    for mean in means:
        for dist in dist_vals:
            for num in num_vals:
                for olap in olap_vals:
                    for cv in cv_vals:
                        for pbc in pbc_vals:
                            for density in density_vals:
                                if (mean, cv, num, density, olap, dist, pbc) in count_dict:
                                    count_dict[(mean, cv, num, density, olap, dist, pbc)] = number_of_foam_files - count_dict[(mean, cv, num, density, olap, dist, pbc)]
                                else:
                                    count_dict[(mean, cv, num, density, olap, dist, pbc)] = number_of_foam_files
                                # Add to the total number of foams
                                total_number_of_foams += count_dict[(mean, cv, num, density, olap, dist, pbc)]


    # Sort the dictionary
    count_dict = {key: value for key, value in
                  # Sort by number, reverse overlap, density and then reverse cv
                  sorted(count_dict.items(), key=lambda item: (item[0][2], -item[0][4], item[0][3], -item[0][1]))}

    # Set the counter for the number of lines
    counter = 0
    # Loop through the remaining runs
    for vals in count_dict:
        # Loop through the number of times each run needs to be made
        for i in range(count_dict[vals]):
            # Get the file number based on the counter so we know when a new file needs to start
            file_number = int(counter // (total_number_of_foams / number_of_files))
            j = counter // 220 + 1

            # Open the file we intend to write to
            with open(f'../foam_gen_{j}.sh', 'a') as foam_writer:
                foam_writer.write(my_string.format(*vals))

            # Update the counter
            counter += 1