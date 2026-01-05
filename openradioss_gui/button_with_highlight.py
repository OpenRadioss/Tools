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
import tkinter as tk

class ButtonWithHighlight(tk.Button):
    def __init__(
        self,
        master=None,
        text=None,
        image=None,
        command=None,
        hovercolor='#ADD8E6',  # Light blue color modified to hex to allow interoperability with linux
        state='normal',
        width=7,
        padx=10
    ):
        super().__init__(
            master,
            text=text,
            image=image,
            command=command,
            state=state,
            width=width,
            padx=padx
        )
        self.bc = self['bg']  # Store the initial background color
        self.hc = hovercolor
        self.bind("<Enter>", self.enter_bg)
        self.bind("<Leave>", self.leave_bg)

    def enter_bg(self, *args):
        if self['state'] == 'normal':
            self['bg'] = self.hc

    def leave_bg(self, *args):
        self['bg'] = self.bc
