# Copyright 1986-2026 Altair Engineering Inc.
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
import sys
import argparse
import json
import platform
import tkinter as tk
if platform.system() == 'Windows':
    import ctypes
    myappid = 'openradioss.jobgui.1.7.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('openradioss.jobgui.1.7.0')
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
try:
    from animtovtkhdf import AnimToVTKHDF
    vtkhdfenabled = True
except ImportError:
    vtkhdfenabled = False
import gui_def
from runopenradioss import RunOpenRadioss


class openradioss_gui:

      def __init__(self,debug,script_dir):
        # Global Variables
        self.debug=debug
        self.script_dir=script_dir
        self.mpi_path = ''
        self.current_platform = platform.system()

        self.load_config()

        self.job_holder = JobHolder(self.debug)
        # Check if the user has selected a valid MPI path
        self.Window     = gui_def.window(vd3penabled, vtkhdfenabled,self.mpi_path,self.single_status,self.starter_status,self.vtk_status,self.csv_status,self.vtkhdf_status,self.d3plot_status,script_dir)
     
        self.job_file_entry=self.Window.file('Job file (.rad, .key, or .k, or .inp)', self.select_file, self.Window.icon_folder)
     
        # Dropdown to set variables
        selected_flags = self.Window.get_selected_options()
    
        # Assign tk.BooleanVar objects
        self.single_status = selected_flags['Single Precision']
        self.starter_status = selected_flags['Run Starter Only']
        self.vtk_status = selected_flags['Anim - vtk']
        self.vtkhdf_status = selected_flags['Anim - vtkhdf']
        self.d3plot_status = selected_flags['Anim - d3plot']
        self.csv_status = selected_flags['TH - csv']

        # Create checkboxes
        self.nt_entry = self.Window.thread_mpi('-nt', 5, 0, 2)
        self.np_entry = self.Window.thread_mpi('-np', 5, 5, 2)
    
        # Create buttons
        self.Window.button('Add Job', self.add_job, (0, 5))
        self.Window.button('Show Queue', self.show_queue, 6)
        self.Window.button('Clear Queue', self.clear_queue, 6)
        self.Window.button('Close', self.close_window, (5, 0))

        # Create a menu bar
        self.Window.menubar()

        self.Window.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.Window.root.after(1000, self.run_job)
    
        self.Window.root.mainloop()

        
      #-------------------------------- Functions #--------------------------------
      # Close the app when the close button is clicked or the window is closed
      # no job is running or the user confirms the close action
      #----------------------------------------------------------------------------
      def close_window(self):
         if self.job_holder.is_empty() or messagebox.askokcancel('Close Window', 'Job is running. Close?'):
           self.Window.close()
           quit()


      #-------------------------------- Functions #--------------------------------
      # Queues the job when the add job button is clicked
      #----------------------------------------------------------------------------
      def add_job(self):
           self.check_install()
     

           if self.job_file_entry.is_placeholder_active() or not os.path.exists(self.job_file_entry.get_user_input()):
               messagebox.showerror('', 'Select job.')
               return

           # Get Values based on Checkbox Statuses
           file         = self.job_file_entry.get_user_input()
           nt           = self.nt_entry.get_user_input('1')
           np           = self.np_entry.get_user_input('1')
           precision    = 'sp' if self.single_status.get() else 'dp' 
           anim_to_vtk  = 'yes' if self.vtk_status.get() else 'no'
           if vtkhdfenabled:
               anim_to_vtkhdf = 'yes' if self.vtkhdf_status.get() else 'no'
           else:
               anim_to_vtkhdf = 'no'
           th_to_csv    = 'yes' if self.csv_status.get() else 'no'
           starter_only = 'yes' if self.starter_status.get() else 'no'
           if vd3penabled:
               d3plot = 'yes' if self.d3plot_status.get() else 'no'
           else:
               d3plot = 'no'

           self.mpi_path = self.Window.mpi_path
           # print('mpi_path='+self.mpi_path)

           allcommand = [os.path.normpath(file), nt, np, precision, anim_to_vtk, th_to_csv, starter_only, d3plot, anim_to_vtkhdf,self.mpi_path]

           # Add Job in Queue
           if messagebox.askokcancel('Add job', 'Add job?'):
               self.save_config()
               if self.debug==1:print("Allcommand: ",allcommand)
               self.job_holder.push_job(allcommand)

      def show_queue(self):
           self.job_holder.show_queue()

      def clear_queue(self):
           self.job_holder.clear_queue()

      def run_job(self):
           self.job_holder.run_job()
           self.Window.root.after(1000, self.run_job)
           return

      def select_file(self):
           file_path = filedialog.askopenfilename(
               title='Select input file',
               filetypes=[('Radioss file', '*.rad *.key *.k *.inp' )]
           )
           self.job_file_entry.on_focus_gain()
           self.job_file_entry.delete(0, tk.END)
           self.job_file_entry.insert(0, file_path)

      def check_sp_exes(self):
           if platform.system() == 'Windows':
               sp_executable = "../exec/starter_win64_sp.exe"
           elif platform.system() == 'Linux':
               sp_executable = "../exec/starter_linux64_gf_sp"
           if self.single_status.get() and not os.path.exists(sp_executable):
               messagebox.showinfo('WARNING', 'Single Precision Executables not Installed\n      Please Install or submit without sp option checked')

           else:
               # single precision executables exist continue with script
               pass

      def check_install(self):
           is_installed = self.script_dir +os.sep +".."+os.sep+"hm_cfg_files"
           if not os.path.exists(is_installed):
               messagebox.showinfo('INCORRECT INSTALL LOCATION', 'The guiscripts folder needs to be saved inside\n your OpenRadioss Folder\n (Same Folder Level as exec and hm_cfg_files)')

           else:
               # installation location correct continue with script
               pass

      # Create Json Config File & write on disk
      def save_config(self):
           config={}
           config['starter_only'] = self.starter_status.get()
           config['vtk'] = self.vtk_status.get()
           config['sp'] = self.single_status.get()
           config['csv'] = self.csv_status.get()
           if vtkhdfenabled:
                config['vtkhdf'] = self.vtkhdf_status.get()
           if vd3penabled:
               config['d3plot'] = self.d3plot_status.get()
           config['np'] = self.np_entry.get_user_input()
           config['nt'] = self.nt_entry.get_user_input()
           config['mpi_path'] = self.mpi_path

           # Open File & Write Json file
           if self.current_platform == 'Windows': 
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

      def load_config(self):
           
           self.single_status = False
           self.starter_status = False
           self.vtk_status = False
           self.csv_status = False   
           self.vtkhdf_status = False
           self.d3plot_status = False
           
           if self.current_platform == 'Windows':
              username = os.environ.get('USERNAME')
              directory = os.path.join('C:\\Users', username, 'AppData','Local','OpenRadioss_GUI')
           else:
              home=os.environ.get('HOME') 
              directory = os.path.join(home,'.OpenRadioss_GUI')

           if not os.path.exists(directory):
               os.makedirs(directory)


           json_file=os.path.join(directory, 'config.json')
           # print('Json File:',json_file)
           try:
               with open(json_file, mode='r') as file:
                   config_file=json.load(file)
                   file.close()

                   if "mpi_path" in config_file:
                     self.mpi_path = config_file['mpi_path']
                   else:
                      self.mpi_path = ''
                   #
                   if "sp" in config_file:
                        self.single_status=config_file['sp']
                   else:
                        self.single_status="false"
                   #
                   if 'starter_only' in config_file:
                       self.starter_status=config_file['starter_only']
                   else:
                       self.starter_status=False
                   #
                   if 'vtk' in config_file:
                          self.vtk_status=config_file['vtk']
                   else:
                          self.vtk_status=False
                   #
                   if 'csv' in config_file:
                          self.csv_status=config_file['csv']
                   else:
                          self.csv_status=False
                   #
                   self.vtkhdf_status=False
                   if vtkhdfenabled:
                        if 'vtkhdf' in config_file:
                            self.vtkhdf_status=config_file['vtkhdf']

                   self.d3plot_status=False
                   if vd3penabled:
                      if 'd3plot' in config_file:
                          self.d3plot_status=config_file['d3plot']

           except:
               config_file={}

