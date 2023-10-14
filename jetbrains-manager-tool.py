#!/usr/bin/env python3

"""
    TODO:
        - Update all
        - Update selected apps
        - Change default path
"""

import requests
import argparse
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

JETBRAINS_XML_URL = "https://www.jetbrains.com/updates/updates.xml"
JETBRAINS_INSTALL_PATH = "/opt/jetbrains/"

APP_LIST = {
    "pycharm": {
        "flag": "-p",
        "long_flag": "--pycharm",
        "help": "PyCharm Professional",
        "folder": "pycharm",
        "name": "PyCharm",
        "channel_name": "PyCharm RELEASE",
        "download-link": "https://download.jetbrains.com/python/pycharm-professional-<VERSION>.tar.gz",
    },
    "clion": {
        "flag": "-c",
        "long_flag": "--clion",
        "help": "CLion",
        "folder": "clion",
    },
}


class JetbrainsManagerTool:
    def __init__(self):
        print("Initializing Jetbrains Updater.")

        # Check for root permission
        if os.geteuid() != 0:
            print("This script requires root permissions. Please enter your password.")

            ret = subprocess.call(["sudo", "python3"] + sys.argv)
            if ret != 0:
                print("Failed to gain root permissions.")
                sys.exit(1)
            sys.exit(0)

        # Parse arguments
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            "-u", "--update", action="store_true", help="Update mode."
        )
        arg_parser.add_argument(
            "-i", "--install", action="store_true", help="Install mode."
        )
        for app in APP_LIST.values():
            arg_parser.add_argument(app["flag"], action="store_true", help=app["help"])
        args = arg_parser.parse_args()

        if args.update and args.install:
            print("Error: You can only use either update or install flags.")
            return
        elif not args.update and not args.install:
            print("Error: You must use either an update or install flags.")
            return

        # Check selected apps
        self.selected_apps = [
            app_key
            for app_key, app_data in APP_LIST.items()
            if getattr(args, app_data["flag"][-1], False)
        ]

        # Check installed apps
        self.__check_installed_apps()

        # Fetch JetBrains XML file
        self.__fetch_xml()

        # Install mode
        if args.install:
            if not self.selected_apps:
                print("No app selected. Stopping installer.")
                return
            else:
                self.__install()

        # Update mode
        if args.update:
            pass
            # TODO: Update

    def __check_installed_apps(self):
        """
        Checks installed apps.
        """
        self.installed_apps = []
        for key, value in APP_LIST.items():
            if os.path.exists(os.path.join("/opt", value["folder"])):
                self.installed_apps.append(key)
        if self.installed_apps:
            print(
                "The following apps are already installed:\n"
                + "\n".join(self.installed_apps)
            )
        else:
            print("No app installed in the designated install folder.")

    def __fetch_xml(self):
        """
        Fetch XML file.
        """
        try:
            req = requests.get(JETBRAINS_XML_URL)
            assert req.status_code == 200
            self.xml_file = req.content
            print("Successfully fetched Jetbrains XML file.")
        except Exception as e:
            print(e)

    def __install(self):
        """
        Installs selected apps.
        TODO: Check if app is already installed.
        """
        root = ET.fromstring(self.xml_file)

        for selected_app in self.selected_apps:
            # Define install path
            install_path = os.path.join(JETBRAINS_INSTALL_PATH, APP_LIST[selected_app]['folder'])

            # Check if app is already installed
            if os.path.exists(install_path):
                print(f"{APP_LIST[selected_app]['name']} is already installed. Skipping installation.")
                continue

            # Check last version
            version_query = "./product[@name='{}']/channel[@name='{}']/build".format(
                APP_LIST[selected_app]['name'],
                APP_LIST[selected_app]['channel_name']
            )
            version_elements = root.findall(version_query)

            if version_elements:
                last_version = version_elements[0].get('version')
            else:
                print("Couldn't find data for {}".format(APP_LIST[selected_app]['name']))

            # Download latest version
            download_link = APP_LIST[selected_app]["download-link"].replace("<VERSION>", last_version)
            print(f"Downloading {APP_LIST[selected_app]['name']} from {download_link}")
            download_path = os.path.join(os.getcwd(),
                                         '{}-{}.tar.gz'.format(APP_LIST[selected_app]['name'], last_version))

            if os.path.exists(download_path):
                print("File already exists. Skipping download.")
            else:
                try:
                    req = requests.get(download_link)
                    assert req.status_code == 200

                    with open(download_path, 'wb') as f:
                        f.write(req.content)

                    print("Successfully downloaded app file to {}".format(download_path))
                except Exception as e:
                    print(e)

            # Extract file
            print("Extracting file...")
            if not os.path.exists(install_path):
                os.makedirs(install_path)
                try:
                    subprocess.call(['sudo', 'tar', '-xzf', download_path, '-C', install_path, '--strip-components=1'])
                    print("Successfully extracted file to {}".format(install_path))
                except Exception as e:
                    print(e)

            # Create desktop entry
            try:
                desktop_entry_path = os.path.join('/usr/share/applications', '{}.desktop'.format(selected_app))

                if os.path.exists(desktop_entry_path):
                    print("Desktop entry already exists. Deleting it.")
                    os.remove(desktop_entry_path)

                with open(desktop_entry_path, 'w') as f:
                    f.write("[Desktop Entry]\n")
                    f.write("Name={}\n".format(APP_LIST[selected_app]['help']))
                    f.write("Exec={}/bin/{}.sh\n".format(install_path, selected_app))
                    f.write("Icon={}/bin/{}.png\n".format(install_path, selected_app))
                    f.write("Terminal=false\n")
                    f.write("Type=Application\n")
                    f.write("Categories=Development;\n")

                print("Successfully created desktop entry at {}".format(desktop_entry_path))
            except Exception as e:
                print(e)

            # Create symlink
            try:
                symlink_path = os.path.join('/usr/local/bin', selected_app)

                if os.path.exists(symlink_path):
                    print("Symlink already exists. Deleting it.")
                    os.remove(symlink_path)

                os.symlink(os.path.join(install_path, 'bin', selected_app + '.sh'), symlink_path)

                print("Successfully created symlink at {}".format(symlink_path))
            except Exception as e:
                print(e)

            # Chmod +x on executable
            try:
                executable_path = os.path.join(install_path, 'bin', selected_app + '.sh')
                subprocess.call(['sudo', 'chmod', '+x', executable_path])
                print("Successfully set executable permissions on {}".format(executable_path))
            except Exception as e:
                print(e)


if __name__ == "__main__":
    updater = JetbrainsManagerTool
    updater()
