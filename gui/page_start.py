#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2018 SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import tkinter as tk
from tkinter import ttk
from sharkpylib.tklib import tkinter_widgets as tkw


class PageStart(tk.Frame):

    def __init__(self, parent, parent_app, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        # parent is the frame "container" in App. contoller is the App class
        self.parent = parent
        self.parent_app = parent_app

    def startup(self):
        """

        :return:
        """
        padding = dict(padx=50, pady=50, sticky='nsew')

        button_basic = ttk.Button(self, text='Basic', command=lambda: self.parent_app.show_frame('PageBasic'))
        button_basic.grid(row=0, column=0, **padding)

        button_advanced = ttk.Button(self, text='Advanced', command=lambda: self.parent_app.show_frame('PageAdvanced'))
        button_advanced.grid(row=0, column=1, **padding)

        tkw.grid_configure(self, nr_columns=2)

        self.update_page()


    #===========================================================================
    def update_page(self):
        pass