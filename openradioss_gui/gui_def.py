# Copyright 1986-2024 Altair Engineering Inc.
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


class window:
    def __init__(self,vd3penabled):
        self.root = tk.Tk()
        self.root.title('OpenRadioss')
        if vd3penabled:
             if arch == 'Windows':
                self.root.geometry('790x105')
                self.root.minsize(790, 105)
             elif arch == 'Linux':
                self.root.geometry('910x105')
                self.root.minsize(910, 105)
             self.root.resizable(True, True)
        else:
             if arch == 'Windows':
                self.root.geometry('700x105')
                self.root.minsize(700, 105)
             elif arch == 'Linux':
                self.root.geometry('800x105')
                self.root.minsize(800, 105)
             self.root.resizable(True, True)

        # Icons
        if arch == 'Windows':
             self.root.iconbitmap('./icon/ross.ico')
             self.icon_folder = tk.PhotoImage(file='./icon/or_folder.png')
        elif arch == 'Linux':
             icon_image = tk.PhotoImage(file='./icon/ross.png')
             self.root.iconphoto(True, icon_image)
             self.icon_folder = tk.PhotoImage(file='./icon/or_folder.png')

        # Frame file
        self.frame_file = tk.Frame(self.root)
        self.frame_file.pack(fill=tk.X, pady=(10,0))

        # Frame thread / MPI
        self.frame_thread = tk.Frame(self.root)
        self.frame_thread.pack(side=tk.LEFT, padx=(30, 0))

        self.frame_checkboxes = tk.Frame(self.frame_thread)
        self.frame_checkboxes.pack(side=tk.TOP)

        self.frame_checkboxes1 = tk.Frame(self.frame_checkboxes)
        self.frame_checkboxes1.pack(side=tk.RIGHT, pady=(5,0))

        self.frame_checkboxes2 = tk.Frame(self.frame_checkboxes1)
        self.frame_checkboxes2.pack(side=tk.BOTTOM)

        if vd3penabled:
          self.frame_checkboxes3 = tk.Frame(self.frame_checkboxes2)
          self.frame_checkboxes3.pack(side=tk.RIGHT)

        # Buttons Frame
        self.frame_control = tk.Frame(self.root)
        self.frame_control.pack(side=tk.RIGHT, padx=(0, 30))


    def menubar(self,title):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        if title=='Info':
            self.about_menu = tk.Menu(self.menubar, tearoff=False)
            self.menubar.add_cascade(label="Info", menu=self.about_menu)
            self.about_menu.add_command(label="Get the latest version of OpenRadioss (github link)", command=self._latestv_dialog)
            self.about_menu.add_command(label="Documentation and Latest Version of this gui (github_link)", command=self._latestgui_dialog)
            self.about_menu.add_command(label="Get the latest version of the VortexRadioss d3plot python module (github link)", command=self._latestvrad_dialog)
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
    
    def checkbox1(self,text,px,py):
        status = tk.BooleanVar()
        checkbox = tk.Checkbutton(self.frame_checkboxes1, text=text, variable=status)
        checkbox.pack(side=tk.LEFT, padx=px, ipady=py)
        return status

    def checkbox2(self,text,px,py):
        status = tk.BooleanVar()
        checkbox = tk.Checkbutton(self.frame_checkboxes2, text=text, variable=status)
        checkbox.pack(side=tk.LEFT, padx=px, ipady=py)
        return status
    
    def checkbox3(self,text,px,py):
        status = tk.BooleanVar()
        checkbox = tk.Checkbutton(self.frame_checkboxes2, text=text, variable=status)
        checkbox.pack(side=tk.LEFT, padx=px, ipady=py)
        return status

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
    def _orweb_dialog(self):
          webbrowser.open("https://openradioss.org")
    def _about_dialog(self):
          messagebox.showinfo("About", "this job submission gui is from OpenRadioss tools" )






