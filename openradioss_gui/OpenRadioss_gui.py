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
import json
import platform
import tkinter as tk
if platform.system() == 'Windows':
    import ctypes
    myappid = 'openradioss.jobgui.1.6.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('openradioss.jobgui.1.6.0')
#import time
import subprocess
from tkinter import filedialog
from tkinter import messagebox
from job_holder import JobHolder

try:
    from vortex_radioss.animtod3plot.Anim_to_D3plot import readAndConvert
    vd3penabled = True
except ImportError:
    # If VortexRadioss Module not present disable d3plot options
    vd3penabled = False
import gui_def

# Global Variables  
current_platform=platform.system() 
debug=0
job_holder = JobHolder(debug)
Window     = gui_def.window(vd3penabled)

#-------------------------------- Functions #--------------------------------
# Close the app when the close button is clicked or the window is closed
# no job is running or the user confirms the close action
#----------------------------------------------------------------------------
def close_window():
    if job_holder.is_empty() or messagebox.askokcancel('Close Window', 'Job is running. Close?'):
        Window.close()
        quit()


#-------------------------------- Functions #--------------------------------
# Queues the job when the add job button is clicked
#----------------------------------------------------------------------------
def add_job():
    check_install()

    if job_file_entry.is_placeholder_active() or not os.path.exists(job_file_entry.get_user_input()):
        messagebox.showerror('', 'Select job.')
        return

    # Get Values based on Checkbox Statuses
    file         = job_file_entry.get_user_input()
    nt           = nt_entry.get_user_input('1')
    np           = np_entry.get_user_input('1')
    precision    = 'sp' if single_status.get() else 'dp' 
    anim_to_vtk  = 'yes' if vtk_status.get() else 'no'
    th_to_csv    = 'yes' if csv_status.get() else 'no'
    starter_only = 'yes' if starter_status.get() else 'no'
    if vd3penabled:
        d3plot = 'yes' if d3plot_status.get() else 'no'
    else:
        d3plot = 'no'

    allcommand = [os.path.normpath(file), nt, np, precision, anim_to_vtk, th_to_csv, starter_only, d3plot]
 
    # Add Job in Queue
    if messagebox.askokcancel('Add job', 'Add job?'):
        save_config()
        if debug==1:print("Allcommand: ",allcommand)
        job_holder.push_job(allcommand)

def show_queue():
    job_holder.show_queue()

def clear_queue():
    job_holder.clear_queue()

def run_job():
    job_holder.run_job()
    Window.root.after(1000, run_job)
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

# Create Json Config File & write on disk
def save_config():
    config={}
    config['starter_only'] = starter_status.get()
    config['vtk'] = vtk_status.get()
    config['sp'] = single_status.get()
    config['csv'] = csv_status.get()
    if vd3penabled:
        config['d3plot'] = d3plot_status.get()
    config['np'] = np_entry.get_user_input()
    config['nt'] = nt_entry.get_user_input()

    # Open File & Write Json file
    if current_platform == 'Windows': 
        username = os.environ.get('USERNAME')
        directory = os.path.join('C:\\Users', username, 'AppData','Local','OpenRadioss_GUI')
    else:
        home=os.environ.get('HOME')
        directory = os.path.join(home,'.OpenRadioss_GUI')

    if not os.path.exists(directory):
        os.makedirs(directory)

    json_file=os.path.join(directory, 'config.json')
    with open(json_file, mode='w') as file:
            json.dump(config, file, indent=4)
            file.close()

def load_config():
    if current_platform == 'Windows':
       username = os.environ.get('USERNAME')
       directory = os.path.join('C:\\Users', username, 'AppData','Local','OpenRadioss_GUI')
    else:
       home=os.environ.get('HOME') 
       directory = os.path.join(home,'.OpenRadioss_GUI')

    if not os.path.exists(directory):
        os.makedirs(directory)
    
    json_file=os.path.join(directory, 'config.json')
    print('Json File:',json_file)
    try:
        with open(json_file, mode='r') as file:
            config_file=json.load(file)
            file.close()

            starter_status.set(config_file['starter_only'])
            vtk_status.set(config_file['vtk'])
            single_status.set(config_file['sp'])
            csv_status.set(config_file['csv'])
            if vd3penabled:
               d3plot_status.set(config_file['d3plot'])
            
    except:
        config_file={}

# ===========================================
# Main entry point
# ===========================================
if __name__ == "__main__":
#----------------------------- GUI Elements #--------------------------------
# File Menu
  job_file_entry=Window.file('Job file (.rad, .key, or .k)', select_file, Window.icon_folder)

  # Create checkboxes
  nt_entry          = Window.thread_mpi('-nt', 5,0,2)
  np_entry          = Window.thread_mpi('-np', 5,5,2)
  single_status     = Window.checkbox1('Single Precision ',5,5)
  vtk_status        = Window.checkbox1('Anim - vtk',5,2)
  starter_status    = Window.checkbox2('Run Starter Only',5,2)
  if vd3penabled:
    d3plot_status = Window.checkbox2('Anim - d3plot',5,2)
    csv_status    = Window.checkbox3('TH - csv',0,0)
  else:
    csv_status    = Window.checkbox2('TH - csv    ',5,2)

  # Create buttons
  Window.button('Add Job', add_job, (0, 5))
  Window.button('Show Queue', show_queue, 5)
  Window.button('Clear Queue', clear_queue, 5)
  Window.button('Close', close_window, (5, 0))

  # Create a menu bar
  Window.menubar('Info')

  load_config()
  Window.root.protocol("WM_DELETE_WINDOW", close_window)
  Window.root.after(1000, run_job)
  Window.root.mainloop()
