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
import os
import platform
import tkinter as tk
import webbrowser
if platform.system() == 'Windows':
    import ctypes
    myappid = 'openradioss.jobgui.1.6.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('openradioss.jobgui.1.6.0')
#import time
import subprocess
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Checkbutton

from button_with_highlight import ButtonWithHighlight
from placeholder_entry import PlaceholderEntry
from job_holder import JobHolder

try:
    from vortex_radioss.animtod3plot.Anim_to_D3plot import readAndConvert
    vd3penabled = True
except ImportError:
    # If VortexRadioss Module not present disable d3plot options
    vd3penabled = False

job_holder = JobHolder()
root = tk.Tk()
root.title('OpenRadioss')
if vd3penabled:
    if platform.system() == 'Windows':
        root.geometry('790x105')
        root.minsize(790, 105)
    elif platform.system() == 'Linux':
        root.geometry('910x105')
        root.minsize(910, 105)
    root.resizable(True, True)
    
else:
    if platform.system() == 'Windows':
        root.geometry('700x105')
        root.minsize(700, 105)
    elif platform.system() == 'Linux':
        root.geometry('800x105')
        root.minsize(800, 105)
    root.resizable(True, True)

if platform.system() == 'Windows':    
    root.iconbitmap('./icon/ross.ico')
    icon_folder = tk.PhotoImage(file='./icon/or_folder.png')
    
elif platform.system() == 'Linux':
    icon_image = tk.PhotoImage(file='./icon/ross.png')
    root.iconphoto(True, icon_image)
    icon_folder = tk.PhotoImage(file='./icon/or_folder.png')

def close_window():
    if job_holder.is_empty() or messagebox.askokcancel('Close Window', 'Job is running. Close?'):
        root.destroy()
        quit()

def on_closing():
    # Call the same function as the 'Close' button when the window is closed
    close_window()

def about_dialog():
    messagebox.showinfo("About", "this job submission gui is from OpenRadioss tools" )

def latestv_dialog():
    webbrowser.open("https://github.com/OpenRadioss/OpenRadioss/releases")
def latestgui_dialog():
    webbrowser.open("https://github.com/OpenRadioss/Tools/tree/main/openradioss_gui")
def latestvrad_dialog():
    webbrowser.open("https://github.com/Vortex-CAE/Vortex-Radioss")
def orweb_dialog():
    webbrowser.open("https://openradioss.org")
    
def add_job():
    check_install()
    if job_file_entry.is_placeholder_active() or not os.path.exists(job_file_entry.get_user_input()):
        messagebox.showerror('', 'Select job.')
        return

    input_file = job_file_entry.get_user_input()
    file_extension = os.path.splitext(input_file)[1].lower()

    arg1 = job_file_entry.get_user_input()
    arg2 = nt_entry.get_user_input('1')
    arg3 = np_entry.get_user_input('1')
    # Get the value of single precision based on the checkbox state
    arg4 = 'sp' if single_status.get() else 'dp' 
    # Get the value of vtk-conversion based on the checkbox state
    arg5 = 'yes' if vtk_status.get() else 'no' 
    # Get the value of csv-conversion based on the checkbox state 
    arg6 = 'yes' if csv_status.get() else 'no'
    # Get the value of starter-only based on the checkbox state 
    arg7 = 'yes' if starter_status.get() else 'no'
    if vd3penabled:
    # Get the value of d3plot conversion based on the checkbox state 
        arg8 = 'yes' if d3plot_status.get() else 'no'
    else:
       arg8 = 'no'
    # Call the function to check MPI vars file for windows only
    if platform.system() == 'Windows':
        check_mpi_path()
 
    check_sp_exes()
 
    if messagebox.askokcancel('Add job', 'Add job?'):
        save_config()

        # Get the directory where your script is located
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Provide the absolute path to runopenradioss.py
        runopenradioss_script = os.path.join(script_directory, 'runopenradioss.py')

        if platform.system() == 'Windows':
            allcommand = [runopenradioss_script, os.path.normpath(arg1), arg2, arg3, arg4, arg5, arg6, arg7, arg8]
        elif platform.system() == 'Linux':
            allcommand = ["python3", runopenradioss_script, os.path.normpath(arg1), arg2, arg3, arg4, arg5, arg6, arg7, arg8]

        job_holder.push_job(allcommand)

