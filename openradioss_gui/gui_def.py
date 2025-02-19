# Copyright 1986-2025 Altair Engineering Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import os

import tkinter as tk
from tkinter import messagebox
import platform
import webbrowser

from button_with_highlight import ButtonWithHighlight
from placeholder_entry import PlaceholderEntry

arch=platform.system()

if arch=='Windows':
    button_width=7
elif arch=='Linux':
    button_width=8

# Establish common path for all resources, e.g. icons need an absolute path for them to work correctly in packaging the application
OPENRADIOSS_GUI_PATH = os.path.dirname(os.path.abspath(__file__))

class window:
    def __init__(self, vd3penabled, vtkhdfenabled):
        self.root = tk.Tk()
        self.root.title('OpenRadioss')
        self.vd3penabled = vd3penabled
        self.vtkhdfenabled = vtkhdfenabled

        if arch == 'Windows':
            self.root.geometry('700x105')
            self.root.minsize(700, 105)
        elif arch == 'Linux':
            self.root.geometry('800x105')
            self.root.minsize(800, 105)
        self.root.resizable(True, True)

        # Icons
        if arch == 'Windows':
             self.root.iconbitmap(OPENRADIOSS_GUI_PATH + '\\icon\\ross.ico')
             self.icon_folder = tk.PhotoImage(file=OPENRADIOSS_GUI_PATH + '\\icon/or_folder.png')
        elif arch == 'Linux':
             icon_image = tk.PhotoImage(file=OPENRADIOSS_GUI_PATH + '\\icon/ross.png')
             self.root.iconphoto(True, icon_image)
             self.icon_folder = tk.PhotoImage(file=OPENRADIOSS_GUI_PATH + '\\icon/or_folder.png')

        # Dropdown Variables
        self.variables = {
            'Single Precision': tk.BooleanVar(),
            'Run Starter Only': tk.BooleanVar(),
            'Anim - vtk': tk.BooleanVar(),
            'Anim - vtkhdf': tk.BooleanVar(),
            'Anim - d3plot': tk.BooleanVar(),
            'TH - csv': tk.BooleanVar(),
        }

        self.variable_flags = {
            'Single Precision': 'single_status',
            'Run Starter Only': 'starter_status',
            'Anim - vtk': 'vtk_status',
            'Anim - vtkhdf': 'vtkhdf_status',
            'Anim - d3plot': 'd3plot_status',
            'TH - csv': 'csv_status',
        }

        # Frame file
        self.frame_file = tk.Frame(self.root)
        self.frame_file.pack(fill=tk.X, pady=(10,0))

        # Frame thread / MPI
        self.frame_thread = tk.Frame(self.root)
        self.frame_thread.pack(side=tk.LEFT, padx=(30, 0))

        self.frame_checkboxes = tk.Frame(self.frame_thread)
        self.frame_checkboxes.pack(side=tk.TOP)

        # Frame for Dropdown
        self.frame_dropdown = tk.Frame(self.frame_checkboxes)
        self.frame_dropdown.pack(side=tk.RIGHT)

        # Dropdown Button
        self.dropdown_button = tk.Menubutton(self.frame_dropdown, text="Run Options", relief=tk.RAISED)
        self.dropdown_menu = tk.Menu(self.dropdown_button, tearoff=False)
        self.dropdown_button.config(menu=self.dropdown_menu)

        # Buttons Frame
        self.frame_control = tk.Frame(self.root)
        self.frame_control.pack(side=tk.RIGHT, padx=(0, 30))

        # Explicitly add all labels to the dropdown
        for label in self.variables:
            if label == 'Anim - vtkhdf' and not vtkhdfenabled:
                continue  # Skip Anim - vtkhdf if vtkhdfenabled is False
            if label == 'Anim - d3plot' and not vd3penabled:
                continue  # Skip Anim - d3plot if vd3penabled is False

            # Add the checkbox to the dropdown menu
            self.dropdown_menu.add_checkbutton(label=label, variable=self.variables[label])

        # Pack the dropdown button
        self.dropdown_button.pack(side=tk.LEFT, padx=5)

    def get_selected_options(self):
        # Return the current state of the dropdown variables
        return self.variables

    def menubar(self,title):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        if title=='Info':
            self.about_menu = tk.Menu(self.menubar, tearoff=False)
            self.menubar.add_cascade(label="Info", menu=self.about_menu)
            self.about_menu.add_command(label="Get the latest version of OpenRadioss (github link)", command=self._latestv_dialog)
            self.about_menu.add_command(label="Documentation and Latest Version of this gui (github_link)", command=self._latestgui_dialog)
            self.about_menu.add_command(label="Get the latest version of the VortexRadioss d3plot python module (github link)", command=self._latestvrad_dialog)
            self.about_menu.add_command(label="Get the latest version of the kitware animtovtkhdf python module (gitlab link)", command=self._latestvtkh_dialog)
            self.about_menu.add_command(label="Visit the OpenRadioss web page", command=self._orweb_dialog)
            self.about_menu.add_command(label="About this gui", command=self._about_dialog)

    def file(self,text,command,icon_folder):
        job_file_entry = PlaceholderEntry(self.frame_file, placeholder_text=text, entry_width=83)
        job_file_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=(30, 0), ipady=2)
        job_file_button = ButtonWithHighlight(self.frame_file, image=icon_folder, command=command, width=20)
        job_file_button.pack(side=tk.RIGHT, padx=(5, 30))
        return job_file_entry

    def thread_mpi(self,text,width,px,py):
        entry = PlaceholderEntry(self.frame_checkboxes, placeholder_text=text, entry_width=width)
        entry.pack(side=tk.LEFT,padx=px,ipady=py)
        return entry
    
    def button(self, text, command, pad):
        button = ButtonWithHighlight(self.frame_control, text=text, command=command,width=button_width)        
        button.pack(side=tk.LEFT, padx=pad)

    def close(self):
           self.root.destroy()

    # Private methods for menu bar
    def _latestv_dialog(self):
          webbrowser.open("https://github.com/OpenRadioss/OpenRadioss/releases")
    def _latestgui_dialog(self):
          webbrowser.open("https://github.com/OpenRadioss/Tools/tree/main/openradioss_gui")
    def _latestvrad_dialog(self):
          webbrowser.open("https://github.com/Vortex-CAE/Vortex-Radioss")
    def _latestvtkh_dialog(self):
          webbrowser.open("https://gitlab.kitware.com/keu-public/openradioss-to-vtkhdf")
    def _orweb_dialog(self):
          webbrowser.open("https://openradioss.org")
    def _about_dialog(self):
          messagebox.showinfo("About", "this job submission gui is from OpenRadioss tools" )

