import time
from numba import jit
import pandas as pd
from joblib import load
from numpy import sqrt, array, random, cbrt, linspace
from pandas import DataFrame
from foam_gen.src.calcs import get_bubbles, calc_dist_numba, calc_tot_vol
from foam_gen.src.make_foam.distributions import get_bubble_radii
from foam_gen.src.make_foam.atomic import standardize_radii_to_atomic



def record_density(bubbles, box, sub_box_size, bubble_matrix, max_bub_radius, n_samples=1000000, pbc=False):
    count = 0
    for i in range(n_samples):
        # Calculate the percentage
        print("\r Checking Density {:.2f} %".format(100 * round(i/n_samples, 4)), end="")

        point = [random.uniform(min(box[0][i], box[1][i]), max(box[0][i], box[1][i])) for i in range(3)]
        # Find the box that the bubble would belong to
        my_box = [int(point[j] / sub_box_size[j]) for j in range(3)]
        # # Find all bubbles within range of the
        bub_ints = get_bubbles(bubble_matrix, my_box, sub_box_size, 2 * max_bub_radius, pbc)
        close_bubs = [bubbles[_] for _ in bub_ints]
        # Sort the bubbles by size
        close_bubs.sort(key=lambda x: x['rad'], reverse=True)
        # Check for overlap with close bubs
        close_locs, close_rads = array([_['loc'] for _ in close_bubs]), array([_['rad'] for _ in close_bubs])
        for j, loc in enumerate(close_locs):
            if calc_dist_numba(array(point), loc, box[1][0], periodic=pbc) < close_rads[j]:
                count += 1
                break
    return count / n_samples


@jit(nopython=True)
def overlap(my_loc, bub, close_locs, close_rads, olp, box_side=None, periodic=True):
    # Loop through the close bubbles
    for i in range(len(close_locs)):
        # Calculate the effective radius considering overlap
        if bub < close_rads[i]:
            effective_radius = close_rads[i] + (1.0 - olp) * bub
        else:
            effective_radius = bub + (1.0 - olp) * close_rads[i]

        if calc_dist_numba(my_loc, close_locs[i], box_side, periodic) < effective_radius:
            return True
    return False


def find_bubs(bubble_radii, num_boxes, cube_width, sub_box_size, olap, n, print_actions, periodic=False,
              box_width=None, elements=None):
    max_bub_radius = max(bubble_radii)
    # Create the bubble list
    bubbles = []
    # Instantiate the grid structure of lists is locations representing a grid
    bubble_matrix = {(-1, -1, -1): [num_boxes]}
    time_start = time.perf_counter()
    break_all = False
    # Place the spheres
    for i, bub_rad in enumerate(bubble_radii):
        # Print the loading bar
        if print_actions:
            my_time = round(time.perf_counter() - time_start)
            print("\rCreating bubbles - {:.2f}% - {} s".format(100 * (i + 1) / n, my_time), end="")
        # Keep trying to place the bubble into a spot where it won't overlap
        while True:
            # Calculate a random bubble location
            if periodic:
                my_loc = random.rand(3) * cube_width
            else:
                my_loc = random.uniform(bub_rad, cube_width - bub_rad, 3)
            # Find the box that the bubble would belong to
            my_box = [int(my_loc[j] / sub_box_size[j]) for j in range(3)]
            # Place the first ball
            if len(bubbles) == 0:
                break
            # Get the distance to the closest bubble
            num_cells = bub_rad + max_bub_radius
            # Find all bubbles within range of the
            bub_ints = get_bubbles(ball_matrix=bubble_matrix, cells=my_box, sub_box_size=sub_box_size, dist=num_cells,
                                   periodic=periodic)
            close_bubs = [bubbles[_] for _ in bub_ints]
            if len(close_bubs) == 0:
                break
            # Sort the bubbles by size
            close_bubs.sort(key=lambda x: x['rad'], reverse=True)
            # Check for overlap with close bubs
            close_locs, close_rads = array([_['loc'] for _ in close_bubs]), array([_['rad'] for _ in close_bubs])

            if not overlap(my_loc, bub_rad, close_locs, close_rads, olap, periodic=periodic, box_side=box_width):
                break
        if break_all:
            break
        # Set the default residue and chain
        chain = '0'
        # # Check the location of the bubble
        # if any([my_loc[i] < bub_rad or my_loc[i] + bub_rad > cube_width for i in range(3)]):
        #     residue, chain = 'BUB', 'E'
        # Check that the element exists
        element = None
        name = str(hex(i))[2:]
        res_name = 0
        if elements is not None:
            element = elements[i]
            name = elements[i]
            res_name = str(hex(i))[2:]

        # Create the bubble
        bubbles.append({'chain': chain, 'loc': my_loc, 'rad': bub_rad, 'num': i, 'name': name, 'asurfs': [],
                        'residue': res_name, 'box': my_box, 'element': element})
        # Add the atom to the box
        try:
            bubble_matrix[my_box[0], my_box[1], my_box[2]].append(i)
        except KeyError:
            bubble_matrix[my_box[0], my_box[1], my_box[2]] = [i]

        if break_all:
            break
    return bubbles, bubble_matrix


