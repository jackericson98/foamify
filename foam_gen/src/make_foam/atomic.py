# Default radii and other radii, excluding protein main chain and side chain radii
element_radii = {
    'H': 1.30, 'HE': 1.40, 'LI': 0.76, 'BE': 0.45, 'B': 1.92, 'C': 1.80, 'N': 1.60, 'O': 1.50, 'P': 1.90,
    'S': 1.90, 'F': 1.33, 'CL': 1.81, 'BR': 1.96, 'I': 2.20, 'AL': 0.60, 'AS': 0.58, 'AU': 1.37, 'BA': 1.35,
    'BI': 1.03, 'CA': 1.00, 'CD': 0.95, 'CO': 0.65, 'CR': 0.73, 'CS': 1.67, 'CU': 0.73, 'FE': 0.61, 'GA': 0.62,
    'GE': 0.73, 'HG': 1.02, 'K': 1.38, 'MG': 0.72, 'MN': 0.83, 'MO': 0.69, 'NA': 1.02, 'NI': 0.69, 'PB': 1.19,
    'PD': 0.86, 'PT': 0.80, 'RB': 1.52, 'SB': 0.76, 'SC': 0.75, 'SN': 0.69, 'SR': 1.18, 'TC': 0.65, 'TI': 0.86,
    'V': 0.79, 'ZN': 0.74, 'ZR': 0.72
}


def find_closest_key(value, sorted_dict):
    """
    Finds the closest key to a given value using binary search in a dictionary that is assumed to be sorted by keys.
    This function directly uses the dictionary and extracts keys as necessary.

    Args:
        value (float): The value to find the closest key for.
        sorted_dict (dict): Dictionary sorted by keys.

    Returns:
        tuple: A tuple containing the closest key and its corresponding value from the dictionary.
    """

    sorted_keys = sorted(sorted_dict.keys())  # Extract sorted keys from the dictionary
    low, high = 0, len(sorted_keys) - 1
    closest_key = None
    min_diff = float('inf')

    while low <= high:
        mid = (low + high) // 2
        mid_key = sorted_keys[mid]
        diff = abs(mid_key - value)

        if diff < min_diff:
            min_diff = diff
            closest_key = mid_key

        if mid_key < value:
            low = mid + 1
        elif mid_key > value:
            high = mid - 1
        else:
            # Exact match found
            return mid_key, sorted_dict[mid_key]

    return closest_key, sorted_dict[closest_key]


def standardize_radii_to_atomic(radii):

    # Reverse the dictionary
    reversed_element_radii = {value: key for key, value in element_radii.items()}

    # Sort the dictionary by keys (radii)
    sorted_reversed_element_radii = dict(sorted(reversed_element_radii.items()))

    # Loop through the radii
    new_radii, new_atoms = [], []
    for radius in radii:
        # Find the closest radius and atom name
        new_radius, new_atom = find_closest_key(radius, sorted_reversed_element_radii)
        new_radii.append(new_radius)
        new_atoms.append(new_atom)
    return new_radii, new_atoms


