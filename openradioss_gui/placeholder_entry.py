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

class PlaceholderEntry(tk.Entry):

    def __init__(
        self,
        parent=None,
        placeholder_text="Enter text...",
        placeholder_color='gray',
        entry_width=20,
    ):
        super().__init__(parent, width=entry_width)
        self.placeholder_text = placeholder_text
        self.placeholder_color = placeholder_color
        self.default_text_color = self['fg']

        self.bind("<FocusIn>", self.on_focus_gain)
        self.bind("<FocusOut>", self.on_focus_loss)
        self.display_placeholder()

    def display_placeholder(self):
        self.insert(0, self.placeholder_text)
        self['fg'] = self.placeholder_color

    def on_focus_gain(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete(0, tk.END)
            self['fg'] = self.default_text_color

    def on_focus_loss(self, *args):
        if not self.get():
            self.display_placeholder()

    def is_placeholder_active(self):
        return not self.get() or self.get() == self.placeholder_text

    def get_user_input(self, default_value=''):
        current_text = self.get()
        return default_value if current_text == self.placeholder_text else current_text

