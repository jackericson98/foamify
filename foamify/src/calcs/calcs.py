from numba import jit
from numpy import sqrt, square, inf, array, pi
from scipy import stats
from pandas import DataFrame


def calc_dist(l0, l1):

    return sqrt(sum(square(array(l0) - array(l1))))


@jit(nopython=True)
def calc_dist_numba(my_loc, other_loc, box_side=None, periodic=True):
    if periodic and box_side is not None:
        # Calculate the minimum distance accounting for periodic boundary conditions
        dist_vector = [min(abs(my_loc[dim] - other_loc[dim]), box_side - abs(my_loc[dim] - other_loc[dim])) for dim in
                       range(3)]
        return (dist_vector[0] ** 2 + dist_vector[1] ** 2 + dist_vector[2] ** 2) ** 0.5
    else:
        # Standard Euclidean distance calculation
        return ((my_loc[0] - other_loc[0])**2 + (my_loc[1] - other_loc[1])**2 + (my_loc[2] - other_loc[2])**2)**0.5


@jit(nopython=True)
def box_search_numba(loc, num_splits, box_verts):
    # Calculate the size of the sub boxes
    sub_box_size = [round((box_verts[1][i] - box_verts[0][i]) / num_splits, 3) for i in range(3)]
    # Find the sub box for the atom
    box_ndxs = [int((loc[j] - box_verts[0][j]) / sub_box_size[j]) for j in range(3)]
    if box_ndxs[0] >= num_splits or box_ndxs[1] >= num_splits or box_ndxs[2] >= num_splits:
        return
    # Return the box indices
    return box_ndxs


def box_search(loc, num_splits, box_verts):
    """
    Locates the sub box indices for a given location
    """
    loc = array(loc)
    return box_search_numba(loc, num_splits, array(box_verts))


def get_bubbles(ball_matrix, cells, sub_box_size, dist=0, periodic=False):
    """
    Takes in the cells and the number of additional cells to search and returns an atom list
    :param cells: The initial boxes in the network to stem from
    :param dist: The number of cells out from the initial set of cells to search
    :param periodic: Boolean indicating whether to apply periodic boundary conditions
    """

    # Calculate the reach based on distance and sub-box size
    reach = int(dist / min(sub_box_size)) + 4

    # Determine the size of the matrix grid
    n = ball_matrix[-1, -1, -1][0]

    # Ensure 'cells' is iterable over indices even if a single cell is provided
    if isinstance(cells[0], int):
        cells = [cells]
    # Gather all indices considering periodic boundaries
    balls = []
    for cell in cells:
        for i in range(cell[0] - reach, cell[0] + reach):
            for j in range(cell[1] - reach, cell[1] + reach):
                for k in range(cell[2] - reach, cell[2] + reach):
                    # Compute wrapped indices if periodic, else bounded indices
                    if periodic:
                        x, y, z = (i + n) % n, (j + n) % n, (k + n) % n
                    else:
                        if 0 <= i < n and 0 <= j < n and 0 <= k < n:
                            x, y, z = i, j, k
                        else:
                            continue  # Skip indices outside the bounds

                    # Try to add balls from the calculated indices
                    try:
                        balls.extend(ball_matrix[x, y, z])
                    except KeyError:
                        pass  # If a cell is empty or key error occurs, skip
    # print(cells)
    # print('\nindices = ', indices)
    return balls


def calc_box(self, locs, rads):
    """
    Determines the dimensions of a box x times the size of the atoms
    :return: Sets the box attribute with the correct values as well as atoms_box
    """
    # Set up the minimum and maximum x, y, z coordinates
    min_vert = array([inf, inf, inf])
    max_vert = array([-inf, -inf, -inf])
    # Loop through each atom in the network
    for loc in locs:
        # Loop through x, y, z
        for i in range(3):
            # If x, y, z values are less replace the value in the mins list
            if loc[i] < min_vert[i]:
                min_vert[i] = loc[i]
            # If x, y, z values are greater replace the value in the maxes list
            if loc[i] > max_vert[i]:
                max_vert[i] = loc[i]
    # Get the vector between the minimum and maximum vertices for the defining box
    r_box = max_vert - min_vert
    # If the atoms are in the same plane adjust the atoms
    for i in range(3):
        if r_box[i] == 0 or abs(r_box[i]) == inf:
            r_box[i], min_vert[i], max_vert[i] = 4 * rads[0], locs[0][i], locs[0][i]
    # Set the atoms box value
    self.atoms_box = [min_vert.tolist(), max_vert.tolist()]
    # Set the new vertices to the x factor times the vector between them added to their complimentary vertices
    min_vert, max_vert = max_vert - r_box * self.box_size, min_vert + r_box * self.box_size
    # Return the list of array turned list vertices
    self.box = [[round(_, 3) for _ in min_vert], [round(_, 3) for _ in max_vert]]


