import os.path
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import filedialog
import textwrap


class HelpGUI:
    def __init__(self, parent):
        # Create a top-level window
        self.top = tk.Toplevel(parent)
        self.top.title("Help")
        self.top.geometry("375x365")  # Width x Height

        # Create the fonts
        self.title_font = font.Font(family='Helvetica', size=15, weight='bold')

        # Dictionary to hold the help topics and their descriptions
        self.help_info = {
            "About": "\n\n".join([textwrap.fill(section, width=40) for section in [
                     "Welcome to foamify Help!",
                     "This program can be used to generate statistical ensembles of balls. These ensembles can be used to represent foams or simply as packings of spheres.",
                     "foamify outputs four files: a TXT file with the balls locations and radii, a similar PDB file, a PyMOL script that sets the ball radii in PyMOL, and an OFF file with the retaining box.",
                     "The name of the directory and the ball files refer to the settings used to create it, separated by underscores in the following order: Mean, CV, Number, Density, Overlap, PBC.",
                     "For more information on any of the settings, use the dropdown menu above."]]),

            "Average Ball Radius": "\n\n".join([textwrap.fill(section, width=40) for section in [
                       "Average Ball Radius",

                       "This setting refers to the the average ball/bubble radius size that the sample distribution uses to sample from."]]),

            "Radii Polydispersity (CV)": "\n\n".join([textwrap.fill(section, width=40) for section in [
                  "Coefficient of Variation",
                  "This setting is a general term that describes the width of the distribution. This is very similar to a "
            ]])
                  ,
            "Number of Balls": "\n\n".join([textwrap.fill(section, width=40) for section in [
                      "Number of Balls",
                      "The number of balls the output foam. "]]),
            "Ball Packing Density": "\n\n".join([textwrap.fill(section, width=40) for section in [
                       "Ball Packing Density"
                       "Sets the amount of space occupied by the balls relative to the total volume. Since the balls average out to the set average radius, the "]]),
            "Overlap Allowance (r)": "\n\n".join([textwrap.fill(section, width=40) for section in [
                       "Allowed Ball Overlap",
                       "The amount the balls are allowed to overlap as a percentage of the smaller of the overlapping balls' radius.",
                       "e.g. If Ball 1 has a radius of 2.0, ball 2 has a radius of 2.5, and the overlap setting if 0.5r, the balls can overlap at most by 1.0 or be placed any closer than 3.5 away from each other"]]),
            "Radii Distribution": "\n\n".join([textwrap.fill(section, width=40) for section in [
                            "Ball Radius Distribution",
                            "The distribution that the radii are pulled from. This determines how the set of output balls are sized. It, in combination with CV, determines how polydisperse the "]]),
            "Periodic Boundary": "\n\n".join([textwrap.fill(section, width=40) for section in [
                                 "Periodic Boundary",
                                 ""]]),
            "Standardized Atomic Radii": "\n\n".join([textwrap.fill(section, width=40) for section in [
                                         ""]]),
            "Output Directory": "\n\n".join([textwrap.fill(section, width=40) for section in [
                                ""]])
        }

        # Create the left and right gaps
        ttk.Label(self.top, text=" ").grid(row=0, column=0, padx=5)

        # Create the title
        ttk.Label(self.top, text="Help", font=self.title_font).grid(row=1, columnspan=2, column=1)

        # Create the label for the combobox
        self.comboboxlabel = ttk.Label(self.top, text="Topic:")
        self.comboboxlabel.grid(row=2, column=1, sticky='w', pady=10, padx=10)

        # Create a Combobox to select the help topic
        self.topic_var = tk.StringVar()
        self.combobox = ttk.Combobox(self.top, textvariable=self.topic_var, state="readonly", width=19)
        self.combobox['values'] = list(self.help_info.keys())
        self.combobox.grid(row=2, column=2, padx=10, pady=10, sticky='e')
        self.combobox.current(0)  # Default to first item in the list
        self.combobox.bind("<<ComboboxSelected>>", self.update_description)

        # Text widget or Label for displaying the help description
        self.description = tk.Text(self.top, height=15, width=40)
        self.description.grid(row=3, column=1, padx=10, pady=10, columnspan=2)
        self.description.insert('end', self.help_info[self.topic_var.get()])
        self.description.config(state='disabled')  # Make the text widget read-only

        # Set up the close button

    def update_description(self, event):
        # Update the text widget with the selected topic's description
        self.description.config(state='normal')  # Enable text widget to modify
        self.description.delete('1.0', 'end')  # Clear current text
        self.description.insert('end', self.help_info[self.topic_var.get()])  # Insert new description
        self.description.config(state='disabled')  # Set back to read-only

    # Function to handle cancel
    def cancel(self):
        self.root.destroy()


