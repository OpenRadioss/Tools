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
import signal
import subprocess
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

from button_with_highlight import ButtonWithHighlight
try:
    from vortex_radioss.animtod3plot.Anim_to_D3plot import readAndConvert
    vd3penabled = True
except ImportError:
    # If VortexRadioss Module not present disable d3plot options
    vd3penabled = False
    
class JobWindow():

    def __init__(self, command):
        self.command = command
        if platform.system() == 'Windows':
            self.job_dir = os.path.dirname(command[1])
            jnm1 = command[1]
        elif platform.system() == 'Linux':
            self.job_dir = os.path.dirname(command[2])
            jnm1 = command[2]

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
    
    def on_close(self):
        self.window.destroy()
    
    def stop_job(self):
        if os.path.exists(self.job_dir + '/running_st_' + self.job_name):
            # Behavior for 'running_st_' files
            if messagebox.askokcancel('Stop', 'Stop job at end of starter phase?'):
                self.terminate_running_st_process()
        
        elif os.path.exists(self.job_dir + '/stopping_st_' + self.job_name):
            # Behavior for 'stopping_st_' files
            messagebox.showinfo('Already Stopping', 'Job stop already requested, will stop at end of Starter')

        else:
            # Behavior for 'running_en_' files
            if messagebox.askokcancel('Stop', 'Stop Job?'):
                if os.path.exists(self.job_dir + '/running_en_' + self.job_name):
                    # Behavior for 'running_en_' files
                    f = open(self.job_dir + '/running_en_' + self.job_name, mode='r')
                    current_job_name = f.readline()
                    f.close()
                    f = open(self.job_dir + '/' + current_job_name + '.ctl', mode='w')
                    f.write('/STOP')
                    f.close()

    def kill_job(self):
        if os.path.exists(self.job_dir + '/running_st_' + self.job_name):
            # Behavior for 'running_st_' files
            if messagebox.askokcancel('Kill', 'Stop job at end of starter phase?'):
                self.terminate_running_st_process()

        elif os.path.exists(self.job_dir + '/stopping_st_' + self.job_name):
            # Behavior for 'stopping_st_' files
            messagebox.showinfo('Already Stopping', 'Job stop already requested, will stop at end of Starter')

        else:
            # Behavior for 'running_en_' files
            if messagebox.askokcancel('Kill', 'Kill Job?'):
                if os.path.exists(self.job_dir + '/running_en_' + self.job_name):
                    # Behavior for 'running_en_' files
                    f = open(self.job_dir + '/running_en_' + self.job_name, mode='r')
                    current_job_name = f.readline()
                    f.close()
                    f = open(self.job_dir + '/' + current_job_name + '.ctl', mode='w')
                    f.write('/KILL')
                    f.close()

    def anim_job(self):
        if os.path.exists(self.job_dir + '/running_en_' + self.job_name):
            # Behavior for 'running_en_' files
            if messagebox.askokcancel('Anim', 'Write Anim File?'):
                f = open(self.job_dir + '/running_en_' + self.job_name, mode='r')
                current_job_name = f.readline()
                f.close()
                f = open(self.job_dir + '/' + current_job_name + '.ctl', mode='w')
                f.write('/ANIM')
                f.close()
        elif os.path.exists(self.job_dir + '/running_st_' + self.job_name):
            # Behavior for 'running_st_' files
            messagebox.showinfo('Starter Phase', 'Job is still in starter phase.')
        elif os.path.exists(self.job_dir + '/stopping_st_' + self.job_name):
            # Behavior for 'stopping_st_' files
            messagebox.showinfo('Starter Phase', 'Job is still in starter phase.')

    def h3d_job(self):
        if os.path.exists(self.job_dir + '/running_en_' + self.job_name):
            # Behavior for 'running_en_' files
            if messagebox.askokcancel('h3d', 'Write h3d File?'):
                f = open(self.job_dir + '/running_en_' + self.job_name, mode='r')
                current_job_name = f.readline()
                f.close()
                f = open(self.job_dir + '/' + current_job_name + '.ctl', mode='w')
                f.write('/H3D')
                f.close()
        elif os.path.exists(self.job_dir + '/running_st_' + self.job_name):
            # Behavior for 'running_st_' files
            messagebox.showinfo('Starter Phase', 'Job is still in starter phase.')
        elif os.path.exists(self.job_dir + '/stopping_st_' + self.job_name):
            # Behavior for 'stopping_st_' files
            messagebox.showinfo('Starter Phase', 'Job is still in starter phase.')

    def d3p_job(self):
        if os.path.exists(self.job_dir + '/running_en_' + self.job_name):
            # Behavior for 'running_en_' files
            # Define the pattern for anim files, e.g., JobNameA000, JobNameA001, etc.
            anim_pattern = re.compile(self.job_name + r"A[0-9]{3,}(?:[0-9])?$")
            
            # List anim files matching the pattern in the job directory
            anim_files = [file for file in os.listdir(self.job_dir) if anim_pattern.match(file)]
            
            if anim_files:
                # If anim files exist, ask the user if they want to convert them
                if messagebox.askokcancel('d3plot', 'Create d3plots of existing anim files?'):
                    if platform.system() == 'Windows':
                        file_stem = self.job_dir + '\\' + self.job_name
                        
                    if platform.system() == 'Linux':
                        file_stem = self.job_dir + '/' + self.job_name
                    # Use the file stem to call readAndConvert	
                    readAndConvert(file_stem,silent=True)

            else:
                # Show an info message if no anim files are found
                messagebox.showinfo('No anim files exist', 'd3plot conversion requires anim files in the run directory.')
    
        elif os.path.exists(self.job_dir + '/running_st_' + self.job_name):
            # Behavior for 'running_st_' files
            messagebox.showinfo('Starter Phase', 'Job is still in starter phase.')
        elif os.path.exists(self.job_dir + '/stopping_st_' + self.job_name):
            # Behavior for 'stopping_st_' files
            messagebox.showinfo('Starter Phase', 'Job is still in starter phase.')
                
    def terminate_running_st_process(self):
        if not self.is_finished and self.process and self.process.poll() is None:
            self.process.terminate()
            running_st_file = self.job_dir + '/running_st_' + self.job_name
            if os.path.exists(running_st_file):
               os.remove(running_st_file)
               f = open(self.job_dir + '/stopping_st_' + self.job_name, mode='w')
               f.close()

    def run_single_job(self):
        if platform.system() == 'Windows':
            self.process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while True:
                line = self.process.stdout.readline().decode('utf8', 'replace')
                if line:
                    self.log_text.insert(tk.END, line)
                    self.log_text.see(tk.END)
                if not line and self.process.poll() is not None:
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
                    break
        elif platform.system() == 'Linux':
            self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
            with self.process.stdout:
                for line in iter(self.process.stdout.readline, ''):
                    self.log_text.insert(tk.END, line)
                    self.log_text.see(tk.END)
                    self.log_text.update_idletasks()
            self.process.wait()
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

            self.close_button['state'] = 'normal'
            stopping_st_file = self.job_dir + '/stopping_st_' + self.job_name
            if os.path.exists(stopping_st_file):
               os.remove(stopping_st_file)
