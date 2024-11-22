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
import re
import platform
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

current_platform = platform.system()
    
class JobWindow():

    def __init__(self, command,debug):
        #DEbug flag activated in OpenRadioss_gui.py
        self.debug=debug
        self.command = command
        self.job_dir = os.path.dirname(command[0])
        self.stop_after_starter=False
        jnm1 = command[0]
        
        # Create an instance of RunOpenRadioss
        self.runOpenRadioss = RunOpenRadioss(self.command,self.debug)
        self.jobname,self.run_id,self.exec_dir=self.runOpenRadioss.get_jobname_runid_rundirectory()
        # Gather the jobname, run_id, job directory from the command


        if jnm1.endswith('.rad'):
            self.job_name = os.path.basename(jnm1)[0:-9]
        elif jnm1.endswith('.k'):
            self.job_name = os.path.basename(jnm1)[0:-2]
        elif jnm1.endswith('.key'):
            self.job_name = os.path.basename(jnm1)[0:-4]
        elif jnm1.endswith('.inp'):
            self.job_name = os.path.basename(jnm1)[0:-4]
 
        self.is_finished = False
        
        self.window = tk.Toplevel()
        self.window.title(self.job_name)
        # Initially disable 'X' button while job is running
        self.window.protocol('WM_DELETE_WINDOW', (lambda: 'pass'))
        if platform.system() == 'Windows':
            # Windows specific code
            self.window.iconbitmap('./icon/ross.ico')
        elif platform.system() == 'Linux':
            # Linux specific code
            icon_image = tk.PhotoImage(file='./icon/ross.png')
            self.window.iconphoto(True, icon_image)
        self.log_text = scrolledtext.ScrolledText(self.window, width=100, height=40)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
      
        self.frame_control = tk.Frame(self.window, padx=10, pady=5)
        self.frame_control.pack(side=tk.TOP, pady=10)

        self.process = None
        
        # Control buttons
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

        # Disable the 'Close' button while job is running
        self.close_button = ButtonWithHighlight(self.frame_control, text='Close', state='disable', command=self.on_close, padx=30)
        self.close_button.pack(side=tk.LEFT, padx=5)

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
        if (self.run_number == 0):
           # Starter Phase - Stop after Starter
           if self.stop_after_starter == True:
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
        if (self.run_number == 0):
           # Starter Phase - Stop after Starter
           if self.stop_after_starter == True:
               messagebox.showinfo('Already Stopping', 'Job stop already requested, will stop at end of Starter')
           else:
               if messagebox.askokcancel('Kill', 'Stop job at end of starter phase?'):
                   self.stop_after_starter == True
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
        if (self.run_number == 0):
            messagebox.showinfo('Starter Phase', 'Job is still in starter phase.\nCannot write Animation file')
        else:
                f = open(self.job_dir + '/' + self.job_name+"_"+str( self.run_number).zfill(4)+ '.ctl', mode='w')
                f.write('/ANIM')
                f.close()

    # ------------------------------------------------
    # H3D button : Write H3D File
    # ------------------------------------------------
    def h3d_job(self):
        if (self.run_number == 0):
            messagebox.showinfo('Starter Phase', 'Job is still in starter phase.\nCannot write H3D State')
        else:
                f = open(self.job_dir + '/' + self.job_name+"_"+str( self.run_number).zfill(4)+ '.ctl', mode='w')
                f.write('/H3D')
                f.close()

    # -----------------------------------------------------
    # D3Plot button : Convert Current Anim Files to d3plot
    # -----------------------------------------------------
    def d3p_job(self):
        if vd3penabled == False:
            messagebox.showinfo('D3Plot Not available', 'D3Plot Converter is not available')
        else:
            if (self.run_number == 0):
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
        if  starter_only=='no' and self.stop_after_starter == False:
          
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
               if self.stop_after_engine == True:
                    break
               engine_command_line = self.runOpenRadioss.get_engine_command(engine_file)
               if self.debug==1:print("EngineCommand: ",engine_command_line)
               self.job_process(engine_command_line,custom_env,self.exec_dir)
               self.run_number = self.run_number + 1

          
          anim_to_vtk=self.command[4]
          if anim_to_vtk=='yes':
            # Execute Anim to VTK
            # --------------------
            animation_file_list = self.runOpenRadioss.get_animation_list()
            if self.debug==1:print("Animation_file_list:",animation_file_list)
            if len(animation_file_list)>0:
                self.print("") 
                self.print("")  
                self.print(" ------------------------------------------------------")
                self.print(" Anim-vtk option selected, Converting Anim Files to vtk")
                self.print(" ------------------------------------------------------")
                self.print("")

                for anim_file in animation_file_list:
                    self.print(" Anim File Being Converted is "+anim_file)
                    self.runOpenRadioss.convert_anim_to_vtk(anim_file)

                self.print("")  
                self.print(" ------------------------------------")
                self.print(" Anim file conversion to vtk complete")
                self.print(" ------------------------------------")
            else:
                self.print("") 
                self.print("")  
                self.print(" ----------------------------------------------------------------")
                self.print(" NB: Anim-vtk option selected, but no Anim files found to convert")
                self.print(" ----------------------------------------------------------------")

          th_to_csh=self.command[5]
          if th_to_csh=='yes':
            # Execute Anim to VTK
            # --------------------
            th_list=self.runOpenRadioss.get_th_list()
            if self.debug==1:print("TH List: ",th_list)
            if len(th_list)>0:
                self.print("") 
                self.print("")  
                self.print(" ------------------------------------------------------")
                self.print(" TH-csv option selected, Converting TH Files to csv")
                self.print(" ------------------------------------------------------")
                self.print("")
    
                for th_file in th_list:
                  self.print(" Time History File Being Converted is "+th_file)
                  self.runOpenRadioss.convert_th_to_csv(th_file)
                self.print("")  
                self.print(" ------------------------------------")
                self.print(" TH file conversion to csv complete")
                self.print(" ------------------------------------")
            else:
                self.print("") 
                self.print("")  
                self.print(" -------------------------------------------------------------")
                self.print(" NB: TH-csv option selected, but no TH files found to convert")
                self.print(" -------------------------------------------------------------")

          anim_to_d3plot=self.command[7]
          if anim_to_d3plot=='yes':
            # Execute Anim to D3Plot
            # ----------------------
            animation_file_list = self.runOpenRadioss.get_animation_list()
            if len(animation_file_list)>0:
                self.print("") 
                self.print("")  
                self.print(" -------------------------------------------------------------")
                self.print(" Anim-d3plot option selected, Converting Anim Files to d3plot")
                self.print(" -------------------------------------------------------------")
                self.print("")
                file_stem = os.path.join(self.exec_dir, self.jobname)
                try:
                       readAndConvert(file_stem,silent=True)
                except Exception as e:
                       messagebox.showinfo('Error', 'Error in d3plot conversion: ' + str(e))


                self.print("")  
                self.print(" ----------------------------------------")
                self.print(" Anim file conversion to d3plot complete")
                self.print(" ----------------------------------------")
            else:
                self.print("") 
                self.print("")  
                self.print(" --------------------------------------------------------------------")
                self.print(" NB: Anim-d3plot option selected, but no Anim files found to convert")
                self.print(" --------------------------------------------------------------------")

        # Job Finished
        # ------------
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

