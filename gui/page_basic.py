#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2018 SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
import datetime
import os
import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog, messagebox
from svea import SveaController

from sharkpylib.tklib import tkinter_widgets as tkw

DEBUG = True


class PageBasic(tk.Frame):

    def __init__(self, parent, parent_app, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        # parent is the frame "container" in App. contoller is the App class
        self.parent = parent
        self.parent_app = parent_app
        self.main_app = self.parent_app.main_app
        self.logger = self.parent_app.logger
        self.user_manager = parent_app.user_manager
        self.user = self.user_manager.user
        
        self.lockable_buttons = []
        self.buttons = {}
        self.stringvars = {}
        self.set_svea_paths = {}

    def startup(self):
        """

        :return:
        """
        self.svea_controller = SveaController(logger=self.logger)

        self.set_svea_paths['working_dir'] = self.svea_controller.set_path_working_directory
        self.set_svea_paths['raw_files_dir'] = self.svea_controller.set_path_raw_files
        self.set_svea_paths['cnv_files_dir'] = self.svea_controller.set_path_cnv_files
        self.set_svea_paths['standard_files_dir'] = self.svea_controller.set_path_standard_format_files

        self._build()

    def _build(self):
        padding = dict(padx=15,
                       pady=15)

        frame_paths = ttk.LabelFrame(self, text='Sökvägar')
        frame_paths.grid(row=0, column=1, sticky='nsew', columnspan=5, **padding)

        frame_options = ttk.LabelFrame(self, text='Alternativ')
        frame_options.grid(row=0, column=0, sticky='nsew', **padding)

        frame_seb_processing = ttk.LabelFrame(self, text='1) SEB processering')
        frame_seb_processing.grid(row=1, column=0, sticky='nsew', **padding)

        frame_create_metadata_file = ttk.LabelFrame(self, text='2) Skapa leveransmall')
        frame_create_metadata_file.grid(row=1, column=1, sticky='nsew', **padding)

        frame_create_standard_format = ttk.LabelFrame(self, text='3) Skapa standardformat')
        frame_create_standard_format.grid(row=1, column=2, sticky='nsew', **padding)

        frame_automatic_qc = ttk.LabelFrame(self, text='4) Automatisk QC')
        frame_automatic_qc.grid(row=1, column=3, sticky='nsew', **padding)

        frame_manual_qc = ttk.LabelFrame(self, text='5) Visuell granskning')
        frame_manual_qc.grid(row=1, column=4, sticky='nsew', **padding)

        frame_other = ttk.LabelFrame(self, text='6) Övrigt')
        frame_other.grid(row=1, column=5, sticky='nsew', **padding)

        tkw.grid_configure(self, nr_columns=6, nr_rows=2)

        self._build_frame_paths(frame_paths)
        self._build_frame_options(frame_options)
        self._build_frame_seb_processing(frame_seb_processing)
        self._build_frame_create_meatadata_file(frame_create_metadata_file)
        self._build_frame_create_standard_format(frame_create_standard_format)
        self._build_frame_auto_qc(frame_automatic_qc)
        self._build_frame_man_qc(frame_manual_qc)
        self._build_frame_other(frame_other)

    def _build_frame_paths(self, frame):
        padding = dict(padx=10,
                       pady=5,
                       sticky='w')

        padd = dict(padx=10,
                       pady=5,
                       sticky='nsew')

        self.buttons['set_working_dir'] = tk.Button(frame, text='Arbetsmapp', command=self._set_working_directory)
        self.buttons['set_working_dir'].grid(row=0, column=0, **padd)
        self.stringvars['working_dir'] = tk.StringVar()
        tk.Label(frame, textvariable=self.stringvars['working_dir']).grid(row=0, column=1, **padding)
        self.stringvars['working_dir_info'] = tk.StringVar()
        tk.Label(frame, textvariable=self.stringvars['working_dir_info']).grid(row=0, column=2, **padding)

        self.buttons['set_raw_dir'] = tk.Button(frame, text='Råfiler (Seabird)', command=self._set_raw_files_directory)
        self.buttons['set_raw_dir'].grid(row=1, column=0, **padd)
        self.stringvars['raw_files_dir'] = tk.StringVar()
        tk.Label(frame, textvariable=self.stringvars['raw_files_dir']).grid(row=1, column=1, **padding)
        self.stringvars['raw_files_dir_info'] = tk.StringVar()
        tk.Label(frame, textvariable=self.stringvars['raw_files_dir_info']).grid(row=1, column=2, **padding)

        self.buttons['set_cnv_dir'] = tk.Button(frame, text='CNV filer', command=self._set_cnv_files_directory) 
        self.buttons['set_cnv_dir'].grid(row=2, column=0, **padd)
        self.stringvars['cnv_files_dir'] = tk.StringVar()
        tk.Label(frame, textvariable=self.stringvars['cnv_files_dir']).grid(row=2, column=1, **padding)
        self.stringvars['cnv_files_dir_info'] = tk.StringVar()
        tk.Label(frame, textvariable=self.stringvars['cnv_files_dir_info']).grid(row=2, column=2, **padding)

        self.buttons['set_standard_dir'] = tk.Button(frame, text='Standardformat', command=self._set_standard_files_directory)
        self.buttons['set_standard_dir'].grid(row=3, column=0, **padd)
        self.stringvars['standard_files_dir'] = tk.StringVar()
        tk.Label(frame, textvariable=self.stringvars['standard_files_dir']).grid(row=3, column=1, **padding)
        self.stringvars['standard_files_dir_info'] = tk.StringVar()
        tk.Label(frame, textvariable=self.stringvars['standard_files_dir_info']).grid(row=3, column=2, **padding)

        self.buttons['set_qc_dir'] = tk.Button(frame, text='QC filer',
                                                    command=self._set_qc_files_directory)
        self.buttons['set_qc_dir'].grid(row=4, column=0, **padd)
        self.stringvars['qc_dir'] = tk.StringVar()
        tk.Label(frame, textvariable=self.stringvars['qc_dir']).grid(row=4, column=1, **padding)
        self.stringvars['qc_dir_info'] = tk.StringVar()
        tk.Label(frame, textvariable=self.stringvars['qc_dir_info']).grid(row=4, column=2, **padding)

        # self.lockable_buttons.append(self.buttons['set_working_dir'])
        self.lockable_buttons.append(self.buttons['set_raw_dir'])
        self.lockable_buttons.append(self.buttons['set_cnv_dir'])
        self.lockable_buttons.append(self.buttons['set_standard_dir'])
        self.lockable_buttons.append(self.buttons['set_qc_dir'])

    def _build_frame_options(self, frame):
        padding = dict(padx=10,
                       pady=5,
                       sticky='w')

        self.booleanvar_unlock_selections = tk.BooleanVar()
        tk.Checkbutton(frame, text='Lås upp val', variable=self.booleanvar_unlock_selections,
                       command=self._toggle_unlock_selections).grid(row=0, column=0, **padding)

        self.booleanvar_allow_overwrite = tk.BooleanVar()
        tk.Checkbutton(frame, text='Skriv över filer', variable=self.booleanvar_allow_overwrite,
                       command=self._toggle_overwrite).grid(row=1, column=0, **padding)

    def _build_frame_seb_processing(self, frame):
        padding = dict(padx=10,
                       pady=5,
                       sticky='w')
        self.button_run_processing = tk.Button(frame, text='Kör processering', command=self._callback_run_seb_processing)
        self.button_run_processing.grid(row=0, column=0, **padding)
        self.lockable_buttons.append(self.button_run_processing)

    def _build_frame_create_meatadata_file(self, frame):
        padding = dict(padx=10,
                       pady=5,
                       sticky='w')
        self.button_create_metadata = tk.Button(frame, text='Skapa leveransmall', command=self._callback_create_metadata_file)
        self.button_create_metadata.grid(row=0, column=0, **padding)
        self.lockable_buttons.append(self.button_create_metadata)

    def _build_frame_create_standard_format(self, frame):
        padding = dict(padx=10,
                       pady=5,
                       sticky='w')
        self.button_create_standard_files = tk.Button(frame, text='Skapa standardformat', command=self._callback_create_standard_format)
        self.button_create_standard_files.grid(row=0, column=0, **padding)
        self.lockable_buttons.append(self.button_create_standard_files)

    def _build_frame_auto_qc(self, frame):
        padding = dict(padx=10,
                       pady=5,
                       sticky='w')
        self.button_run_automatic_qc = tk.Button(frame, text='Utför automatisk QC', command=self._callback_run_automatic_qc)
        self.button_run_automatic_qc.grid(row=0, column=0, **padding)
        self.lockable_buttons.append(self.button_run_automatic_qc)

    def _build_frame_man_qc(self, frame):
        padding = dict(padx=10,
                       pady=5,
                       sticky='w')

        self.combobox_vis = tkw.ComboboxWidget(frame, title='vis', items=['deep_vis', 'smhi_vis'])

        self.button_run_bokeh_server = tk.Button(frame, text='Visualisera i webbrowser (QC)',
                                                 command=self._callback_run_bokeh_server)
        self.button_run_bokeh_server.grid(row=1, column=0, **padding)
        self.lockable_buttons.append(self.button_run_bokeh_server)

    def _build_frame_other(self, frame):
        padding = dict(padx=10,
                       pady=5,
                       sticky='w')

    def _set_working_directory(self, directory=None):
        old_dir = self.stringvars['working_dir'].get()
        if directory is None:
            directory = filedialog.askdirectory(initialdir=self.stringvars['working_dir'].get())
        if not directory:
            return
        if old_dir == directory:
            return

        if self._is_locked():
            directory = get_sub_directory(directory)

        self.stringvars['working_dir'].set(directory)
        self.svea_controller.working_directory = directory
        self.stringvars['working_dir_info'].set(get_directory_info(directory))
        self._save_user_settings()
        self._update_svea_paths('working_dir')

        if self._is_locked():
            if not self._raw_files_are_present():
                self._highlight_button(self.buttons['set_raw_dir'])
            else:
                self._highlight_button(self.button_run_processing)

    def _set_raw_files_directory(self, directory=None):
        d = directory
        if directory is None:
            directory = filedialog.askdirectory(initialdir=self.stringvars['raw_files_dir'].get())
        if not directory:
            return
        self.stringvars['raw_files_dir'].set(directory)
        self.stringvars['raw_files_dir_info'].set(get_directory_info(directory))

        self._update_svea_paths('raw_files_dir')

        if not d:
            self._save_user_settings()

        if self._is_locked():
            if not self._raw_files_are_present():
                self._highlight_button(self.buttons['set_raw_dir'])
            else:
                self._highlight_button(self.button_run_processing)

    def _set_cnv_files_directory(self, directory=None):
        d = directory
        if directory is None:
            directory = filedialog.askdirectory(initialdir=self.stringvars['cnv_files_dir'].get())
        if not directory:
            return
        self.stringvars['cnv_files_dir'].set(directory)
        self.stringvars['cnv_files_dir_info'].set(get_directory_info(directory))
        self._update_svea_paths('cnv_files_dir')

        if not d:
            self._save_user_settings()

    def _set_standard_files_directory(self, directory=None):
        if directory is None:
            directory = filedialog.askdirectory(initialdir=self.stringvars['standard_files_dir'].get())
        if not directory:
            return
        self.stringvars['standard_files_dir'].set(directory)
        self.stringvars['standard_files_dir_info'].set(get_directory_info(directory))
        self._save_user_settings()
        self._update_svea_paths('standard_files_dir')

    def _set_qc_files_directory(self, directory=None):
        if directory is None:
            directory = filedialog.askdirectory(initialdir=self.stringvars['standard_f_dir'].get())
        if not directory:
            return
        self.stringvars['qc_dir'].set(directory)
        self.stringvars['qc_dir_info'].set(get_directory_info(directory))
        self._save_user_settings()
        self._update_svea_paths('qc_dir')

    def _update_svea_paths(self, _id=None):
        def none_if_empty(item):
            if item == '':
                item = None
            return item
        if _id:
            self.set_svea_paths[_id](none_if_empty(self.stringvars[_id].get()))
        else:
            for key in self.set_svea_paths.keys():
                path = none_if_empty(self.stringvars[key].get())
                # If raw files check if path exists
                if path and not Path(path).is_dir():
                    path = None
                    self.stringvars[key].set('')
                self.set_svea_paths[key](none_if_empty(path))

    def _update_directory_content(self):
        self.stringvars['working_dir_info'].set(get_directory_info(self.stringvars['working_dir'].get()))
        self.stringvars['raw_files_dir_info'].set(get_directory_info(self.stringvars['raw_files_dir'].get()))
        self.stringvars['cnv_files_dir_info'].set(get_directory_info(self.stringvars['cnv_files_dir'].get()))
        self.stringvars['standard_files_dir_info'].set(get_directory_info(self.stringvars['standard_files_dir'].get()))
        self.stringvars['qc_dir_info'].set(get_directory_info(self.stringvars['qc_dir'].get()))

    def _toggle_overwrite(self, *args, **kwargs):
        overwrite = self.booleanvar_allow_overwrite.get()
        self.svea_controller.set_overwrite_permission(overwrite)
        self._save_user_settings()

    def _toggle_unlock_selections(self, *args, **kwargs):
        unlock = self.booleanvar_unlock_selections.get()
        self._save_user_settings()
        if unlock:
            self._unlock()
        else:
            self._lock()

    def _is_locked(self):
        return not self.booleanvar_unlock_selections.get()

    def _lock(self):
        self._reset_paths_on_lock_selection()  # Also resets in svea_controller
        if not self.stringvars['working_dir'].get():
            self._highlight_button(self.buttons['set_working_dir'])
        elif not self._raw_files_are_present():
            self._highlight_button(self.buttons['set_raw_dir'])
        else:
            self._highlight_button(self.button_run_processing)
        self._update_directory_content()

    def _unlock(self):
        self._load_user_setting()
        self._unlock_buttons()
        self._reset_button_color()
        self._update_directory_content()

    def _lock_buttons(self):
        self._reset_button_color()
        for btn in self.lockable_buttons:
            btn.configure(state='disabled')

    def _unlock_buttons(self):
        self._reset_button_color()
        for btn in self.lockable_buttons:
            btn.configure(state='normal')

    def _reset_button_color(self):
        color = 'SystemButtonFace'
        for btn in self.lockable_buttons:
            btn.configure(bg=color)

    def _reset_paths_on_lock_selection(self):
        for key, value in self.stringvars.items():
            value.set('')

        self._reset_paths_in_svea_controller()
        self._set_paths_on_lock()

    def _set_paths_on_lock(self):
        working_dir = self.user.basic_dirs.setdefault('working', '')
        # raw_files_dir = self.user.basic_dirs.setdefault('raw_files', '')

        self._set_working_directory(working_dir)
        # self._set_raw_files_directory(raw_files_dir)

    def _reset_paths_in_svea_controller(self):
        self.svea_controller.reset_paths()

    def _save_user_settings(self):
        self.user.basic_dirs.set('working', self.stringvars['working_dir'].get())
        self.user.basic_dirs.set('raw_files', self.stringvars['raw_files_dir'].get())
        self.user.basic_dirs.set('cnv_files', self.stringvars['cnv_files_dir'].get())
        self.user.basic_dirs.set('standard_files', self.stringvars['standard_files_dir'].get())

        self.user.basic_options.set('overwrite', self.booleanvar_allow_overwrite.get())
        self.user.basic_options.set('unlock_selections', self.booleanvar_unlock_selections.get())

    def _load_user_setting(self):
        self.stringvars['working_dir'].set(self.user.basic_dirs.setdefault('working', ''))
        self.stringvars['raw_files_dir'].set(self.user.basic_dirs.setdefault('raw_files', ''))
        self.stringvars['cnv_files_dir'].set(self.user.basic_dirs.setdefault('cnv_files', ''))
        self.stringvars['standard_files_dir'].set(self.user.basic_dirs.setdefault('standard_files', ''))

        self.booleanvar_allow_overwrite.set(self.user.basic_options.setdefault('overwrite', False))
        self.booleanvar_unlock_selections.set(self.user.basic_options.setdefault('unlock_selections', False))

    def _highlight_button(self, button_ref):
        self._reset_button_color()
        self._lock_buttons()
        button_ref.configure(state='normal')
        button_ref.configure(bg='darkgreen')

    def _callback_run_seb_processing(self):
        try:
            new_dir = self.svea_controller.sbe_processing()
        except Exception as e:
            messagebox.showerror('Internal error', e)
            if DEBUG:
                raise e
            return
        self._set_raw_files_directory(new_dir)
        if self._is_locked():
            self._highlight_button(self.button_create_metadata)

    def _callback_create_metadata_file(self):
        try:
            new_dir = self.svea_controller.create_metadata_file()
        except Exception as e:
            messagebox.showerror('Internal error', e)
            if DEBUG:
                raise e
            return
        self._set_cnv_files_directory(new_dir)
        if self._is_locked():
            self._highlight_button(self.button_create_standard_files)

    def _callback_create_standard_format(self):
        try:
            new_dir = self.svea_controller.create_standard_format()
        except Exception as e:
            messagebox.showerror('Internal error', e)
            if DEBUG:
                raise e
            return
        self._set_standard_files_directory(new_dir)
        if self._is_locked():
            self._highlight_button(self.button_run_automatic_qc)

    def _callback_run_automatic_qc(self):
        try:
            self.svea_controller.perform_automatic_qc()
        except Exception as e:
            messagebox.showerror('Internal error', e)
            if DEBUG:
                raise e
            return

    def _callback_run_bokeh_server(self):

        self.svea_controller.bokeh_visualize_setting = self.combobox_vis.get_value()
        # venv
        venv_path = Path(Path(__file__).parent.parent.parent.parent.parent, 'venv_py36_sharktools')
        if not venv_path.exists():
            venv_path = None
        # server_directory
        server_directory = Path(Path(__file__).parent.parent.parent.parent)

        self.svea_controller.open_visual_qc(server_file_directory=server_directory,
                                            venv_path=venv_path,
                                            # month_list=[4, 5, 6],
                                            )

    def update_page(self):
        self.user = self.user_manager.user
        self._load_user_setting()

        self._toggle_overwrite()
        self._toggle_unlock_selections()

        self._update_svea_paths()
        print('WORKING DIRECTORY', self.svea_controller.working_directory)

    def _raw_files_are_present(self):
        if 'btl' in self.stringvars['raw_files_dir_info'].get():
            return True
        return False


def get_directory_info(directory):
    if not directory:
        return ''
    directory = Path(directory)
    if not directory.exists():
        return ''
    content = {}
    for file_name in os.listdir(directory):
        file_path = Path(directory, file_name)
        if file_path.is_dir():
            content.setdefault('dirs', 0)
            content['dirs'] += 1
        else:
            suffix = file_path.suffix
            content.setdefault(suffix, 0)
            content[suffix] += 1

    return_list = []
    for key, value in content.items():
        string = f'{value} ({key})'
        return_list.append(string)
    return ' - '.join(return_list)


def get_sub_directory(directory, new=False):
    time_str = datetime.datetime.now().strftime('%Y%m%d%H%M')
    directory = Path(directory)
    name = str(directory.name)

    if not name.isdigit():
        return str(Path(directory, time_str))

    if not directory.exists():
        return str(directory)

    if name == time_str and new:
        while directory.exists():
            directory = Path(str(directory) + '0')
        return directory

    return str(directory)