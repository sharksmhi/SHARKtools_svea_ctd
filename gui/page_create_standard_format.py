#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2018 SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from sharkpylib.tklib import tkinter_widgets as tkw

import ctdpy

from pathlib import Path


class PageCreateStandardFormat(tk.Frame):

    def __init__(self, parent, parent_app, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        # parent is the frame "container" in App. contoller is the App class
        self.parent = parent
        self.parent_app = parent_app
        self.logger = self.parent_app.logger
        self.user_manager = parent_app.user_manager
        self.user = self.user_manager.user

    def _build(self):
        padding = dict(padx=15,
                       pady=15)
        frame_create_metadata_file = ttk.LabelFrame(self, text='Create metadata file')
        frame_create_metadata_file.grid(row=0, column=0, sticky='nsew', **padding)

        tkw.grid_configure(self, nr_columns=2, nr_rows=1)

        self._build_frame_create_metadata_file(frame_create_metadata_file)

    def _build_frame_create_metadata_file(self, frame):
        padding = dict(padx=10,
                       pady=5)

        metadata_left_frame = tk.Frame(frame)
        metadata_left_frame.grid(row=0, column=0, sticky='nsew', **padding)

        metadata_right_frame = tk.Frame(frame)
        metadata_right_frame.grid(row=0, column=1, sticky='nsew', **padding)

        self._build_load_cnv_frame(metadata_left_frame)
        self._build_frame_manual_metadata(metadata_right_frame)

    def _build_load_cnv_frame(self, frame):
        padding = dict(padx=10,
                       pady=5,
                       sticky='w')
        self.button_load_cnv_files = ttk.Button(frame,
                                                text='Load cnv files',
                                                command=self._callback_button_load_cnv_files)
        self.button_load_cnv_files.grid(row=0, column=0, **padding)

        self.strvar_cnv_directory = tk.StringVar()
        str_frame = tk.Frame(frame)
        str_frame.grid(row=1, column=0, sticky='sw', padx=padding.get('padx'))
        tk.Label(str_frame, text='Directory:').grid(row=0, column=0, sticky='w')
        tk.Label(str_frame, textvariable=self.strvar_cnv_directory).grid(row=0, column=1, sticky='w')

        self.cnv_files_selection_widget = tkw.ListboxSelectionWidget(frame,
                                                                     prop_items={'width': 50},
                                                                     prop_selected={'width': 50}, row=2, column=0, **padding)

    def _build_frame_manual_metadata(self, frame):
        padding = dict(padx=10,
                       pady=5,
                       sticky='w')
        entry_list = []
        r = 0
        for r, item in enumerate(self.manual_metadata_items):
            strvar = tk.StringVar()
            ttk.Label(frame, text=item).grid(row=r, column=0, **padding)
            ent = ttk.Entry(frame, textvariable=strvar)
            ent.grid(row=r, column=1, **padding)
            entry_list.append(ent)
            self.manual_metadata_stringvars[item] = strvar

        # tkw.grid_configure(frame, nr_columns=2, nr_rows=r+1)

        # Link entries
        for f, t in zip(entry_list[:-1], entry_list[1:]):
            f.bind('<Return>', lambda event, x=t: x.focus())
            f.bind('<Down>', lambda event, x=t: x.focus())
            t.bind('<Up>', lambda event, x=f: x.focus())

    def _callback_button_load_cnv_files(self, *args, **kwargs):
        file_objects = filedialog.askopenfiles(title='Select files',
                                               initialdir=str(Path(self.user.directory.setdefault('cnv_files',
                                                                                         r'\\winfs-proj\proj\havgem\EXPRAPP\Exprap2020'))),
                                               filetypes=[('cnv-files', '.cnv')])
        if not file_objects:
            return

        self.cnv_files_paths = {}
        directory = ''
        items = []
        for item in file_objects:
            file_path = Path(item.name)
            file_name = file_path.name
            directory = file_path.parent
            items.append(file_name)
            self.cnv_files_paths[file_name] = file_path

        self.user.directory.set('cnv_files', str(directory))

        self.strvar_cnv_directory.set(directory)
        self.cnv_files_selection_widget.update_items(items)
        self.cnv_files_selection_widget.move_items_to_selected(items)

    def startup(self):
        self.manual_metadata_items = ['WINDIR', 'WINSP', 'AIRTEMP', 'AIRPRES', 'WEATH', 'CLOUD', 'WAVES', 'ICEOB']
        self.manual_metadata_entry_linking = {}
        self.manual_metadata_stringvars = {}
        self.cnv_files_paths = {}

        self._build()
        self.update_page()

    def update_page(self):
        self.user = self.user_manager.user


if __name__ == '__main__':
    file_paths = filedialog.askopenfiles(title='Select files',
                                         initialdir=r'\\winfs-proj\proj\havgem\EXPRAPP\Exprap2020',
                                         filetypes=[('cnv-files', '.cnv')])