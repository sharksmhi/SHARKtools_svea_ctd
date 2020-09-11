#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2018 SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
import datetime
import shutil
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import gui as main_gui
import os

from sharkpylib.tklib import tkinter_widgets as tkw

from ctdpy.core import session as ctdpy_session
from ctdpy.core.utils import generate_filepaths

from pathlib import Path


class PageCreateStandardFormat(tk.Frame):

    def __init__(self, parent, parent_app, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        # parent is the frame "container" in App. contoller is the App class
        self.parent = parent
        self.parent_app = parent_app
        self.main_app = self.parent_app.main_app
        self.logger = self.parent_app.logger
        self.user_manager = parent_app.user_manager
        self.user = self.user_manager.user

    def _build(self):
        padding = dict(padx=15,
                       pady=15)

        frame_working_directory = ttk.LabelFrame(self, text='Working directory')
        frame_working_directory.grid(row=0, column=0, sticky='nsew', **padding)

        frame_metadata_file = ttk.LabelFrame(self, text='Create metadata file')
        frame_metadata_file.grid(row=1, column=0, sticky='nsew', **padding)

        frame_standard_format = ttk.LabelFrame(self, text='Create standard format files')
        frame_standard_format.grid(row=2, column=0, sticky='nsew', **padding)

        tkw.grid_configure(self, nr_columns=1, nr_rows=3)

        self._build_frame_working_directory(frame_working_directory)
        self._build_frame_metadata_file(frame_metadata_file)
        self._build_frame_standard_format(frame_standard_format)

    def _build_frame_working_directory(self, frame):
        padding = dict(padx=10,
                       pady=5,
                       sticky='w')
        ttk.Button(frame, text='Get', command=self._select_working_directory).grid(row=0, column=0, **padding)
        ttk.Button(frame, text='Generate subdirectory', command=self._generate_subdirectory).grid(row=0, column=1, **padding)
        tk.Label(frame, text='Working directory:').grid(row=0, column=2, **padding)
        self.strvar_working_directory = tk.StringVar()
        tk.Label(frame, textvariable=self.strvar_working_directory).grid(row=0, column=3, **padding)
        self.strvar_working_directory.set(self.user.directory.setdefault('working_directory', ''))

        self.strvar_working_directory_info = tk.StringVar()
        tk.Label(frame, text='Info').grid(row=1, column=0, **padding)
        tk.Label(frame, textvariable=self.strvar_working_directory_info).grid(row=1, column=1, columnspan=3, **padding)

        self._update_working_directory_information()

    def _build_frame_standard_format(self, frame):
        padding = dict(padx=10,
                       pady=5,
                       sticky='w')
        ttk.Button(frame,
                   text='Create standard format files',
                   command=self._create_standard_format_files).grid(row=0, column=0, **padding)

    def _create_standard_format_files(self):
        try:
            working_directory = self._get_working_directory()
            if not self._is_validate_working_directory(working_directory):
                messagebox.showinfo('Create standard files', 'Not a valid working directory')
                self.logger.info('Not a valid working directory')
                return

            if not self._working_directory_has_files_for_creating_standard_fromat():
                messagebox.showinfo('Create standard files', 'No files to process in working directory')
                self.logger.info(f'No files in working directory: {working_directory}')
                return

            save_directory = Path(working_directory, 'standard_format_files')
            if save_directory.exists():
                if os.listdir(save_directory):
                    if messagebox.askyesno('Create standard files', 'Output files already exist. Do you want to delete the old ones?'):
                        self._delete_files_in_directory(save_directory)
                    else:
                        messagebox.showinfo('Create standard files', 'Aborted by user')
            else:
                os.makedirs(save_directory)

            files = generate_filepaths(working_directory,
                                       pattern_list=['.cnv', '.xlsx'],
                                       only_from_dir=True)

            session = ctdpy_session.Session(filepaths=files,
                                            reader='smhi')

            start_time = time.time()
            datasets = session.read()
            self.logger.debug("Datasets loaded--%.3f sec" % (time.time() - start_time))

            start_time = time.time()
            data_path = session.save_data(datasets,
                                          writer='ctd_standard_template',
                                          return_data_path=True,
                                          # save_path=save_directory,
                                          )
            for file_name in os.listdir(data_path):
                source_path = Path(data_path, file_name)
                target_path = Path(save_directory, file_name)
                shutil.copy2(source_path, target_path)

            self.logger.debug(f"Datasets saved in {time.time() - start_time} sec at location: {data_path}. Files copied to: {save_directory}")
            messagebox.showinfo('Create standard files', f'Standard format files created in directory: {save_directory}')

        except Exception as e:
            self.logger.error(e)
            messagebox.showerror('Internal error', e)

    def _build_frame_metadata_file(self, frame):
        padding = dict(padx=10,
                       pady=5)

        metadata_upper_left_frame = tk.Frame(frame)
        metadata_upper_left_frame.grid(row=0, column=0, sticky='nsew', **padding)

        metadata_upper_right_frame = tk.Frame(frame)
        metadata_upper_right_frame.grid(row=0, column=1, sticky='nsew', **padding)

        metadata_lower_left_frame = ttk.LabelFrame(frame, text='Options')
        metadata_lower_left_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', **padding)

        metadata_lower_right_frame = tk.Frame(frame)
        metadata_lower_right_frame.grid(row=1, column=1, columnspan=2, sticky='nsew', **padding)

        self._build_frame_load_cnv(metadata_upper_left_frame)
        self._build_frame_manual_metadata(metadata_upper_right_frame)
        self._build_frame_options(metadata_lower_left_frame)
        self._build_frame_create_metadata_file(metadata_lower_right_frame)

    def _build_frame_load_cnv(self, frame):
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
        tk.Label(str_frame, text='Source directory:').grid(row=0, column=0, sticky='w')
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

        # Link entries
        for f, t in zip(entry_list[:-1], entry_list[1:]):
            f.bind('<Return>', lambda event, x=t: x.focus())
            f.bind('<Down>', lambda event, x=t: x.focus())
            t.bind('<Up>', lambda event, x=f: x.focus())

    def _build_frame_options(self, frame):
        padding = dict(padx=10,
                       pady=5,
                       sticky='w')

        self.boolean_overwrite_metadata = tk.BooleanVar()
        ttk.Checkbutton(frame, text='Overwrite metadata', variable=self.boolean_overwrite_metadata).grid(row=0, column=0, **padding)
        self.boolean_overwrite_metadata.set(self.user.create_options.setdefault('overwrite_metadata', False))

    def _build_frame_create_metadata_file(self, frame):
        padding = dict(padx=10,
                       pady=5,
                       sticky='w')
        self.button_create_metadata_file = ttk.Button(frame,
                                                      text='Create metadata file',
                                                      command=self._callback_create_metadata_file)
        self.button_create_metadata_file.grid(row=0, column=0, **padding)

    def _select_working_directory(self):
        directory = filedialog.askdirectory()
        if not directory:
            return
        self.strvar_working_directory.set(directory)
        self.user.directory.set('working_directory', str(directory))
        self._update_working_directory_information()

    def _is_validate_working_directory(self, working_directory=None):
        if not working_directory:
            working_directory = self._get_working_directory()
        if not working_directory:
            return False
        working_directory = Path(working_directory)
        names = [working_directory.name, working_directory.parent.name]
        for name in names:
            split_name = name.split('_')
            if split_name[0] == 'svea' and split_name[1] == 'ctd' and split_name[2].isdigit():
                return True
        return False

    def _get_working_directory(self):
        return self.strvar_working_directory.get()

    def _create_working_directory(self, working_directory):
        if self.directory_exists(working_directory):
            return
        if not self._is_validate_working_directory(working_directory):
            return
        os.makedirs(working_directory)

    @staticmethod
    def get_subdirectory_string():
        return f'svea_ctd_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}'

    @staticmethod
    def directory_is_empty(directory):
        if os.listdir(directory):
            return False
        return True
    
    def _working_directory_has_files_for_creating_standard_fromat(self, working_directory=None):
        if not working_directory:
            working_directory = self._get_working_directory()
        has_cnv = False
        has_xlsx = False
        for file_name in os.listdir(working_directory):
            suffix = Path(file_name).suffix
            if suffix == '.cnv':
                has_cnv = True
            elif suffix == '.xlsx':
                has_xlsx = True

        if has_cnv and has_xlsx:
            return True
        return False


    @staticmethod
    def directory_exists(directory):
        return Path(directory).exists()

    def _delete_files_in_directory(self, directory):
        if not self.directory_exists(directory):
            self.logger.debug(f'Directory does not exist: {directory}')
            return False
        if self.directory_is_empty(directory):
            self.logger.debug(f'Directory is empty: {directory}')
            return False
        if not self._is_validate_working_directory(directory):
            self.logger.debug(f'Directory is not a valid working directory: {directory}')
            return False

        for file_name in os.listdir(directory):
            file_path = Path(directory, file_name)
            try:
                if file_path.is_file():
                    os.remove(str(file_path))
                elif file_path.is_dir():
                    shutil.rmtree(str(file_path))
            except Exception as e:
                self.logger.error(e)
                messagebox.showerror('Removing files', e)
        self.logger.debug(f'Deleted files in directory: {directory}')
        return True

    def _generate_subdirectory(self):
        working_directory = self.strvar_working_directory.get()
        if not working_directory:
            main_gui.show_information('Generate subdirectory', 'You have to set the working directory before you can generate a subdirectory!')
            self.logger.info('Trying to generate subdirektory with no working directory present')
            return
        working_directory = Path(working_directory)
        main_directory = working_directory.parent
        if self._is_validate_working_directory(working_directory):
            new_directory = Path(main_directory, self.get_subdirectory_string())
        else:
            new_directory = Path(working_directory, self.get_subdirectory_string())
        self.strvar_working_directory.set(new_directory)
        self.user.directory.set('working_directory', str(new_directory))
        self._update_working_directory_information()

    def _update_working_directory_information(self):
        working_directory = self._get_working_directory()
        string = ''
        if not self._is_validate_working_directory(working_directory):
            string = 'Not a valid working directory'
            self.strvar_working_directory_info.set(string)
            return

        if not working_directory:
            string = 'No working directory selected'
            self.strvar_working_directory_info.set(string)
            return

        working_directory = Path(working_directory)
        if not working_directory.exists():
            string = 'Working directory does not exist'
            self.strvar_working_directory_info.set(string)
            return

        file_names = os.listdir(working_directory)
        if not file_names:
            string = 'Directory exists and is empty'
            self.strvar_working_directory_info.set(string)
            return

        suffixes = {}
        for file_name in file_names:
            suffix = Path(file_name).suffix
            suffixes.setdefault(suffix, 0)
            suffixes[suffix] += 1
        string_list = []
        for suffix, nr in suffixes.items():
            string_list.append(f'{suffix}-files ({str(nr)})')
        string = f'Files in working directory: {", ".join(string_list)}'
        self.strvar_working_directory_info.set(string)
        return

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

    def _callback_create_metadata_file(self, *args, **kwargs):
        try:
            # Check working path
            working_directory = self._get_working_directory()
            if not self._is_validate_working_directory(working_directory):
                self.logger.debug(f'Not a valid working directory: {working_directory}')
                main_gui.show_information('Creating metadata file', 'You need to specify a valid working directory')
                return

            if not self.directory_exists(working_directory):
                self.logger.debug(f'Creating working directory: {working_directory}')
                os.makedirs(working_directory)

            delete_files = False
            generate_subdir = False

            if not self.directory_is_empty(working_directory):
                if not messagebox.askyesno('Create metadata file', 'Working directory is not empty. Do you want to remove the old files and continue?'):
                    if messagebox.askyesno('Create metadata file', 'Do you want to create a new subdirectory for your files instead?'):
                        generate_subdir = True
                    else:
                        messagebox.showinfo('Create metadata file', 'Aborted by user')
                        return
                else:
                    delete_files = True

            if generate_subdir:
                self._generate_subdirectory()
                self._update_working_directory_information()
                working_directory = self._get_working_directory()
                self.logger.debug(f'Subdirectory generated: {working_directory}')
                self._update_working_directory_information()

            elif delete_files:
                ok = self._delete_files_in_directory(working_directory)
                if not ok:
                    messagebox.showinfo('Create metadata file', f'Could not remove files in directory {working_directory}')
                    return
                self.logger.debug(f'Files deleted in: {working_directory}')

            file_names = self.cnv_files_selection_widget.get_selected()
            if not file_names:
                self.logger.debug(f'No CNV files selected')
                messagebox.showinfo('Create metadata file', 'No CNV files selected!')
                return

            file_paths = [str(self.cnv_files_paths.get(file_name)) for file_name in file_names]
            session = ctdpy_session.Session(filepaths=file_paths,
                                            reader='smhi')
            start_time = time.time()
            datasets = session.read()
            self.logger.debug(f'{len(file_paths)} CNV files loaded in {time.time()-start_time} seconds.')

            # Check metadata
            metadata = {}
            for key, strvar in self.manual_metadata_stringvars.items():
                value = strvar.get().strip()
                if not value:
                    continue
                metadata[key] = value
            self.logger.debug(f'{len(metadata)} metadata parameters selected for update')

            # Update metadata in datasets
            overwrite = self.boolean_overwrite_metadata.get()
            self.logger.debug(f'Overwrite metadata is set to {overwrite}')
            session.update_metadata(datasets=datasets[0], metadata=metadata, overwrite=overwrite)
            self.logger.debug('Metadata updated in datasets')

            # Save data
            self._create_working_directory(working_directory)
            start_time = time.time()
            save_path = session.save_data(datasets[0],
                                          writer='metadata_template',
                                          return_data_path=True)
            self.logger.debug(f'Data saved in {time.time()-start_time} seconds at location {save_path}')

            # Save options
            self.user.create_options.set('overwrite_metadata', overwrite)

            # Copy metadata file
            source_path = Path(save_path)
            target_path = Path(working_directory, source_path.name)
            shutil.copy2(source_path, target_path)

            # Copy cnv files
            for file_path in file_paths:
                source_path = Path(file_path)
                target_path = Path(working_directory, source_path.name)
                shutil.copy2(source_path, target_path)

            self.main_app.update_help_information(f'Data copied to: {working_directory}')
            self.user.directory.set('working_directory', working_directory)
            self.logger.info(f'Data moved to {working_directory}')

        except ImportError as e:
            self.logger.error(e)
            main_gui.show_error('Internal error', e)

        self._update_working_directory_information()


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