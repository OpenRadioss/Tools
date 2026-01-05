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
import re
import platform
import contextlib
import subprocess
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from runopenradioss import RunOpenRadioss
from button_with_highlight import ButtonWithHighlight

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

current_platform = platform.system()


class RedirectText:
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)
        self.widget.update_idletasks()

    def flush(self):
        pass  # Required for compatibility with sys.stdout

class JobWindow():

    def __init__(self, command,debug):
        #Debug flag activated in OpenRadioss_gui.py
        script_dir = os.path.abspath(__file__)
        self.script_dir = os.path.dirname(script_dir)+os.sep
        self.debug=debug
        self.command = command
        self.job_dir = os.path.dirname(command[0])
        self.stop_after_starter=False
        jnm1 = command[0]
        mpi_path= command[9]

        # Create an instance of RunOpenRadioss
        self.runOpenRadioss = RunOpenRadioss(self.command,self.debug)
        self.job_name,self.decktype = self.runOpenRadioss.get_decktype()
        self.jobname,self.run_id,self.exec_dir=self.runOpenRadioss.get_jobname_runid_rundirectory()
        # Gather the jobname, run_id, job directory from the command

        self.is_finished = False

        self.window = tk.Toplevel()
        self.window.title(self.job_name)
        
        # Initially disable 'X' button while job is running
        self.window.protocol('WM_DELETE_WINDOW', (lambda: 'pass'))
        if platform.system() == 'Windows':
            self.window.iconbitmap(self.script_dir+'icon'+os.sep+'ross.ico')
        elif platform.system() == 'Linux':
            icon_image = tk.PhotoImage(file=self.script_dir+'icon'+os.sep+'ross.png')
            self.window.iconphoto(True, icon_image)
        
        # Configure grid layout for the window
        self.window.rowconfigure(0, weight=1)  # Row for ScrolledText expands
        self.window.rowconfigure(1, weight=0)  # Row for buttons remains fixed
        self.window.columnconfigure(0, weight=1)
        
        # ScrolledText widget
        self.log_text = scrolledtext.ScrolledText(self.window, width=100, height=40)
        self.log_text.grid(row=0, column=0, sticky="nsew", padx=30, pady=(30, 10))
        
        # Frame for buttons (anchored at the bottom)
        self.frame_control = tk.Frame(self.window, padx=10, pady=5)
        self.frame_control.grid(row=1, column=0, pady=(10, 20))
        
        # Add buttons to the frame
        self.stop_button = ButtonWithHighlight(self.frame_control, text='Stop', command=self.stop_job, padx=30)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        self.kill_button = ButtonWithHighlight(self.frame_control, text='Kill', command=self.kill_job, padx=30)
        self.kill_button.pack(side=tk.LEFT, padx=5)
        self.anim_button = ButtonWithHighlight(self.frame_control, text='Anim', command=self.anim_job, padx=30)
        self.anim_button.pack(side=tk.LEFT, padx=5)
        self.h3d_button = ButtonWithHighlight(self.frame_control, text='h3d', command=self.h3d_job, padx=30)
        self.h3d_button.pack(side=tk.LEFT, padx=5)
        if vd3penabled:
            self.d3p_button = ButtonWithHighlight(self.frame_control, text='d3plot', command=self.d3p_job, padx=30)
            self.d3p_button.pack(side=tk.LEFT, padx=5)
        
        self.close_button = ButtonWithHighlight(self.frame_control, text='Close', state='disable', command=self.on_close, padx=30)
        self.close_button.pack(side=tk.LEFT, padx=5)
        
        # Start the thread
        self.th = threading.Thread(target=self.run_single_job)
        self.th.start()

    # ------------------------------------------------
    # Close : Close the window
    # ------------------------------------------------
    def on_close(self):
        self.window.destroy()

    # ------------------------------------------------
    # Stop button : Stop after Starter or Stop Engine
    # ------------------------------------------------
    def stop_job(self):
        if self.run_number == 0:
           # Starter Phase - Stop after Starter
            if self.stop_after_starter is True:
                messagebox.showinfo('Already Stopping', 'Job stop already requested, will stop at end of Starter')
            else:
                if messagebox.askokcancel('Stop', 'Stop job at end of starter phase?'):
                    self.stop_after_starter = True
        else :
            # Behavior for 'running_en_' files
            if messagebox.askokcancel('Stop', 'Stop Job?'):
                f = open(self.job_dir + '/' + self.job_name+"_"+str( self.run_number).zfill(4)+ '.ctl', mode='w')
                f.write('/STOP')
                f.close()
                self.stop_after_engine = True
    # ------------------------------------------------
    # KILL button : Kill after Starter or Stop Engine
    # ------------------------------------------------
    def kill_job(self):
        if self.run_number == 0:
            # Starter Phase - Stop after Starter
            if self.stop_after_starter is True:
                messagebox.showinfo('Already Stopping', 'Job stop already requested, will stop at end of Starter')
            else:
                if messagebox.askokcancel('Kill', 'Stop job at end of starter phase?'):
                    self.stop_after_starter = True
        else:
            if messagebox.askokcancel('Kill', 'Kill Job?'):
                f = open(self.job_dir + '/' + self.job_name+"_"+str( self.run_number).zfill(4)+ '.ctl', mode='w')
                f.write('/KILL')
                f.close()
                self.stop_after_engine = True

    # ------------------------------------------------
    # ANIM button : Write animation
    # ------------------------------------------------
    def anim_job(self):
        if self.run_number == 0:
            messagebox.showinfo('Starter Phase', 'Job is still in starter phase.\nCannot write Animation file')
        else:
            f = open(self.job_dir + '/' + self.job_name+"_"+str( self.run_number).zfill(4)+ '.ctl', mode='w')
            f.write('/ANIM')
            f.close()

    # ------------------------------------------------
    # H3D button : Write H3D File
    # ------------------------------------------------
    def h3d_job(self):
        if self.run_number == 0:
            messagebox.showinfo('Starter Phase', 'Job is still in starter phase.\nCannot write H3D State')
        else:
            f = open(self.job_dir + '/' + self.job_name+"_"+str( self.run_number).zfill(4)+ '.ctl', mode='w')
            f.write('/H3D')
            f.close()

    # -----------------------------------------------------
    # D3Plot button : Convert Current Anim Files to d3plot
    # -----------------------------------------------------
    def d3p_job(self):
        if vd3penabled is False:
            messagebox.showinfo('D3Plot Not available', 'D3Plot Converter is not available')
        else:
            if self.run_number == 0:
                messagebox.showinfo('Starter Phase', 'Job is still in starter phase.\nCannot convert Anim files to d3plot')
            else:
                anim_pattern = re.compile(self.job_name + r"A[0-9]{3,}(?:[0-9])?$")
                anim_files = [file for file in os.listdir(self.job_dir) if anim_pattern.match(file)]

                if anim_files:
                    # If anim files exist, ask the user if they want to convert them
                    if messagebox.askokcancel('d3plot', 'Create d3plots of existing anim files?'):
                        file_stem = os.path.join(self.job_dir, self.job_name)
                    # Use the file stem to call readAndConvert
                    try:
                        readAndConvert(file_stem,silent=True)
                    except Exception as e:
                        messagebox.showinfo('Error', 'Error in d3plot conversion: ' + str(e))

    # -------------------------------------------------------------------------
    # Job Process : Run Starter and Engine(s) with environment / Stdout in GUI
    # -------------------------------------------------------------------------
    def job_process(self,starter_command_line,custom_env,exec_dir):
        if current_platform == 'Windows':
            self.process = subprocess.Popen(starter_command_line, env=custom_env,cwd=exec_dir,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            self.process = subprocess.Popen(starter_command_line, env=custom_env,cwd=exec_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            line = self.process.stdout.readline().decode('utf8', 'replace')
            if line:
                self.log_text.insert(tk.END, line)
                self.log_text.see(tk.END)
            if not line and self.process.poll() is not None:
                break

    # --------------------------
    # Print : Print line in GUI
    # --------------------------
    def print(self, line):
        self.log_text.insert(tk.END, line)
        self.log_text.insert(tk.END, "\n")
        self.log_text.see(tk.END)

    # ----------------------------------------------------------------
    # Main entrance from job_holder : Create Output Windows & Run Job
    # ----------------------------------------------------------------
    def run_single_job(self):
        #Initialise variables

        # Set the job environment variables
        custom_env = self.runOpenRadioss.environment()

        self.print("")
        self.print("")
        self.print(" JobName: "+self.jobname)
        self.print(" ----------------------------")
        self.print(" Number of MPI processes : "+self.command[2])
        self.print(" Number of OpenMP threads: "+self.command[1])
        self.print("")

        if self.decktype == 'inp':
        # Decktype is inp : Run inp2rad conversion
        # -----------------------------------------------

            # Temporarily disable buttons while inp2rad is running
            self.stop_button['state'] = 'disable'
            self.kill_button['state'] = 'disable'
            self.anim_button['state'] = 'disable'
            self.h3d_button['state'] = 'disable'
            if vd3penabled:
                    self.d3p_button['state'] = 'disable'

            inp2rad_successful = False  # Flag to track success of conversion

            # Redirect inp2rad stdout and stderr to GUI text widget
            redirect_text = RedirectText(self.log_text)
            with contextlib.redirect_stdout(redirect_text), contextlib.redirect_stderr(redirect_text):
                    # Attempt to execute the conversion
                    success = self.runOpenRadioss.inp2rad_conversion()

                # Check if the process completed successfully
            if success:  # Assuming `success` is a boolean or status code
                    self.command[0] = self.command[0][:-4] + '.rad'
                    inp2rad_successful = True
            else:
                    self.close_button['state'] = 'normal'
                    self.window.protocol('WM_DELETE_WINDOW', self.on_close)
                    self.is_finished = True

            # Only re-enable buttons if the operation was successful
            if inp2rad_successful:
                    self.stop_button['state'] = 'active'
                    self.kill_button['state'] = 'active'
                    self.anim_button['state'] = 'active'
                    self.h3d_button['state'] = 'active'
                    if vd3penabled:
                        self.d3p_button['state'] = 'active'

            # Stop further execution if the inp2rad operation was unsuccessful
            else:
                self.print(" ---------------------------------------------------------")
                self.print(" Stopping execution due to unsuccessful inp2rad conversion")
                self.print(" ---------------------------------------------------------")
                return  # Exit this function early and prevent further execution


        # Starter Deck - execute Starter
        # -------------------------------
        self.run_number = self.run_id
        if self.run_id==0:

            # First Delete previous result in the directory"
            self.runOpenRadioss.delete_previous_results()

            # Set Run Number to 0 (Starter)
            starter_command_line=self.runOpenRadioss.get_starter_command()
            if self.debug==1:print("StarterCommand: ",starter_command_line)
            if self.debug==1:print("ExecDir: ",self.exec_dir)
            # Run Starter Command
            self.job_process(starter_command_line,custom_env,self.exec_dir)
            self.run_number = self.run_number + 1

        # Go to Engine : proceed or not
        starter_only=self.command[6]
        if starter_only=='no' and self.stop_after_starter is False:

            # Execute Engine(s)
            # ------------------

            # Get Engine Input File List
            if self.run_id==0:
                engine_file_list = self.runOpenRadioss.get_engine_input_file_list()
            else:
                engine_file_list=[self.command[0]]
            if self.debug==1:print("Engine_file_list:",engine_file_list)
            self.stop_after_engine = False
            for engine_file in engine_file_list:
                if self.stop_after_engine is True:
                    break
                engine_command_line = self.runOpenRadioss.get_engine_command(engine_file)
                if self.debug==1:print("EngineCommand: ",engine_command_line)
                self.job_process(engine_command_line,custom_env,self.exec_dir)
                self.run_number = self.run_number + 1

            # Execute TH to CSV
            # --------------------
            # Redirect stdout and stderr to GUI text widget
            redirect_text = RedirectText(self.log_text)
            with contextlib.redirect_stdout(redirect_text), contextlib.redirect_stderr(redirect_text):
                # Attempt to execute the conversion
                self.runOpenRadioss.convert_th_to_csv()

            # Execute Anim to VTK
            # --------------------
            redirect_text = RedirectText(self.log_text)
            with contextlib.redirect_stdout(redirect_text), contextlib.redirect_stderr(redirect_text):
                # Attempt to execute the conversion
                self.runOpenRadioss.convert_anim_to_vtk()

            # Execute Anim to D3Plot
            # ----------------------
            # Redirect stdout and stderr to GUI text widget
            redirect_text = RedirectText(self.log_text)
            with contextlib.redirect_stdout(redirect_text), contextlib.redirect_stderr(redirect_text):
                # Attempt to execute the conversion
                self.runOpenRadioss.d3plot_conversion()

            # Execute Anim to VTKHDF
            # --------------------
            redirect_text = RedirectText(self.log_text)
            with contextlib.redirect_stdout(redirect_text), contextlib.redirect_stderr(redirect_text):
                # Attempt to execute the conversion
                self.runOpenRadioss.convert_anim_to_vtkhdf()

        # Job Finished
        # ------------
        self.print(" ")
        self.print(" ")
        self.print(" --------------------")
        self.print(" Job Finished")
        self.print(" --------------------")    
        self.is_finished = True
        self.log_text['state'] = 'disable'
        self.stop_button['state'] = 'disable'
        self.kill_button['state'] = 'disable'
        self.anim_button['state'] = 'disable'
        self.h3d_button['state'] = 'disable'
        if vd3penabled:
            self.d3p_button['state'] = 'disable'
        # Enable 'Close' button and 'X' button after job finishes
        self.close_button['state'] = 'normal'
        self.window.protocol('WM_DELETE_WINDOW', self.on_close)
        stopping_st_file = self.job_dir + '/stopping_st_' + self.job_name
        if os.path.exists(stopping_st_file):
            os.remove(stopping_st_file)

