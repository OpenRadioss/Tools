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

from collections import deque
from enum import Enum
import os
import platform
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from button_with_highlight import ButtonWithHighlight
from job_window import JobWindow

class State(Enum):
  
    WAITING = 0
    RUNNING = 1

class JobHolder():
  
    def __init__(self,debug):
        self.state = State.WAITING
        self.deque = deque()
        self.is_showing_queue = False
        self.debug = debug
    
    def submit_next_job(self):
        if not self.deque:
            messagebox.showinfo('Next Job', 'Queue is empty.')
            return
# Get the next job from the queue
        command = self.deque.popleft()
# Open a new instance of JobWindow with the next job
        job_window_instance = JobWindow(command,self.debug)
# Show the updated queue if it's open
        if self.is_showing_queue:
            self.print_queue()

    def submit_last_job(self):
        if not self.deque:
            messagebox.showinfo('Last Job', 'Queue is empty.')
            return
# Get the next job from the queue
        command = self.deque.pop()
# Open a new instance of JobWindow with the next job
        job_window_instance = JobWindow(command)
# Show the updated queue if it's open
        if self.is_showing_queue:
            self.print_queue()
    
    def push_job(self, command):
        self.deque.append(command)
        if self.is_showing_queue: self.print_queue()
    
    def is_empty(self):
        if self.state == State.RUNNING: return False
        if self.deque: return False
        return True
    
    def update_state(self):
        if self.state == State.RUNNING and self.running_job.is_finished:
            self.state = State.WAITING
        
    def run_job(self):
        self.update_state()
        if self.state == State.RUNNING: return
        if not self.deque: return
        self.state = State.RUNNING
        self.running_job = JobWindow(self.deque.popleft(),self.debug)
        if self.is_showing_queue: self.print_queue()

    def clear_queue(self):
        if not self.deque:
            messagebox.showinfo('Clear Queue', 'Queue is empty.')
            return
        if messagebox.askokcancel('Clear Queue', 'Clear Queue?'):
            while self.deque: self.deque.pop()
            if self.is_showing_queue: self.print_queue()
    
    def print_queue(self):
        self.queue_list.delete(*self.queue_list.get_children())
        for command in self.deque:
            dir = os.path.dirname(command[0])
            job = os.path.basename(command[0])
            nt = command[1]
            np = command[2]
            sp = command[3]
            vtk = command[4]
            csv = command[5]
            d3plot = command[7]
            self.queue_list.insert(parent='', index='end', values=(dir, job, nt, np, sp, vtk, d3plot, csv))
    
    def cancel_next_job(self):
        if self.deque:
            self.deque.popleft()
            self.print_queue()
    
    def cancel_last_job(self):
        if self.deque:
            self.deque.pop()
            self.print_queue()
    
    def show_queue(self):
        if self.is_showing_queue:
            self.queue_window.lift()
            return
        
        self.is_showing_queue = True
        self.queue_window = tk.Toplevel()
        self.queue_window.title('Job Queue')
        self.queue_window.resizable(True, True)      
        if platform.system() == 'Windows':
            # Windows specific code
            self.queue_window.iconbitmap('./icon/ross.ico')
        elif platform.system() == 'Linux':
            # Linux specific code
            icon_image = tk.PhotoImage(file='./icon/ross.png')
            self.queue_window.iconphoto(True, icon_image)
        self.queue_window.protocol('WM_DELETE_WINDOW', self.close_queue)
        self.queue_window.grid_rowconfigure(0, weight=1)
        self.queue_window.grid_columnconfigure(0, weight=1)
        self.queue_list = ttk.Treeview(self.queue_window, columns=('directory', 'job name', '-nt', '-np', 'sp', 'vtk', 'd3plot', 'csv'))
        self.queue_list.column('#0', width=0, stretch=False)
        self.queue_list.column('directory', anchor='w', width=600, stretch=True)
        self.queue_list.column('job name', anchor='w', width=300, stretch=True)
        self.queue_list.column('-nt', anchor='center', width=50, stretch=False)
        self.queue_list.column('-np', anchor='center', width=50, stretch=False)
        self.queue_list.column('sp', anchor='center', width=50, stretch=False)
        self.queue_list.column('vtk', anchor='center', width=50, stretch=False)
        self.queue_list.column('d3plot', anchor='center', width=50, stretch=False)
        self.queue_list.column('csv', anchor='center', width=50, stretch=False)
        self.queue_list.heading('directory', text='directory', anchor='w')
        self.queue_list.heading('job name', text='job name', anchor='w')
        self.queue_list.heading('-nt', text='-nt', anchor='center')
        self.queue_list.heading('-np', text='-np', anchor='center')
        self.queue_list.heading('sp', text='sp/dp', anchor='center')
        self.queue_list.heading('vtk', text='vtk', anchor='center')
        self.queue_list.heading('d3plot', text='d3plot', anchor='center')
        self.queue_list.heading('csv', text='csv', anchor='center')
        self.queue_list.grid(row=0, column=0, sticky='nsew', padx=(10, 10), pady=(10, 10))  # Add padding and stretch

        self.frame_control = tk.Frame(self.queue_window, padx=10, pady=10)
        self.frame_control.grid(row=1, column=0, sticky='ew')  # Ensure it sticks to horizontal edges when resizing
    
        self.queue_window.grid_rowconfigure(1, weight=0)  # Make sure control frame doesn't expand
        self.queue_window.grid_columnconfigure(0, weight=1)
        
        self.cancel_next_button = ButtonWithHighlight(self.frame_control, text='Cancel Next Job', command=self.cancel_next_job, padx=50)
        self.cancel_next_button.pack(side=tk.LEFT, padx=10)
        self.cancel_last_button = ButtonWithHighlight(self.frame_control, text='Cancel Last Job', command=self.cancel_last_job, padx=50)
        self.cancel_last_button.pack(side=tk.LEFT, padx=10)
# Add a new button to manually submit the next job from the queue
        self.submit_next_button = ButtonWithHighlight(self.frame_control, text='Start Next Job', command=self.submit_next_job, padx=50)
        self.submit_next_button.pack(side=tk.LEFT, padx=10)
# Add a new button to manually submit the last job from the queue
        self.submit_last_button = ButtonWithHighlight(self.frame_control, text='Start Last Job', command=self.submit_last_job, padx=50)
        self.submit_last_button.pack(side=tk.LEFT, padx=10)
        self.close_button = ButtonWithHighlight(self.frame_control, text='Close', command=self.close_queue, padx=50)
        self.close_button.pack(side=tk.LEFT, padx=10)
        
        self.print_queue()
        
    def close_queue(self):
        self.is_showing_queue = False
        self.queue_window.destroy()
