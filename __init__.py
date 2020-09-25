# Copyright (c) 2018 SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from . import gui
from .app import App


INFO = dict(title='Svea CTD',
            users_directory='users',
            sub_pages=[dict(name='PageStart',
                            title='Start'),
                       dict(name='PageBasic',
                            title='Svea CTD (enkel)'),
                       dict(name='PageAdvanced',
                            title='Svea CTD (avancerad)')
                       ],
            user_page_class='PageUser')  # Must match name in ALL_PAGES in main app

USER_SETTINGS = [('basic', 'directory'),
                 ('basic', 'create_options'),
                 ('basic', 'basic_options'),
                 ('basic', 'basic_dirs')]