def make_foam(sys, print_actions):
    # Get the variables
    mu, cv, n, density, olap, dist, pbc, sar = (sys.data['avg'], sys.data['std'], sys.data['num'], sys.data['den'],
                                                sys.data['olp'], sys.data['dst'], sys.data['pbc'], sys.data['sar'])
    # Get the bubble radii
    bubble_radii = get_bubble_radii(dist, cv, mu, n)

    # Check if the radii need to be standardized to atomic radii
    atom_names = None
    if sar:
        bubble_radii, atom_names = standardize_radii_to_atomic(bubble_radii)

    # Get the maximum bubble radius
    max_bub_radius = max(bubble_radii)

    # Adjust the density using the model
    if olap > 0.0:
        model = load('./Data/linreg_pipeline.pkl')
        new_data = pd.DataFrame({'Adjusted Density': [density], 'Mean': [mu], 'CV': [cv], 'Number': [n],
                                 'Distribution': [dist], 'Overlap': [olap], 'PBC': pbc})
        new_density = model.predict(new_data)[0]
    else:
        new_density = density

    # Calculate the cube width by getting the cube root of total volume of the bubble radii over the density
    cube_width = cbrt(calc_tot_vol(bubble_radii) / new_density)
    # Create the box
    sys.box = [[0, 0, 0], [cube_width, cube_width, cube_width]]
    # Set the number of boxes to roughly 5x the number of atoms must be a cube for the of cells per row/column/aisle
    num_boxes = int(0.5 * sqrt(n)) + 1
    # Get the cell size
    sub_box_size = [round(cube_width / num_boxes, 3) for i in range(3)]

    bubbles, sys.bubble_matrix = find_bubs(bubble_radii, num_boxes, cube_width, sub_box_size, olap, n,
                                           print_actions, periodic=sys.data['pbc'], box_width=sys.box[1][0],
                                           elements=atom_names)
    # if olap > 0:
    #     new_density = record_density(bubbles, [[0, 0, 0], [cube_width, cube_width, cube_width]],
    #                                  sub_box_size=sub_box_size, max_bub_radius=max_bub_radius,
    #                                  bubble_matrix=sys.bubble_matrix, pbc=sys.data['pbc'])
    #     with open(sys.vpy_dir + '/Data/density_adjustments.txt', 'a') as density_logs:
    #         density_logs.write("{} {} {} {} {} {} {} {}\n".format(new_density, mu, cv, n, density, dist, olap, sys.data['pbc']))

    # Create the dataframe for the bubbles
    sys.bubbles = DataFrame(bubbles)
