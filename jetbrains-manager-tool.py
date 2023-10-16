#!/usr/bin/env python3

"""
    TODO:
        - Update all
        - Update selected apps
        - Change default path
        - Update mimeapps.list
        - Check if download link exists before download
"""

import requests
import argparse
import os
import subprocess
import sys
import xml.etree.ElementTree as elementTree
import json

JETBRAINS_XML_URL = "https://www.jetbrains.com/updates/updates.xml"
ANDROID_STUDIO_XML_URL = "https://dl.google.com/android/studio/patches/updates.xml"
JETBRAINS_INSTALL_PATH = "/opt/jetbrains/"

APP_LIST = {
    "android-studio": {
        "flag": "-t",
        "long_flag": "--android-studio",
        "help": "Android Studio",
        "folder": "android-studio",
        "name": "Android Studio",
        "channel_name": "Android Studio updates",
        "download-link": "https://redirector.gvt1.com/edgedl/android/studio/ide-zips/<VERSION>/android-studio-<VERSION>-linux.tar.gz",
        "comment": "An IDE for Android app development",
        "executable": "studio",
    },
    "pycharm-professional": {
        "flag": "-p",
        "long_flag": "--pycharm",
        "help": "PyCharm Professional",
        "folder": "pycharm",
        "name": "PyCharm",
        "channel_name": "PyCharm RELEASE",
        "download-link": "https://download.jetbrains.com/python/pycharm-professional-<VERSION>.tar.gz",
        "comment": "The full stack Python IDE",
        "executable": "pycharm",
    },
    "clion": {
        "flag": "-c",
        "long_flag": "--clion",
        "help": "CLion",
        "folder": "clion",
        "name": "CLion",
        "channel_name": "CLion RELEASE",
        "download-link": "https://download.jetbrains.com/cpp/CLion-<VERSION>.tar.gz",
        "comment": "A cross-platform IDE for C and C++",
        "executable": "clion",
    },
    "datagrip": {
        "flag": "-d",
        "long_flag": "--datagrip",
        "help": "DataGrip",
        "folder": "datagrip",
        "name": "DataGrip",
        "channel_name": "DataGrip RELEASE",
        "download-link": "https://download.jetbrains.com/datagrip/datagrip-<VERSION>.tar.gz",
        "comment": "Your Swiss Army Knife for Databases and SQL",
        "executable": "datagrip",
    },
    "goland": {
        "flag": "-g",
        "long_flag": "--goland",
        "help": "GoLand",
        "folder": "goland",
        "name": "GoLand",
        "channel_name": "GoLand RELEASE",
        "download-link": "https://download.jetbrains.com/go/goland-<VERSION>.tar.gz",
        "comment": "A Clever IDE to Go",
        "executable": "goland",
    },
    "intellij-community": {
        "flag": "-n",
        "long_flag": "--intellij-community",
        "help": "IntelliJ IDEA Community",
        "folder": "ideaIC",
        "name": "IntelliJ IDEA",
        "channel_name": "IntelliJ IDEA RELEASE",
        "download-link": "https://download.jetbrains.com/idea/ideaIC-<VERSION>.tar.gz",
        "comment": "The IDE for Java and Kotlin enthusiasts",
        "executable": "idea",
    },
    "intellij-ultimate": {
        "flag": "-m",
        "long_flag": "--intellij-ultimate",
        "help": "IntelliJ IDEA Ultimate",
        "folder": "ideaIU",
        "name": "IntelliJ IDEA",
        "channel_name": "IntelliJ IDEA RELEASE",
        "download-link": "https://download.jetbrains.com/idea/ideaIU-<VERSION>.tar.gz",
        "comment": "The Leading Java and Kotlin IDE",
        "executable": "idea",
    },
    "phpstorm": {
        "flag": "-k",
        "long_flag": "--phpstorm",
        "help": "PhpStorm",
        "folder": "phpstorm",
        "name": "PhpStorm",
        "channel_name": "PhpStorm RELEASE",
        "download-link": "https://download.jetbrains.com/webide/PhpStorm-<VERSION>.tar.gz",
        "comment": "The Lightning-Smart IDE for PHP Programming",
        "executable": "phpstorm",
    },
    "pycharm-community": {
        "flag": "-y",
        "long_flag": "--pycharm-community",
        "help": "PyCharm Community",
        "folder": "pycharm-community",
        "name": "PyCharm Community",
        "channel_name": "PyCharm RELEASE",
        "download-link": "https://download.jetbrains.com/python/pycharm-community-<VERSION>.tar.gz",
        "comment": "The Python IDE for Professional Developers",
        "executable": "pycharm",
    },
    "pycharm-edu": {
        "flag": "-e",
        "long_flag": "--pycharm-edu",
        "help": "PyCharm Edu",
        "folder": "pycharm-edu",
        "name": "PyCharm Edu",
        "channel_name": "PyCharm Edu RELEASE",
        "download-link": "https://download.jetbrains.com/python/pycharm-edu-<VERSION>.tar.gz",
        "comment": "The Python IDE for Professional Developers",
        "executable": "pycharm",
    },
    "rider": {
        "flag": "-x",
        "long_flag": "--rider",
        "help": "Rider",
        "folder": "rider",
        "name": "Rider",
        "channel_name": "Rider RELEASE",
        "download-link": "https://download.jetbrains.com/rider/JetBrains.Rider-<VERSION>.tar.gz",
        "comment": "Cross-platform .NET IDE based on IntelliJ platform and ReSharper",
        "executable": "rider",
    },
    "rubymine": {
        "flag": "-b",
        "long_flag": "--rubymine",
        "help": "RubyMine",
        "folder": "rubymine",
        "name": "RubyMine",
        "channel_name": "RubyMine RELEASE",
        "download-link": "https://download.jetbrains.com/ruby/RubyMine-<VERSION>.tar.gz",
        "comment": "The Most Intelligent Ruby and Rails IDE",
        "executable": "rubymine",
    },
    "webstorm": {
        "flag": "-w",
        "long_flag": "--webstorm",
        "help": "WebStorm",
        "folder": "webstorm",
        "name": "WebStorm",
        "channel_name": "WebStorm RELEASE",
        "download-link": "https://download.jetbrains.com/webstorm/WebStorm-<VERSION>.tar.gz",
        "comment": "The Smartest JavaScript IDE",
        "executable": "webstorm",
    },
    "appcode": {
        "flag": "-a",
        "long_flag": "--appcode",
        "help": "AppCode",
        "folder": "appcode",
        "name": "AppCode",
        "channel_name": "AppCode RELEASE",
        "download-link": "https://download.jetbrains.com/objc/AppCode-<VERSION>.tar.gz",
        "comment": "Smart IDE for iOS/macOS development",
        "executable": "appcode",
    },
    "aquacode": {
        "flag": "-q",
        "long_flag": "--aquacode",
        "help": "AquaCode",
        "folder": "aquacode",
        "name": "AquaCode",
        "channel_name": "AquaCode RELEASE",
        "download-link": "https://download.jetbrains.com/aquacode/AquaCode-<VERSION>.tar.gz",
        "comment": "A powerful IDE for test automation",
        "executable": "aquacode",
    },
    "dataspell": {
        "flag": "-s",
        "long_flag": "--dataspell",
        "help": "DataSpell",
        "folder": "dataspell",
        "name": "DataSpell",
        "channel_name": "DataSpell RELEASE",
        "download-link": "https://download.jetbrains.com/python/dataspell-<VERSION>.tar.gz",
        "comment": "The data science IDE",
        "executable": "dataspell",
    },
    "rustrover": {
        "flag": "-o",
        "long_flag": "--rustrover",
        "help": "RustRover",
        "folder": "rustrover",
        "name": "RustRover",
        "channel_name": "RustRover RELEASE",
        "download-link": "https://download.jetbrains.com/rustrover/RustRover-<VERSION>.tar.gz",
        "comment": "The IDE for Rust",
        "executable": "rustrover",
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
            self.__install(update=True)

    def __check_installed_apps(self):
        """
        Checks installed applications and its versions.
        """
        # Check installed applications
        self.installed_apps = {}
        for key, value in APP_LIST.items():
            install_path = os.path.join(JETBRAINS_INSTALL_PATH, value["folder"])
            print(install_path)
            if os.path.exists(install_path):
                print('exists')
                with open(os.path.join(install_path, 'product-info.json'), 'r') as json_file:
                    version = json.load(json_file)['version']
                    print(f'{key}: {version}')
                self.installed_apps[key] = version

        # Print result
        if self.installed_apps:
            print(
                "The following apps are already installed:\n"
                + "\n".join(self.installed_apps.keys())
            )
        else:
            print("No app installed in the designated install folder.")

    def __fetch_xml(self):
        """
        Fetch XML file.
        """
        try:
            # Fetch Jetbrains XML file
            req_jetbrains = requests.get(JETBRAINS_XML_URL)
            assert req_jetbrains.status_code == 200
            jetbrains_xml = req_jetbrains.content
            print("Successfully fetched Jetbrains XML file.")

            # Fetch Android Studio XML file
            req_android_studio = requests.get(ANDROID_STUDIO_XML_URL)
            assert req_android_studio.status_code == 200
            android_studio_xml = req_android_studio.content

            # Append Android Studio XML to JetBrains XML
            jetbrains_root = elementTree.fromstring(jetbrains_xml)
            android_studio_root = elementTree.fromstring(android_studio_xml)
            for child in android_studio_root:
                jetbrains_root.append(child)

            self.xml_file = elementTree.tostring(jetbrains_root, encoding="utf-8")

            print(
                "Successfully fetched and combined JetBrains and Android Studio XML files."
            )

        except Exception as e:
            print(e)

    def __update(self):
        """
        Updates selected or all installed apps.
        """
        pass

    def __install(self, update=False):
        """
        Installs selected apps.
        """
        root = elementTree.fromstring(self.xml_file)

        # Check outdated applications
        if update:
            print('UPDATE CALLED')
            outdated_apps = []
            for installed_app, installed_version in self.installed_apps.items():
                version_query = "./product[@name='{}']/channel[@name='{}']/build".format(
                    APP_LIST[installed_app]["name"], APP_LIST[installed_app]["channel_name"]
                )
                version_elements = root.findall(version_query)

                if version_elements:
                    last_version = version_elements[0].get("version")

                    if installed_app == "android-studio":
                        last_version = last_version.split(" ")[2]
                else:
                    print(
                        "Couldn't find data for {}".format(APP_LIST[installed_app]["name"])
                    )

                if installed_version != last_version:
                    outdated_apps.append(installed_app)

            print(outdated_apps)

            return

        for selected_app in self.selected_apps:
            # Define install path
            install_path = os.path.join(
                JETBRAINS_INSTALL_PATH, APP_LIST[selected_app]["folder"]
            )

            # Check if app is already installed
            if os.path.exists(install_path):
                print(
                    f"{APP_LIST[selected_app]['name']} is already installed. Skipping installation."
                )
                continue

            # Check last version
            version_query = "./product[@name='{}']/channel[@name='{}']/build".format(
                APP_LIST[selected_app]["name"], APP_LIST[selected_app]["channel_name"]
            )
            version_elements = root.findall(version_query)

            if version_elements:
                last_version = version_elements[0].get("version")

                if selected_app == "android-studio":
                    last_version = last_version.split(" ")[2]
            else:
                print(
                    "Couldn't find data for {}".format(APP_LIST[selected_app]["name"])
                )

            # Download latest version
            if selected_app == "android-studio":
                valid_link_found = False
                for suffix in reversed(range(1, 30)):
                    last_version_try = last_version + "." + str(suffix)
                    temp_link = APP_LIST[selected_app]["download-link"].replace(
                        "<VERSION>", last_version_try
                    )
                    final_status = self.check_redirect(temp_link)

                    if final_status == 200:
                        download_link = temp_link
                        valid_link_found = True
                        break

                if not valid_link_found:
                    print(
                        "Error. Could not find a valid download link for Android Studio. Aborting installation."
                    )
                    continue

            else:
                download_link = APP_LIST[selected_app]["download-link"].replace(
                    "<VERSION>", last_version
                )

            print(f"Downloading {APP_LIST[selected_app]['name']} from {download_link}")
            download_path = os.path.join(
                os.getcwd(),
                "{}-{}.tar.gz".format(APP_LIST[selected_app]["name"], last_version),
            )

            if os.path.exists(download_path):
                print("File already exists. Skipping download.")
            else:
                try:
                    req = requests.get(download_link)
                    assert req.status_code == 200

                    with open(download_path, "wb") as f:
                        f.write(req.content)

                    print(
                        "Successfully downloaded app file to {}".format(download_path)
                    )
                except Exception as e:
                    print(e)

            # Extract file
            print("Extracting file...")
            if not os.path.exists(install_path):
                os.makedirs(install_path)
                try:
                    result = subprocess.call(
                        [
                            "sudo",
                            "tar",
                            "-xzf",
                            download_path,
                            "-C",
                            install_path,
                            "--strip-components=1",
                        ]
                    )
                    assert result != 0
                except Exception as e:
                    print(e)

            # Create desktop entry
            try:
                desktop_entry_path = os.path.join(
                    "/usr/share/applications", "{}.desktop".format(selected_app)
                )

                if os.path.exists(desktop_entry_path):
                    print("Desktop entry already exists. Deleting it.")
                    os.remove(desktop_entry_path)

                with open(desktop_entry_path, "w") as f:
                    f.write("[Desktop Entry]\n")
                    f.write("Name={}\n".format(APP_LIST[selected_app]["help"]))
                    f.write(
                        "Exec={}/bin/{}.sh\n".format(
                            install_path, APP_LIST[selected_app]["executable"]
                        )
                    )
                    f.write(
                        "Icon={}/bin/{}.png\n".format(
                            install_path, APP_LIST[selected_app]["executable"]
                        )
                    )
                    f.write("Terminal=false\n")
                    f.write("Type=Application\n")
                    f.write("Categories=Development;\n")
                    f.write("Comment={}\n".format(APP_LIST[selected_app]["comment"]))

                print(
                    "Successfully created desktop entry at {}".format(
                        desktop_entry_path
                    )
                )
            except Exception as e:
                print(e)

            # Create symlink
            try:
                symlink_path = os.path.join("/usr/local/bin", selected_app)

                if os.path.exists(symlink_path):
                    print("Symlink already exists. Deleting it.")
                    os.remove(symlink_path)

                os.symlink(
                    os.path.join(
                        install_path,
                        "bin",
                        APP_LIST[selected_app]["executable"] + ".sh",
                    ),
                    symlink_path,
                )

                print("Successfully created symlink at {}".format(symlink_path))
            except Exception as e:
                print(e)

            # Chmod +x on executable
            try:
                executable_path = os.path.join(
                    install_path, "bin", APP_LIST[selected_app]["executable"] + ".sh"
                )
                subprocess.call(["sudo", "chmod", "+x", executable_path])
                print(
                    "Successfully set executable permissions on {}".format(
                        executable_path
                    )
                )
            except Exception as e:
                print(e)

            # Remove downloaded file
            try:
                os.remove(download_path)
                print(
                    "Successfully removed downloaded file at {}".format(download_path)
                )
            except Exception as e:
                print(e)

    def check_redirect(self, url, max_redirects=5):
        """Check the final status code after following redirects."""
        for _ in range(max_redirects):
            response = requests.head(url, allow_redirects=False)
            if response.status_code in (301, 302):
                url = response.headers.get("Location")
            else:
                return response.status_code
        return None


if __name__ == "__main__":
    updater = JetbrainsManagerTool
    updater()
