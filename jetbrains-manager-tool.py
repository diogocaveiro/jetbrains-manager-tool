#!/usr/bin/env python3

import requests
import argparse
import os

JETBRAINS_XML_URL = 'https://www.jetbrains.com/updates/updates.xml'
JETBRAINS_INSTALL_PATH = '/opt/jetbrains/'

APP_LIST = {
    'pycharm': {
        'arg': '-p',
        'help': 'PyCharm',
        'folder': 'pycharm',
    },
}

class JetbrainsUpdater:
    def __init__(self):
        print('Initializing Jetbrains Updater.')

        # Parse arguments
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('-u', '--update', action='store_true', help='Update mode.')
        arg_parser.add_argument('-i', '--install', action='store_true', help='Install mode.')
        for app in APP_LIST.values():
            arg_parser.add_argument(app['arg'], action='store_true', help=app['help'])
        args = arg_parser.parse_args()

        if args.update and args.install:
            print('Error: You can only use either update or install arguments.')
            return
        elif not args.update and not args.install:
            print('Error: You must use either an update or install arguments.')
            return

        # Check installed apps
        self.__check_installed_apps()


    def __check_installed_apps(self):
        """
        Checks installed apps.
        """
        self.installed_apps = []
        for key, value in APP_LIST.items():
            if os.path.exists(os.path.join('/opt', value['folder'])):
                self.installed_apps.append(key)
        #self.installed_apps = ['DOG', 'CAT', 'MOUSE']
        if self.installed_apps:
            print('The following apps are already installed:\n' + '\n'.join(self.installed_apps))
        else:
            print('No app installed in the designated install folder.')

    def __fetch_xml(self):
        """
        Fetch XML file
        """
        try:
            req = requests.get(JETBRAINS_XML_URL)
            assert req.status_code == 200
            self.xml_file = req.content
        except Exception as e:
            print(e)


if __name__ == '__main__':
    updater = JetbrainsUpdater
    updater()