def show_queue():
    job_holder.show_queue()

def clear_queue():
    job_holder.clear_queue()

def run_job():
    job_holder.run_job()
    root.after(1000, run_job)
    return

def select_file():
    file_path = filedialog.askopenfilename(
        title='Select input file',
        filetypes=[('Radioss or Dyna file', '*.rad *.key *.k')]
    )
    job_file_entry.on_focus_gain()
    job_file_entry.delete(0, tk.END)
    job_file_entry.insert(0, file_path)

def check_mpi_path():
    mpi_path_file = "path_to_intel-mpi.txt"
    if np_entry.get_user_input() > '1' and not os.path.exists(mpi_path_file):
        messagebox.showinfo('', 'Running MPI requires intel mpi installation. Please browse to an intel-mpi location. Or select np = 1')
        directory_path = filedialog.askdirectory(
            title='Select intel-mpi directory'            
        )
        if directory_path:
            with open(mpi_path_file, 'w') as file:
                file.write('"' + directory_path + '"')
    else:
        # MPI path file exists or np <= 1, continue with the script
        pass

def check_sp_exes():
    if platform.system() == 'Windows':
        sp_executable = "../exec/starter_win64_sp.exe"
    elif platform.system() == 'Linux':
        sp_executable = "../exec/starter_linux64_gf_sp"
    if single_status.get() and not os.path.exists(sp_executable):
        messagebox.showinfo('WARNING', 'Single Precision Executables not Installed\n      Please Install or submit without sp option checked')

    else:
        # single precision executables exist continue with script
        pass

def check_install():
    is_installed = "../hm_cfg_files"
    if not os.path.exists(is_installed):
        messagebox.showinfo('INCORRECT INSTALL LOCATION', 'The guiscripts folder needs to be saved inside\n your OpenRadioss Folder\n (Same Folder Level as exec and hm_cfg_files)')

    else:
        # installation location correct continue with script
        pass

def save_config():
    with open('./config/sp', mode='w') as f:
        f.write(str(single_status.get()))
    with open('./config/anim_vtk', mode='w') as f:
        f.write(str(vtk_status.get()))
    with open('./config/th_csv', mode='w') as f:
        f.write(str(csv_status.get()))
    with open('./config/starter', mode='w') as f:
        f.write(str(starter_status.get()))
    if vd3penabled:
        with open('./config/anim_d3plot', mode='w') as f:
            f.write(str(d3plot_status.get()))

def apply_config():
    if os.path.exists('./config/sp'):
        with open('./config/sp', mode='r') as f:
            if f.readline() == 'True':
                single_status.set(True)
    if os.path.exists('./config/anim_vtk'):
        with open('./config/anim_vtk', mode='r') as f:
            if f.readline() == 'True':
                vtk_status.set(True)
    if os.path.exists('./config/th_csv'):
        with open('./config/th_csv', mode='r') as f:
            if f.readline() == 'True':
                csv_status.set(True)
    if os.path.exists('./config/starter'):
        with open('./config/starter', mode='r') as f:
            if f.readline() == 'True':
                starter_status.set(True)
    if os.path.exists('./config/anim_d3plot'):
        if vd3penabled:
            with open('./config/anim_d3plot', mode='r') as f:
                if f.readline() == 'True':
                    d3plot_status.set(True)

frame_file = tk.Frame(root)
frame_file.pack(fill=tk.X, pady=(10,0))
job_file_entry = PlaceholderEntry(frame_file, placeholder_text='Job file (.rad, .key, or .k)', entry_width=83)
job_file_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=(30, 0), ipady=2)
job_file_button = ButtonWithHighlight(frame_file, image=icon_folder, command=select_file, width=20)
job_file_button.pack(side=tk.RIGHT, padx=(5, 30))

frame_thread = tk.Frame(root)
frame_thread.pack(side=tk.LEFT, padx=(30, 0))

# Two separate frames to stack checkboxes
frame_checkboxes = tk.Frame(frame_thread)
frame_checkboxes.pack(side=tk.TOP)

frame_checkboxes1 = tk.Frame(frame_checkboxes)
frame_checkboxes1.pack(side=tk.RIGHT, pady=(5,0))

