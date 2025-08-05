import numpy as np
import os
from foamify.src.draw import draw_line
from foamify.src.calcs import pdb_line, periodicize


def output_all(sys, my_dir=None):
    # Set the system Name
    if sys.name is None:
        sys.name = '_'.join([str(sys.data[_]) for _ in sys.data])
    # Set up the bubbles and box variables
    bubbles, verts = sys.bubbles, sys.box
    # Check to see if the user wants to do periodic bubbling
    if sys.data['pbc']:
        periodicize(sys)
    if sys.dir is not None:
        # Write the output files
        file_name = '_'.join([str(sys.data[_]) for _ in sys.data])
        my_dir = set_sys_dir(sys.dir + '/' + file_name)
    elif my_dir is None:
        # Write the output files
        file_name = '_'.join([str(sys.data[_]) for _ in sys.data])
        my_dir = set_sys_dir('Data/user_data/' + file_name)
    else:
        file_name = 'foam'
        my_dir = set_sys_dir('foam')

    write_pdb(sys, directory=my_dir)
    write_txt(sys, directory=my_dir)
    write_pymol_radii(sys, directory=my_dir)
    write_box(verts, file_name='retaining_box', directory=my_dir, radius=0.01 * sys.box[1][0])


def write_pdb(sys, directory=None):
    """
    Creates a pdb file type in the current working directory
    :param bubbles: List of atom type objects for writing
    :param file_name: Name of the output file
    :param sys: System object used for writing the whole pbd file
    :param directory: Output directory for the file
    :return: Writes a pdb file for the set of atoms
    """
    # Make note of the starting directory
    start_dir = os.getcwd()
    # Change to the specified directory
    if directory is not None:
        os.chdir(directory)
    # Open the file for writing
    with open(sys.name + '.pdb', 'w') as pdb_file:
        # Write the header that lets vorpy know it is a foam pdb
        pdb_file.write('REMARK foamify Box WHL = {:.3f}, Average Radius = {}, CV = {}, Number of Primary Balls = '
                       '{}, Density = {}, Overlap Allowance = {}r, Distribution = {}, '
                       'Periodic Boundary Conditions? = {}, Standardized Radii to Atomic? = {}\n'
                       .format(sys.box[1][1], sys.data['avg'], sys.data['std'], sys.data['num'],
                               sys.data['den'], sys.data['olp'], sys.data['dst'].capitalize(),
                               sys.data['pbc'], sys.data['sar']))

        # Go through each atom in the system
        for i, a in sys.bubbles.iterrows():
            # Get the location string
            x, y, z = a['loc']
            occ = 1
            if a['element'] is not None:
                elem = a['element']
            else:
                elem = 'h'
                if a['residue'] == 'OUT':
                    elem = 'n'
            # Write the atom information
            pdb_file.write(pdb_line(ser_num=i, name=a['name'], res_name=a['residue'], chain=a['chain'], elem=elem,
                                    x=x, y=y, z=z, occ=occ, tfact=a['rad']))
    # Change back to the starting directory
    os.chdir(start_dir)


def write_txt(sys, name=None, directory=None, round_to=4):
    """
    Writes a txt file for the balls in the system. The balls are in the style of a Voronota balls file. If the
    """
    # Make note of the starting directory
    start_dir = os.getcwd()

    # Change to the specified directory
    if directory is not None:
        os.chdir(directory)

    # Set the file Name
    if name is None:
        name = sys.name

    # Open the file for writing
    with open(name + '.txt', 'w') as balls_file:

        # Go through each atom in the system
        for i, a in sys.bubbles.iterrows():
            # Get the location string
            x, y, z = [round(_, round_to) for _ in a['loc']]

            # Add the end values for the atom if they exist
            vals = ' '.join([str(a[_]) if a[_] is not None else ' ' for _ in ['residue', 'chain', 'name', 'element']])

            # Write the atom information
            balls_file.write(f"{x} {y} {z} {round(a['rad'], round_to)} # {i} {vals}\n")

    # Change back to the starting directory
    os.chdir(start_dir)