# ===========================================
# Main entry point
# ===========================================
if __name__ == "__main__":
#----------------------------- GUI Elements #--------------------------------
# File Menu
  num_args = len(sys.argv) - 1
  parser = argparse.ArgumentParser(description='OpenRadioss GUI')
  parser.add_argument('-gui', '--gui',action='store_true', default=False, help='Enable GUI mode')
  parser.add_argument('-i', '--input', type=str, help='The input file to process in form:  filename<.k|.key>, filename_<runnumber 4 digits>.rad or filename.inp')
  parser.add_argument('-nt', '--nt', type=int, metavar='n', help='Number of threads')
  parser.add_argument('-np', '--np', type=int, metavar='p', help='Number of MPI process')
  parser.add_argument('-sp', '--sp', action='store_true', default=False, help='Enable Extended Single precision mode (default is double precision)')
  parser.add_argument('-starter', '--starter_only', action='store_true', default=False, help='Enable Starter Only mode')
  parser.add_argument('-th_to_csv', '--th_to_csv', action='store_true', default=False, help='Enable TH to CSV conversion')
  parser.add_argument('-anim_to_vtk', '--anim_to_vtk', action='store_true', default=False, help='Enable Animation to VTK conversion')
  parser.add_argument('-anim_to_d3plot', '--anim_to_d3plot', action='store_true', default=False, help='Enable Animation to D3plot conversion (need VortexRadioss installed)')
  parser.add_argument('-anim_to_vtkhdf', '--anim_to_vtkhdf', action='store_true', default=False, help='Enable Animation to VTKHDF conversion (need VTKHDF installed)')
  parser.add_argument('-mpi_path', '--mpi_path', type=str, help='Path to MPI installation')
  parser.add_argument('-d', '--debug',action='store_true', default=False, help='Enable debug mode')
  args = parser.parse_args()

  script_dir = os.path.abspath(__file__)
  script_dir = os.path.dirname(script_dir)+os.sep
  if num_args > 0:
      if args.gui:
          debug=1 if args.debug else 0
          gui= openradioss_gui(debug,script_dir)
          exit(0)
      if not args.input:
          print(" ")
          print("Error: Input file is required in non-GUI mode.")
          print(" ")

          parser.print_help()
          exit(1)

      if not args.nt: args.nt=1
      if not args.np: args.np=1
    
      command = []
      command.append(args.input)
      command.append(str(args.nt))
      command.append(str(args.np))
      command.append("sp" if args.sp else "dp")  # precision
      command.append("yes" if args.anim_to_vtk else "no")  # anim_to_vtk
      command.append("yes" if args.th_to_csv else "no")  # th_to_csv
      command.append("yes" if args.starter_only else "no")  # starter_only
      command.append("yes" if args.anim_to_d3plot else "no")  # anim_to_d3plot
      command.append("yes" if args.anim_to_vtkhdf else "no")  # anim_to_vtkhdf
      command.append(args.mpi_path if args.mpi_path else "")    # mpi_path

      Run_OR= RunOpenRadioss(command, debug=1 if args.debug else 0)
      Run_OR.batch_run()

  else: 
      script_dir = os.path.abspath(__file__)
      script_dir = os.path.dirname(script_dir)+os.sep
      gui= openradioss_gui(0,script_dir)