frame_checkboxes2 = tk.Frame(frame_checkboxes1)
frame_checkboxes2.pack(side=tk.BOTTOM)

if vd3penabled:
    frame_checkboxes3 = tk.Frame(frame_checkboxes2)
    frame_checkboxes3.pack(side=tk.RIGHT)

nt_entry = PlaceholderEntry(frame_checkboxes, placeholder_text='-nt', entry_width=5)
nt_entry.pack(side=tk.LEFT, ipady=2)
np_entry = PlaceholderEntry(frame_checkboxes, placeholder_text='-np', entry_width=5)
np_entry.pack(side=tk.LEFT, padx=5, ipady=2)

single_status = tk.BooleanVar()
single_checkbox = Checkbutton(frame_checkboxes1, text='Single Precision ', variable=single_status)
single_checkbox.pack(side=tk.LEFT, padx=5, ipady=5)
vtk_status = tk.BooleanVar()
vtk_checkbox = Checkbutton(frame_checkboxes1, text='Anim - vtk', variable=vtk_status)
vtk_checkbox.pack(side=tk.LEFT, padx=5, ipady=2)
starter_status = tk.BooleanVar()
starter_checkbox = Checkbutton(frame_checkboxes2, text='Run Starter Only', variable=starter_status)
starter_checkbox.pack(side=tk.LEFT, padx=5, ipady=2)
if vd3penabled:
    d3plot_status = tk.BooleanVar()
    d3plot_checkbox = Checkbutton(frame_checkboxes2, text='Anim - d3plot', variable=d3plot_status)
    d3plot_checkbox.pack(side=tk.LEFT, padx=5, ipady=2)
csv_status = tk.BooleanVar()
if vd3penabled:
    csv_checkbox = Checkbutton(frame_checkboxes3, text='TH - csv', variable=csv_status)
    csv_checkbox.pack(side=tk.LEFT)
else:
    csv_checkbox = Checkbutton(frame_checkboxes2, text='TH - csv    ', variable=csv_status)
    csv_checkbox.pack(side=tk.LEFT, padx=5, ipady=2)

frame_control = tk.Frame(root)
frame_control.pack(side=tk.RIGHT, padx=(0, 30))
if platform.system() == 'Windows':
    add_button = ButtonWithHighlight(frame_control, text='Add Job', command=add_job, width=7)
elif platform.system() == 'Linux':
    add_button = ButtonWithHighlight(frame_control, text='Add Job', command=add_job, width=8)
add_button.pack(side=tk.LEFT, padx=(0, 5))
if platform.system() == 'Windows':
    show_queue_button = ButtonWithHighlight(frame_control, text='Show Queue', command=show_queue, width=7)
elif platform.system() == 'Linux':
    show_queue_button = ButtonWithHighlight(frame_control, text='Show Queue', command=show_queue, width=8)    
show_queue_button.pack(side=tk.LEFT, padx=5)
if platform.system() == 'Windows':
    clear_queue_button = ButtonWithHighlight(frame_control, text='Clear Queue', command=clear_queue, width=7)
elif platform.system() == 'Linux':
    clear_queue_button = ButtonWithHighlight(frame_control, text='Clear Queue', command=clear_queue, width=8)
clear_queue_button.pack(side=tk.LEFT, padx=5)
if platform.system() == 'Windows':
    close_button = ButtonWithHighlight(frame_control, text='Close', command=close_window, width=7)
elif platform.system() == 'Linux':
    close_button = ButtonWithHighlight(frame_control, text='Close', command=close_window, width=8)
close_button.pack(side=tk.LEFT, padx=(5, 0))

# Create a menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Create an About menu
about_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="Info", menu=about_menu)
about_menu.add_command(label="Get the latest version of OpenRadioss (github link)", command=latestv_dialog)
about_menu.add_command(label="Documentation and Latest Version of this gui (github_link)", command=latestgui_dialog)
about_menu.add_command(label="Get the latest version of the VortexRadioss d3plot python module (github link)", command=latestvrad_dialog)
about_menu.add_command(label="Visit the OpenRadioss web page", command=orweb_dialog)
about_menu.add_command(label="About this gui", command=about_dialog)

apply_config()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.after(1000, run_job)
root.mainloop()