class SettingsGUI:
    def __init__(self):
        # Function to collect values and update the data dictionary
        self.data = {'avg': 1.0, 'std': 0.1, 'num': 1000, 'den': 0.25, 'olp': 0.0, 'dst': 'gamma', 'pbc': False,
                     'sar': False, 'dir': './Data/user_data'}
        # Set up the root
        self.root = tk.Tk()
        # Main window
        # self.root.title("Foamify")
        self.root.geometry("375x540")  # Set the window size

        # Place the Foamify logo image under the title, with transparent background matching the window
        try:
            from PIL import Image, ImageTk

            # Load the logo image
            logo_image = Image.open("assets/FoamifyLogo.png")

            # Convert to RGBA to ensure transparency
            if logo_image.mode != "RGBA":
                logo_image = logo_image.convert("RGBA")

            # Replace white or near-white background with full transparency to match 'wheat'
            datas = logo_image.getdata()
            newData = []
            # Define a threshold for "white" (tune as needed)
            threshold = 240
            for item in datas:
                # item is (R, G, B, A) or (R, G, B)
                if len(item) == 4:
                    r, g, b, a = item
                else:
                    r, g, b = item
                    a = 255
                if r > threshold and g > threshold and b > threshold:
                    # Make transparent
                    newData.append((255, 245, 200, 0))  # transparent, matches 'wheat' RGB
                else:
                    newData.append((r, g, b, a))
            logo_image.putdata(newData)

            # Resize the image
            try:
                resample = Image.Resampling.LANCZOS
            except AttributeError:
                resample = Image.LANCZOS
            logo_image = logo_image.resize((120, 120), resample)

            self.logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = ttk.Label(self.root, image=self.logo_photo, background=None)
            logo_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        except Exception as e:
            print(f"Could not load logo image: {e}")

        # Setting up the grid and padding
        self.options = {'padx': 10, 'pady': 5}  # Common options for padding
        # Styles
        self.background_color = 'wheat'
        self.foreground_color = 'black'
        # Create the variables
        self.create_fonts()
        self.create_variables()
        self.create_styles()
        self.create_widgets()

    def create_fonts(self):
        self.title_font = font.Font(family="Cooper Black", size=25, weight='bold')
        self.label_font = font.Font(family='Serif', size=10, weight='bold')
        # Fonts
        self.setting_labels_font = font.Font(family='Serif', size=10, weight='bold')
        self.settings_font = font.Font(family='Serif', size=10)

    def create_variables(self):
        self.avg_var = tk.StringVar(value=str(self.data['avg']))
        self.std_var = tk.StringVar(value=str(self.data['std']))
        self.num_var = tk.StringVar(value=str(self.data['num']))
        self.den_var = tk.StringVar(value=str(self.data['den']))
        self.olp_var = tk.StringVar(value=str(self.data['olp']))
        self.dst_var = tk.StringVar(value=self.data['dst'].capitalize())
        self.pbc_var = tk.BooleanVar(value=self.data['pbc'])
        self.sar_var = tk.BooleanVar(value=self.data['sar'])
        self.dir_var = tk.StringVar(value=self.data['dir'])
        self.dir_var_name = tk.StringVar(value="./foamify" + self.data['dir'][1:])

    def create_styles(self):
        style = ttk.Style(self.root)
        style.configure("Custom.TLabel", background='wheat', foreground='black')
        style.configure("Custom.TEntry", fieldbackground="white", foreground="black")
        style.configure("Custom.TButton", background="lightblue", foreground="black")
        style.configure("Custom.TCheckbutton", background='wheat', foreground='black')

    # Browse the folder request function
    def browse_folder(self, browse_request="Choose Output Directory"):
        my_folder = filedialog.askdirectory(title=browse_request)
        self.dir_var.set(my_folder)
        self.dir_var_name.set(my_folder if len(my_folder) < 47 else '...' + my_folder[-44:])

    def help_gui(self):
        HelpGUI(self.root)

    def apply_values(self):

        self.data = {
            "avg": float(self.avg_var.get()),
            "std": float(self.std_var.get()),
            "num": int(self.num_var.get()),
            "den": float(self.den_var.get()),
            "olp": float(self.olp_var.get()),
            "dst": self.dst_var.get().lower(),
            "pbc": self.pbc_var.get(),
            "sar": self.sar_var.get(),
            "dir": self.dir_var.get() if os.path.exists(self.dir_var.get()) else None
        }
        self.root.destroy()

    # Function to handle cancel
    def cancel(self):
        self.root.destroy()

    def create_widgets(self):
        # Create the title
        # ttk.Label(self.root, text='Foam Gen', font=self.title_font).grid(row=0, column=1, columnspan=2, pady=15)

        # Padding on the right
        ttk.Label(self.root, text=' ').grid(column=0, padx=10)


        # Average Entry
        ttk.Label(self.root, text="Average Ball Radius", font=self.setting_labels_font).grid(row=1, column=1, sticky='w', **self.options)
        ttk.Entry(self.root, textvariable=self.avg_var).grid(row=1, column=2, **self.options)

        # Standard Deviation Entry
        ttk.Label(self.root, text="Radii Polydispersity (CV)", font=self.setting_labels_font).grid(row=2, column=1, sticky='w', **self.options)
        ttk.Entry(self.root, textvariable=self.std_var).grid(row=2, column=2, **self.options)

        # Number Entry
        ttk.Label(self.root, text="Number of Balls", font=self.setting_labels_font).grid(row=3, column=1, sticky='w', **self.options)
        ttk.Entry(self.root, textvariable=self.num_var).grid(row=3, column=2, **self.options)

        # Density Entry/Slider
        ttk.Label(self.root, text="Ball Packing Density", font=self.setting_labels_font).grid(row=4, column=1, sticky='w', **self.options)
        ttk.Entry(self.root, textvariable=self.den_var).grid(row=4, column=2, **self.options)

        # Overlap Entry/Slider
        ttk.Label(self.root, text="Overlap Allowance (r)", font=self.setting_labels_font).grid(row=5, column=1, sticky='w', **self.options)
        ttk.Entry(self.root, textvariable=self.olp_var).grid(row=5, column=2, **self.options)

        # Distribution Dropdown
        ttk.Label(self.root, text="Radii Distribution", font=self.setting_labels_font).grid(row=6, column=1, sticky='w', **self.options)
        dst_options = ["Gamma", "Log-Normal", "Weibull", "Normal", "Half-Normal", "Physical 1 (Devries)",
                       "Physical 2 (Gal-Or)", "Physical 3 (Lemelich)"]
        dst_menu = ttk.Combobox(self.root, textvariable=self.dst_var, values=dst_options, width=14, font=self.settings_font)
        dst_menu.grid(row=6, column=2, **self.options)
        dst_menu.current(dst_options.index(self.data['dst'].capitalize()))

        # Periodic Boundary Condition Checkbox
        ttk.Label(self.root, text="Periodic Boundary", font=self.setting_labels_font).grid(row=7, column=1, sticky='w',
                                                                                      **self.options)
        ttk.Checkbutton(self.root, variable=self.pbc_var).grid(row=7, column=2, **self.options)

        # Standardize Atomic Radii Checkbox
        ttk.Label(self.root, text="Standardize Atomic Radii", font=self.setting_labels_font).grid(row=8, column=1,
                                                                                             sticky='w', **self.options)
        ttk.Checkbutton(self.root, variable=self.sar_var).grid(row=8, column=2, **self.options)

        # Browse output directory
        ttk.Label(self.root, text=" ").grid(row=9, pady=8)
        ttk.Label(self.root, text="Output Directory:", font=self.setting_labels_font).grid(row=10, column=1, sticky='w',
                                                                                      padx=10)
        ttk.Button(self.root, text='Browse', command=self.browse_folder).grid(row=10, column=2, padx=10)
        ttk.Label(self.root, textvariable=self.dir_var_name, font=self.settings_font).grid(row=11, column=1, columnspan=2,
                                                                                 padx=10, sticky='w')

        # Buttons
        ttk.Label(self.root, text=" ").grid(row=12, pady=8)
        ttk.Button(self.root, text="Help", command=self.help_gui).grid(row=13, column=1, sticky='w', pady=5)
        ttk.Button(self.root, text="Cancel", command=self.cancel).grid(row=13, column=1, sticky='e', pady=5)
        ttk.Button(self.root, text="Create Foam", command=self.apply_values).grid(row=13, column=2, sticky='e', **self.options)

        # Run the GUI
        self.root.mainloop()


if __name__ == '__main__':
    my_gui = SettingsGUI()
    myhelp = HelpGUI(my_gui.root)
    print(my_gui.data)
