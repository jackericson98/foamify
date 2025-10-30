import os
from numpy import inf
from pandas import DataFrame

from foamify.src.output import output_all
from foamify.src.make_foam import make_foam
from foamify.src.visualize import SettingsGUI


class System:
    def __init__(self, args=None, bubbles=None, output_directory=None, gui=None, root_dir=None, print_actions=False):
        """
        System class for managing and processing bubble/atom systems.

        This class is used to import, store, and manipulate systems of bubbles (atoms), 
        handle file I/O, and interface with a GUI if provided.

        Attributes:
            name (str): Name describing the system.
            args (list or None): Pre-loaded arguments for system configuration.
            bubbles (list or None): List holding the atom/bubble objects.
            bubble_matrix (np.ndarray or None): 3D matrix for tracking bubble overlap.
            box (Any): Vertices of the box containing the bubbles.
            data (dict): Additional data provided by the base file.
            dir (str or None): Output directory for export files.
            vpy_dir (str): Directory where Vorpy is running.
            max_atom_rad (float): Largest radius of the system for reference.
            gui (Any): GUI object (e.g., tkinter) for system interaction.
            print_actions (bool): Whether to print actions for debugging/logging.

        Methods:
            read_argv():
                Reads and parses command-line arguments to set system parameters.

            set_loaded_bubs():
                Sets up the system when bubbles are loaded directly.

            output():
                Outputs the current system state to the output directory.

        Returns:
            System: An initialized System object.

        Example:
            >>> sys = System(args=['num', 100, 'avg', 1.0], output_directory='output/')
            >>> sys.read_argv()
            >>> print(sys.data)
            {'avg': 1.0, 'std': 0.1, 'num': 100, 'den': 0.25, 'olp': 0.0, 'dst': 'gamma', 'pbc': False, 'sar': False}
        """

        # Names
        self.name = None                    # Name                :   Name describing the system

        # Loadable objects
        self.args = args                    # Args                :   Pre loaded arguments to run faster
        self.bubbles = bubbles              # Atoms               :   List holding the atom objects
        self.bubble_matrix = None           # Bubble Matrix       :   3D matrix holding the bubbles for tracking overlap
        self.box = None                     # Bubble box          :   Vertices of the box holding the bubbles

        # Set up the file attributes
        self.data = {'olp': 0.0}            # Data                :   Additional data provided by the base file
        self.dir = output_directory         # Output Directory    :   Output directory for the export files
        self.vpy_dir = os.getcwd()          # Vorpy Directory     :   Directory that vorpy is running out of
        self.max_atom_rad = 0               # Max atom rad        :   Largest radius of the system for reference

        # Gui
        self.gui = gui                      # GUI                 :   GUI Vorpy object that can be updated through sys
        self.print_actions = print_actions  # Print actions Bool  :   Tells the system to print or not

        # Read the arguments of the terminal
        if bubbles is None:
            self.read_argv()
        else:
            self.set_loaded_bubs()
            output_all(self)

    def read_argv(self):
        
        # Set up the data dictionary
        self.data = {'avg': 1, 'std': 0.1, 'num': 1000, 'den': 0.25, 'olp': 0.0, 'dst': 'gamma', 'pbc': False,
                     'sar': False}
        setting_names = {
            **{_: 'avg' for _ in {'size', 'average', 'mean', 'sz', 'avg', 'mu'}},
            **{_: 'std' for _ in {'std', 'cv', 'variance', 'standard_deviation', 'coefficient_of_variation'}},
            **{_: 'num' for _ in {'num', 'number', 'amount', 'quantity', 'bubbles', 'nmbr', 'bn'}},
            **{_: 'den' for _ in {'den', 'density', 'packing'}},
            **{_: 'olp' for _ in {'olp', 'overlap', 'crossing', 'olap'}},
            **{_: 'dst' for _ in {'dst', 'dist', 'distribution', 'pdf'}},
            **{_: 'pbc' for _ in {'pbc', 'periodic', 'cyclic'}},
            **{_: 'sar' for _ in {'sar', 'std_ar'}}
        }
        # First check to see if a setting has been named
        if any([_.lower() in setting_names for _ in self.args]):
            i = 0
            # Loop through the different settings that are set
            while i < len(self.args):
                # Check to see if the setting is in the dictionary in the settings names
                if self.args[i].lower() in setting_names:
                    # Set the settings
                    self.data[setting_names[self.args[i].lower()]] = self.args[i + 1]
                    i += 1
                i += 1

        # Check to see if argv have been made
        elif len(self.args) > 1:
            args = self.args[1:]
            for i, data in enumerate(self.data):
                if i >= len(args):
                    break
                self.data[data] = args[i]

        # If we want to prompt the user
        else:
            self.gui = SettingsGUI()
            self.data = self.gui.data
        # Check the open cell condition:
        if type(self.data['olp']) is str and self.data['olp'].lower() in ['true', 't', '1']:
            self.data['olp'] = 1.0
        elif type(self.data['olp']) is str and self.data['olp'].lower() in ['false', 'f', '0']:
            self.data['olp'] = 0.0

        # Check for periodic flags for periodic boundary conditions
        if type(self.data['pbc']) is str and self.data['pbc'].lower() in {'true', 't', 'yes', '1'}:
            self.data['pbc'] = True
        elif type(self.data['pbc']) is str and self.data['pbc'].lower() in {'false', 'f', '0', 'no', 'false\r', 'false\n'}:
            self.data['pbc'] = False

        # Check for periodic flags for standardized atomic radii
        if type(self.data['sar']) is str and self.data['sar'].lower() in {'true', 't', 'yes', '1'}:
            self.data['sar'] = True
        elif type(self.data['sar']) is str and self.data['sar'].lower() in {'false', 'f', '0', 'no'}:
            self.data['sar'] = False

        # Once done set the settings' to their correct variable type
        self.data = {'avg': float(self.data['avg']), 'std': float(self.data['std']), 'num': int(self.data['num']),
                     'den': float(self.data['den']), 'olp': float(self.data['olp']), 'dst': self.data['dst'],
                     'pbc': self.data['pbc'], 'sar': self.data['sar']}
        self.make_foam()
        output_all(self)

    def prompt(self, bubble_size=None, bubble_sd=None, bubble_num=None, bubble_density=None, open_cell=None):
        # Get the system information
        if bubble_size is None:
            self.data['avg'] = float(input("Enter mean bubble size - "))
        if bubble_sd is None:
            self.data['std'] = float(input("Enter bubble standard deviation - "))
        if bubble_num is None:
            self.data['num'] = int(input("Enter number of bubbles - "))
        if bubble_density is None:
            self.data['den'] = float(input("Enter bubble density - "))
        if open_cell is None:
            opc = input("Open cell (overlapping)? - ")
            # If user says yes, default is True so no need to catch those cases
            if opc.lower() in ['n', 'no', 'f', 'false']:
                self.data['olp'] = 0.0
            else:
                try:
                    self.data['olp'] = float(opc)
                except ValueError:
                    self.data['olp'] = 0.0

    def set_loaded_bubs(self):
        # Set the default residue and chain
        residue, chain, my_box = 'BUB', 'A', None
        # Set up the bubbles list
        bubbles = []
        box = [[inf, inf, inf], [-inf, -inf, -inf]]
        # Bubbles loaded need to be (loc, rad)
        for i, bub in enumerate(self.bubbles):
            # Pull the loc and the rad
            my_loc, bub_rad = bub
            # Set the box
            for j in range(3):
                if my_loc[j] - bub_rad < box[0][j]:
                    box[0][j] = my_loc[j] - bub_rad
                if my_loc[j] + bub_rad > box[1][j]:
                    box[1][j] = my_loc[j] + bub_rad
            # Create the bubble
            bubbles.append(
                {'chain': chain, 'loc': my_loc, 'rad': bub_rad, 'num': i, 'name': str(hex(i))[2:], 'asurfs': [],
                 'residue': residue, 'box': my_box})
        # Make the data_frame
        self.bubbles = DataFrame(bubbles)
        self.box = box

    def make_foam(self, print_actions=True):
        make_foam(self, print_actions)