def calc_tot_vol(radii):
    return sum([4 / 3 * pi * bub ** 3 for bub in radii])


def pdb_line(atom="ATOM", ser_num=0, name="", alt_loc=" ", res_name="", chain="A", res_seq=0, cfir="", x=0, y=0, z=0,
             occ=1, tfact=0, seg_id="", elem="h", charge=""):
    return "{:<6}{:>5} {:<4}{:1}{:>3} {:^1}{:>4}{:1}   {:>8.3f}{:>8.3f}{:>8.3f}{:>6.2f}{:>6.2f}      {:<4}{:>2}{}\n"\
        .format(atom, ser_num, name, alt_loc, res_name, chain, res_seq, cfir, x, y, z, occ, tfact, seg_id, elem, charge)


def periodicize(sys, mirror=False):
    # Create the list of bubbles
    sys_bubs = sys.bubbles.copy().to_dict(orient='records')
    # New list
    bubbles = [_ for _ in sys_bubs]
    chain_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                     'U', 'V', 'W', 'X', 'Y', 'Z']
    # Loop through the first 6
    for i, direction in enumerate([[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, -1], [0, 0, 1], [-1, -1, 0],
                                   [-1, 1, 0], [-1, 0, -1], [-1, 0, 1], [1, -1, 0], [1, 1, 0], [1, 0, -1], [1, 0, 1],
                                   [0, -1, -1], [0, -1, 1], [0, 1, -1], [0, 1, 1], [-1, -1, -1], [-1, -1, 1],
                                   [-1, 1, -1], [-1, 1, 1], [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1]]):
        chain = chain_letters[i]
        for bubble in sys_bubs:
            # First we need to copy the bubble
            new_bub = bubble.copy()
            # Change the location
            if not mirror:
                new_bub['loc'] = array([bubble['loc'][i] + direction[i] * sys.box[1][i] for i in range(3)])
            else:
                # Mirrored boundary
                new_bub['loc'] = array([
                    # If moving in the negative or positive direction, reflect about the box boundaries
                    2 * sys.box[1][i] - bubble['loc'][i] if direction[i] == -1 else
                    bubble['loc'][i] if direction[i] == 0 else
                    2 * sys.box[0][i] - bubble['loc'][i]  # For positive direction, reflect
                    for i in range(3)
                ])
            # Change the residue so that it is identified as separate
            new_bub['residue'] = bubble['residue']
            # Change the chain name so that it's identified as separate
            new_bub['chain'] = chain
            # Add the bubble to the list
            bubbles.append(new_bub)

    # Make the dataframe
    sys.bubbles = DataFrame(bubbles)


def calc_stats(sds, mu, num_its, num_balls):
    if type(num_balls) is int:
        num_balls = [num_balls]
    for sd in sds:
        sd1s, sd2s, sd3s = [], [], []
        sd1gsl, sd2gsl, sd3gsl = [], [], []
        for i in num_balls:
            sd1, sd2, sd3 = [], [], []
            sd1gs, sd2gs, sd3gs = 0, 0, 0
            for j in range(num_its):
                bubs = []
                while len(bubs) < i:
                    data = stats.lognorm(sd, loc=mu).rvs(size=1)[0] - 1
                    if data > 0:
                        bubs.append(data)
                sd1_count, sd2_count, sd3_count = 0, 0, 0
                for bub in bubs:
                    if abs(bub - mu) < sd:
                        sd1_count += 1
                    if abs(bub - mu) < 2 * sd:
                        sd2_count += 1
                    if abs(bub - mu) < 3 * sd:
                        sd3_count += 1
                sd1.append(sd1_count)
                sd2.append(sd2_count)
                sd3.append(sd3_count)
                sd1g, sd2g, sd3g = 0, 0, 0
                if sd1_count / i > 0.68:
                    sd1g = 1
                if sd2_count / i > 0.95:
                    sd2g = 1
                if sd3_count / i > 0.99:
                    sd3g = 1
                sd1gs += sd1g
                sd2gs += sd2g
                sd3gs += sd3g
            # print("{} Done".format(i))
            print(i, (sum(sd1) / num_its) / i, (sum(sd2) / num_its) / i, (sum(sd3) / num_its) / i, sd1gs, sd2gs, sd3gs)