def write_pymol_radii(sys, set_sol=True, directory=None, file_name=None):

    """
    Writes the pymol script for the
    """
    # Get the current directory, so we can come back to it when done
    start_dir = os.getcwd()

    # Change to the directory that the user set or just change to the system directory
    if directory is not None:
        os.chdir(directory)
    else:
        os.chdir(sys.dir)

    if file_name is None:
        file_name = 'set_radii.pml'
    if not set_sol:
        file_name = file_name[:-4] + '_nosol.pml'
    # Create the file
    with open(file_name, 'w') as file:
        for i, ball in sys.bubbles.iterrows():
            if not set_sol and ball.name.lower() == 'sol':
                continue
            file.write("alter {} and c. {} and r. {} and n. {}, vdw={}\n".format(sys.name, ball['chain'], ball['residue'], ball['name'], ball['rad']))
        # Rebuild the system
        file.write("\nrebuild")
    os.chdir(start_dir)


def write_box(verts, file_name, color=None, directory=None, radius=0.02):
    """
    Writes an off file for the edges specified
    :param edges: Edges to be output
    :param file_name: Name for the output file
    :param color: Color for the edges
    :param directory: Output directory
    :return: None
    """
    # Check to see if a directory is given
    if directory is not None:
        os.chdir(directory)
    # If no color is given, make the color random
    if color is None:
        color = [0.5, 0.5, 0.5]
    # Check that the edge has been drawn
    edges_draw_points, edges_draw_tris = [], []
    lines = [[[0, 0, 0], [1, 0, 0]], [[0, 0, 0], [0, 1, 0]], [[0, 0, 0], [0, 0, 1]], [[1, 0, 0], [1, 1, 0]],
             [[1, 0, 0], [1, 0, 1]], [[0, 1, 0], [1, 1, 0]], [[0, 1, 0], [0, 1, 1]], [[0, 0, 1], [1, 0, 1]],
             [[0, 0, 1], [0, 1, 1]], [[1, 1, 0], [1, 1, 1]], [[1, 0, 1], [1, 1, 1]], [[0, 1, 1], [1, 1, 1]]]
    points = []
    for line in lines:
        p0, p1 = [verts[line[0][i]][i] for i in range(3)], [verts[line[1][i]][i] for i in range(3)]
        points.append([p0, p1])
        draw_points, draw_tris = draw_line([p0, p1], radius=radius)
        edges_draw_points.append(draw_points)
        edges_draw_tris.append(draw_tris)
    num_verts, num_tris = 72, 72
    # Create the file
    with open(file_name + ".off", 'w') as file:
        # Count the number of triangles and vertices there are
        # Write the numbers into the file
        file.write("OFF\n" + str(num_verts) + " " + str(num_tris) + " 0\n\n\n")
        # Go through the surfaces and add the points
        for line in edges_draw_points:
            # Go through the points on the surface
            for point in line:
                # Add the point to the system file and the surface's file (rounded to 4 decimal points)
                str_point = [str(round(float(point[_]), 4)) for _ in range(3)]
                file.write(str_point[0] + " " + str_point[1] + " " + str_point[2] + '\n')
        num_verts, tri_count = 0, 0
        # Go through each surface and add the faces
        for line in edges_draw_tris:
            # Go through the triangles in the surface
            for tri in line:
                # Add the triangle to the system file and the surface's file
                str_tri = [str(tri[_] + num_verts) for _ in range(3)]
                file.write("3 " + str_tri[0] + " " + str_tri[1] + " " + str_tri[2] + " " + str(color[0]) + " " +
                           str(color[1]) + " " + str(color[2]) + "\n")
            # Keep counting triangles for the system file
            num_verts += 6


def set_sys_dir(dir_name=None):
    """
    Sets the directory for the output data. If the directory exists add 1 to the end number
    :param sys: System to assign the output directory to
    :param dir_name: Name for the directory
    :return:
    """
    if dir_name is None:
        # If no outer directory was specified use the directory outside the current one
        dir_name = os.getcwd() + 'foam'

    # Catch for existing directories. Keep trying out directories until one doesn't exist
    i = 0
    while True:
        # Try creating the directory with the system name + the current i_string
        try:
            # Create a string variable for the incrementing variable
            i_str = '_' + str(i)
            # If no file with the system name exists change the string to empty
            if i == 0:
                i_str = ""
            # Try to create the directory
            os.mkdir(dir_name + i_str)
            break
        # If the file exists increment the counter and try creating the directory again
        except FileExistsError:
            i += 1
        except FileNotFoundError:
            os.mkdir('Data/user_data')
    # Set the output directory for the system
    return dir_name + i_str
