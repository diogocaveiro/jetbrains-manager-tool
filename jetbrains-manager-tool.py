#!/usr/bin/env python3

"""
    TODO:
        - Change default path
        - Update mimeapps.list
        - Remove/Install/Update flags logic
    REQUIRES TESTING:
        - Update all / selected apps
"""
import shutil

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

with open('apps_data.json', 'r') as json_file:
    APP_LIST = json.load(json_file)


def check_redirect(url, max_redirects=5):
    """Check the final status code after following redirects."""
    for _ in range(max_redirects):
        response = requests.head(url, allow_redirects=False)
        if response.status_code in (301, 302):
            url = response.headers.get("Location")
        else:
            return response.status_code
    return None


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
        arg_parser.add_argument(
            "-r", "--remove", action="store_true", help="Removal mode."
        )
        for app in APP_LIST.values():
            arg_parser.add_argument(app["flag"], action="store_true", help=app["help"])
        args = arg_parser.parse_args()

        if args.update and args.install:
            print("Error: You can only use either update or install flags.")
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

        # Remove mode
        if args.remove:
            if not self.selected_apps:
                print("No app selected. Stopping installer.")
                return
            else:
                self.__remove()

    def __check_installed_apps(self):
        """
        Checks installed applications and its versions.
        """
        # Check installed applications
        self.installed_apps = {}
        for key, value in APP_LIST.items():
            install_path = os.path.join(JETBRAINS_INSTALL_PATH, value["folder"])
            if os.path.exists(install_path):
                with open(os.path.join(install_path, 'product-info.json'), 'r') as json_file:
                    data = json.load(json_file)
                    version = data['version']
                    build_number = data['buildNumber']
                self.installed_apps[key] = [version, build_number]

        # Print result
        if self.installed_apps:
            print(
                "The following apps are already installed:\n"
                + "  - "
                + "\n  - ".join(
                    [app_content['help'] for app, app_content in APP_LIST.items() if app in self.installed_apps.keys()])
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

    def __get_current_versions(self, list_of_apps: list):

        root = elementTree.fromstring(self.xml_file)
        self.app_versions = {}

        for app in list_of_apps:
            version_query = "./product[@name='{}']/channel[@name='{}']/build".format(
                APP_LIST[app]["name"], APP_LIST[app]["channel_name"]
            )
            version_elements = root.findall(version_query)

            if version_elements:
                last_version = version_elements[0].get("version")

                if app == "android-studio":
                    last_version = last_version.split(" ")[2]
                    build_number = version_elements[0].get("number")[3:]
                else:
                    build_number = version_elements[0].get("fullNumber")

                self.app_versions[app] = [last_version, build_number]

            else:
                print(
                    "It was not possible to find data for {}".format(APP_LIST[app]["name"])
                )

    def __install(self, update=False, only_update_data=True):
        """
        Installs selected apps.
        Updates selected or all installed apps.
        """

        # Check outdated applications
        if update:
            outdated_apps = []
            self.__get_current_versions(list(self.installed_apps.keys()))

            for installed_app, version_data in self.installed_apps.items():
                if version_data[1] != self.app_versions[installed_app][1]:
                    if not self.selected_apps or installed_app in self.selected_apps:
                        outdated_apps.append(installed_app)

            if not outdated_apps:
                print("All applications are up-to-date.")
                return

            install_process_apps = outdated_apps

        else:
            self.__get_current_versions(list(self.selected_apps))
            install_process_apps = self.selected_apps

        # Install process
        for selected_app in install_process_apps:
            print("\n{} {}...".format("Updating" if update else "Installing", APP_LIST[selected_app]["name"]))

            # Define install path
            install_path = os.path.join(
                JETBRAINS_INSTALL_PATH, APP_LIST[selected_app]["folder"]
            )

            # Check if app is already installed
            if os.path.exists(install_path) and not update and not only_update_data:
                print(
                    f"{APP_LIST[selected_app]['name']} is already installed. Skipping installation."
                )
                continue
            elif os.path.exists(install_path) and update and not only_update_data:
                shutil.rmtree(install_path)

            # Download latest version
            if not only_update_data:
                if selected_app == "android-studio":
                    valid_link_found = False
                    for suffix in reversed(range(1, 30)):
                        last_version_try = self.app_versions['android_studio'][0] + "." + str(suffix)
                        temp_link = APP_LIST[selected_app]["download-link"].replace(
                            "<VERSION>", last_version_try
                        )
                        final_status = check_redirect(temp_link)

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
                        "<VERSION>", self.app_versions[selected_app][0]
                    )

                print(f"Downloading {APP_LIST[selected_app]['name']} from {download_link}")
                download_path = os.path.join(
                    os.getcwd(),
                    "{}-{}.tar.gz".format(APP_LIST[selected_app]["name"], self.app_versions[selected_app][0]),
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
                    f.write("StartupWMClass={}\n".format(APP_LIST[selected_app]["wm_class"]))

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
            if not only_update_data:
                try:
                    os.remove(download_path)
                    print(
                        "Successfully removed downloaded file at {}".format(download_path)
                    )
                except Exception as e:
                    print(e)

    def __remove(self):
        """Removes selected apps."""

        for selected_app in self.selected_apps:
            if selected_app in self.installed_apps.keys():
                # Removal confirmation
                confirmation_question = input("\nAre you sure you want to remove {}? Enter YES for confirmation.\n".format(APP_LIST[selected_app]["name"]))
                if confirmation_question != 'YES':
                    print("Cancelling removal.")
                    return

                print("Removing {}...".format(APP_LIST[selected_app]["name"]))

                # Remove directory
                try:
                    install_path = os.path.join(JETBRAINS_INSTALL_PATH, APP_LIST[selected_app]["folder"])
                    print(install_path)

                except Exception as e:
                    print(e)

                # Remove desktop entry
                try:
                    desktop_entry_path = os.path.join(
                        "/usr/share/applications", "{}.desktop".format(selected_app)
                    )

                    if os.path.exists(desktop_entry_path):
                        print("Removing desktop entry.")
                        os.remove(desktop_entry_path)

                except Exception as e:
                    print(e)

                # Remove symlink
                try:
                    symlink_path = os.path.join("/usr/local/bin", selected_app)

                    if os.path.exists(symlink_path):
                        print("Removing symlink.")
                        os.remove(symlink_path)

                except Exception as e:
                    print(e)


if __name__ == "__main__":
    updater = JetbrainsManagerTool
    up