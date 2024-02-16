#!/usr/bin/env python

import shutil
import requests
import argparse
import os
import subprocess
import sys
import xml.etree.ElementTree as elementTree
import json
import logging

__author__ = "Diogo Caveiro"
__date__ = "2024-02-16"
__version__ = "0.4.1"
__github__ = "https://github.com/diogocaveiro"
__license__ = "GPLv3 License"

JETBRAINS_XML_URL = "https://www.jetbrains.com/updates/updates.xml"
ANDROID_STUDIO_XML_URL = "https://dl.google.com/android/studio/patches/updates.xml"
JETBRAINS_INSTALL_PATH = "/opt/jetbrains/"
SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
global args

with open(os.path.join(SCRIPT_DIRECTORY, 'apps_data.json'), 'r') as json_file:
    APP_LIST = json.load(json_file)

OPERATION_FLAGS = {
    "install": [
        "-i",
        "--install",
        "Install mode. Use this flag to install applications.",
        "store_true",
    ],
    "update": [
        "-u",
        "--update",
        "Update mode. Use this flag to update applications.",
        "store_true",
    ],
    "remove": [
        "-r",
        "--remove",
        "Removal mode. Use this flag to remove applications.",
        "store_true",
    ],
    "help": [
        "-h",
        "--help",
        "Displays helpful information.",
        "store_true",
    ],
    "list": [
        "-l",
        "--list",
        "List installed applications.",
        "store_true",
    ],
    "updatedir": [
        "-n",
        "--updatedir",
        "Update the installation path.",
        "store_true",
    ],
}

CONFIGURATION_FLAGS = {
    "directory": [
        "-d",
        "--directory",
        "Set the directory for JetBrains' applications.",
        "store_true",
    ],
    "only_update_data": [
        "-z",
        "--only-update-data",
        "Update application menu and symlinks only.",
        "store_true",
    ],
    "update_mimetypes": [
        "-m",
        "--update-mimetypes",
        "Update mimetypes.",
        "store_true",
    ],
    "no_confirm": [
        "-y",
        "--no-confirm",
        "Do not ask for confirmation.",
        "store_true",
    ],
    "verbose": [
        "-v",
        "--verbose",
        "Verbose mode.",
        "store_true",
    ],
}


def check_redirect(url, max_redirects=5) -> int | None:
    """
    Check the final status code of a URL after potentially following a series of redirects.

    The function uses the HTTP HEAD method to iteratively follow redirects up to a maximum
    specified by `max_redirects`. If the maximum number of redirects is reached without arriving
    at a non-redirect status code, the function returns `None`.

    Parameters:
    - url (str): The initial URL to check.
    - max_redirects (int, optional): The maximum number of redirects to follow. Defaults to 5.

    Returns:
    - int or None: The HTTP status code of the final destination after following redirects. If the
      maximum number of redirects is exceeded, returns `None`.

    Notes:
    - Only 301 and 302 status codes are treated as redirects.
    """

    for _ in range(max_redirects):
        response = requests.head(url, allow_redirects=False)
        if response.status_code in (301, 302):
            url = response.headers.get("Location")
        else:
            return response.status_code
    return None


class JetbrainsManagerTool:
    def __init__(self):
        # Set logging level
        logging.basicConfig(level=logging.DEBUG, filename=os.path.join('/var/log/', 'jetbrains-manager-tool.log'))

        msg_initialize = "Initializing Jetbrains Updater."
        print("\n" + msg_initialize)
        logging.info(msg_initialize)

        # Verbose mode
        self.verbose = True if args.verbose else False

        # Check selected applications
        self.selected_apps = [
            app_key
            for app_key, app_data in APP_LIST.items()
            if getattr(args, app_data["flag"][-1], False)
        ]

        # Check installed applications
        self.__check_installed_apps()

        # Fetch JetBrains XML file
        self.__fetch_xml()

        # Set operation (install, update, remove)
        if args.install:
            if not self.selected_apps:
                msg_no_app_selected = "No app selected. Stopping installer."
                print(msg_no_app_selected)
                logging.info(msg_no_app_selected)
                return
            else:
                self.__install(only_update_data=args.only_update_data, update_mimetypes=args.update_mimetypes,
                               no_confirm=args.no_confirm)
        elif args.update:
            self.__install(update=True, only_update_data=args.only_update_data, update_mimetypes=args.update_mimetypes,
                           no_confirm=args.no_confirm)
        elif args.remove:
            if not self.selected_apps:
                msg_no_app_selected = "No app selected. Stopping installer."
                print(msg_no_app_selected)
                logging.info(msg_no_app_selected)
                return
            else:
                self.__remove(no_confirm=args.no_confirm)

        elif args.list:
            self.__check_installed_apps(list_installed_apps=True)

        print("\nOperation completed successfully.")

    def __check_installed_apps(self, list_installed_apps=False):
        """
        Check and identify installed JetBrains applications along with their versions.

        This method scans a predefined installation directory (specified by JETBRAINS_INSTALL_PATH) for any
        JetBrains applications listed in the APP_LIST. For each detected application, it retrieves the version
        and build number from the 'product-info.json' file located within the application's folder.

        The information about installed applications is stored in the instance variable `self.installed_apps` in the
        form: {<app_key>: [<version>, <build_number>], ...}

        If `list_installed_apps` or verbose flag are set to True, the method prints a list of installed apps and
        their descriptions to the console. If no applications are detected in the installation path, a message is
        printed indicating the absence of installed apps.

        Attributes updated:
        - self.installed_apps (dict): A dictionary mapping app keys to their respective versions and build numbers.
        """

        # Check installed applications
        self.installed_apps = {}
        for key, value in APP_LIST.items():
            install_path = os.path.join(JETBRAINS_INSTALL_PATH, value["folder"])
            if os.path.exists(install_path):
                with open(os.path.join(install_path, 'product-info.json'), 'r') as product_info_json:
                    data = json.load(product_info_json)
                    version = data['version']
                    build_number = data['buildNumber']
                self.installed_apps[key] = [version, build_number]

        # Print result
        if self.installed_apps:
            msg_installed_apps = "The following apps are already installed:\n" \
                                 + "  - " \
                                 + "\n  - ".join([app_content['help'] for app, app_content in APP_LIST.items()
                                                  if app in self.installed_apps.keys()])
            if self.verbose or list_installed_apps:
                print(msg_installed_apps)
        else:
            msg_installed_apps = "No app installed in the designated install folder."
            if self.verbose or list_installed_apps:
                print(msg_installed_apps)

        logging.info(msg_installed_apps)

    def __fetch_xml(self):
        """
        Fetch XML files from JetBrains and Android Studio URLs and combine them.

        This method performs the following tasks:
        1. Fetches the XML file from the JetBrains URL.
        2. Fetches the XML file from the Android Studio URL.
        3. Appends the contents of the Android Studio XML into the JetBrains XML.
        4. Stores the combined XML content into the instance variable `self.xml_file`.

        If any step fails (e.g., the request returns a non-200 status code or parsing issues occur),
        an exception is raised and the error message is printed to the console.

        Note:
        - The URLs JETBRAINS_XML_URL and ANDROID_STUDIO_XML_URL should be set correctly before calling this method.
        - The combined XML content will be stored as a bytes string in the `self.xml_file` attribute.

        Attributes updated:
        - self.xml_file (bytes): Combined XML content from both JetBrains and Android Studio.

        Raises:
        - Various exceptions, including potential HTTP errors and XML parsing errors. Errors are printed to the console.
        """

        try:
            # Fetch Jetbrains XML file
            req_jetbrains = requests.get(JETBRAINS_XML_URL)
            assert req_jetbrains.status_code == 200
            jetbrains_xml = req_jetbrains.content
            msg_fetch_xml = "Successfully fetched Jetbrains XML file."
            if self.verbose:
                print(msg_fetch_xml)
            logging.debug('XML Status code: ' + str(req_jetbrains.status_code))
            logging.info(msg_fetch_xml)

            # Fetch Android Studio XML file
            req_android_studio = requests.get(ANDROID_STUDIO_XML_URL)
            assert req_android_studio.status_code == 200
            android_studio_xml = req_android_studio.content
            msg_fetch_xml_as = "Successfully fetched Android Studio XML file."
            if self.verbose:
                print(msg_fetch_xml_as)
            logging.debug('Android Studio XML Status code: ' + str(req_android_studio.status_code))
            logging.info(msg_fetch_xml_as)

            # Append Android Studio XML to JetBrains XML
            jetbrains_root = elementTree.fromstring(jetbrains_xml)
            android_studio_root = elementTree.fromstring(android_studio_xml)
            for child in android_studio_root:
                jetbrains_root.append(child)

            self.xml_file = elementTree.tostring(jetbrains_root, encoding="utf-8")

            msg_xml_success = "Successfully fetched and combined JetBrains and Android Studio XML files."
            if self.verbose:
                print(msg_xml_success)
            logging.info(msg_xml_success)

        except Exception:
            logging.exception('Exception occurred')

    def __get_current_versions(self, list_of_apps: list):
        """
        Fetch and store the current versions of specified applications from the XML content.

        This method processes the XML content stored in `self.xml_file` to extract the version and build number
        of each application specified in `list_of_apps`. The data is then stored in the `self.app_versions` dictionary.

        The method specifically looks for product entries in the XML and fetches the associated build details.
        For Android Studio, special handling is done to extract the version and build number correctly.

        Parameters:
        - list_of_apps (list): A list of application keys (e.g., ['android-studio', 'pycharm']) for which the
                               versions need to be fetched.

        Attributes updated:
        - self.app_versions (dict): A dictionary mapping application keys to their respective versions
                                    and build numbers in the form: {<app_key>: [<version>, <build_number>], ...}

        Raises:
        - Potential XML parsing errors. If the version data for an application is not found in the XML,
          a message will be printed to the console.
        """

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
                msg_fetch_data_error = "Could not find data for {}.".format(APP_LIST[app]["name"])
                print(msg_fetch_data_error)
                logging.error(msg_fetch_data_error)

    @staticmethod
    def __confirmation_prompt(job: str, app_list: list) -> bool:
        """
        Display a user confirmation prompt for a given job on a list of applications.

        This method constructs a formatted prompt based on the given job ('install', 'remove' and 'update') and
        the names of applications in `app_list`. Depending on the number of applications, the prompt uses
        appropriate conjunctions (like "and") to create a readable message. After constructing the prompt,
        the method requests user confirmation by asking them to enter "YES".

        Parameters:
        - job (str): The action to be confirmed ('install', 'remove', 'update').
        - app_list (list): A list of application keys (e.g., ['android-studio', 'pycharm']) for which the
                           confirmation is being sought.

        Returns:
        - bool: True if the user confirms with "YES", otherwise False.

        Note:
        - The method is case-sensitive and requires the user to enter "YES" in uppercase for confirmation.

        Raises:
        - Potential KeyErrors if an app from app_list doesn't exist in the global APP_LIST.
        """
        match len(app_list):
            case (1):
                app_prompt = APP_LIST[app_list[0]]["help"]
            case (2):
                app_prompt = " and ".join([APP_LIST[app]["help"] for app in app_list])
            case _:
                app_prompt = ", ".join([APP_LIST[app]["help"] for app in app_list[:-1]]) + " and " + \
                             APP_LIST[app_list[-1]]["help"]

        confirmation_question = input(
            "\nAre you sure you want to {} {}? Enter YES for confirmation.\n".format(job, app_prompt)
        )
        if confirmation_question != "YES":
            print(f'Cancelling {job} job.')
            logging.info(f'No confirmation. Cancelling {job}.')
            return False
        return True

    def __install(self, update=False, only_update_data=False, update_mimetypes=False, no_confirm=False):
        """
        Install or update the selected applications.

        The method checks whether an application is outdated or not installed, and based on the specified flags,
        it installs or updates the application accordingly. The application is downloaded from a specified link,
        extracted, and then the desktop entry, symlink, and execution permissions are set up.

        Parameters:
        - update (bool): If set to True, the method will attempt to update the specified applications. Default is False.
        - only_update_data (bool): If set to True, only the data for the applications will be updated without
                                   re-downloading and re-installing them. Default is False.
        - update_mimetypes (bool): If set to True, the method will update the MIME types for the specified applications
                                   in their desktop entry. Default is False.
        - no_confirm (bool): If set to True, the method will not prompt the user for confirmation. Default is False.

        Attributes accessed:
        - self.selected_apps (list): List of application keys selected for installation or update.
        - self.installed_apps (dict): Dictionary mapping installed applications to their versions and build numbers.
        - self.app_versions (dict): Dictionary mapping application keys to their latest versions and build numbers.

        Note:
        - The `JETBRAINS_INSTALL_PATH` constant determines where the applications are installed.

        Raises:
        - Potential OSError, requests.exceptions.RequestException, or other exceptions related to file, directory,
          and web operations. These exceptions are caught and printed to the console.
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
                msg_no_outdated_apps = "All applications are up-to-date."
                print(msg_no_outdated_apps)
                logging.info(msg_no_outdated_apps)
                return

            install_process_apps = outdated_apps

        else:
            self.__get_current_versions(list(self.selected_apps))
            install_process_apps = self.selected_apps

        # Confirmation
        if not no_confirm:
            if not self.__confirmation_prompt("update" if update else "install", install_process_apps):
                return

        # Install process
        for selected_app in install_process_apps:
            msg_install_process = "\n{} {}...".format("Updating" if update else "Installing",
                                                      APP_LIST[selected_app]["name"])
            print(msg_install_process)
            logging.info(msg_install_process)

            # Define install path
            install_path = os.path.join(
                JETBRAINS_INSTALL_PATH, APP_LIST[selected_app]["folder"]
            )

            # Check if app is already installed
            if os.path.exists(install_path) and not update and not only_update_data:
                msg_app_already_installed = (f"{APP_LIST[selected_app]['name']} is already installed. Skipping "
                                             f"installation.")
                print(msg_app_already_installed)
                logging.warning(msg_app_already_installed)
                continue
            elif os.path.exists(install_path) and update and not only_update_data:
                shutil.rmtree(install_path)
                logging.info(f'Removed directory before {"update" if update else "install"}: {install_path}')

            # Download latest version
            if not only_update_data:
                if selected_app == "android-studio":
                    valid_link_found = False
                    for suffix in reversed(range(1, 30)):
                        last_version_try = self.app_versions['android-studio'][0] + "." + str(suffix)
                        temp_link = APP_LIST[selected_app]["download-link"].replace(
                            "<VERSION>", last_version_try
                        )
                        final_status = check_redirect(temp_link)

                        if final_status == 200:
                            download_link = temp_link
                            valid_link_found = True
                            break

                    if not valid_link_found:
                        msg_no_valid_link_as = ("Error. Could not find a valid download link for Android Studio. "
                                                "Aborting installation.")
                        print(msg_no_valid_link_as)
                        logging.error(msg_no_valid_link_as)
                        continue

                else:
                    download_link = APP_LIST[selected_app]["download-link"].replace(
                        "<VERSION>", self.app_versions[selected_app][0]
                    )

                msg_download_app = f"Downloading {APP_LIST[selected_app]['name']} from {download_link}"
                if self.verbose:
                    print(msg_download_app)
                logging.debug(msg_download_app)

                download_path = os.path.join(
                    "/tmp",
                    "{}-{}.tar.gz".format(APP_LIST[selected_app]["name"], self.app_versions[selected_app][0]),
                )

                if os.path.exists(download_path):
                    msg_path_exists = "File already exists. Skipping download."
                    if self.verbose:
                        print(msg_path_exists)
                    logging.warning(msg_path_exists)
                else:
                    try:
                        req = requests.get(download_link)
                        assert req.status_code == 200

                        with open(download_path, "wb") as f:
                            f.write(req.content)

                        msg_download_success = "Successfully downloaded app file."
                        if self.verbose:
                            print(msg_download_success)
                        logging.info(msg_download_success)
                        logging.debug("Successfully downloaded app file to {}".format(download_path))

                    except Exception:
                        logging.exception('Exception occurred')

                # Extract file
                msg_extracting_file = "Extracting file..."
                if self.verbose:
                    print(msg_extracting_file)
                logging.info(msg_extracting_file)

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
                    except Exception:
                        logging.exception('Exception occurred')

            # Create desktop entry
            try:
                desktop_entry_path = os.path.join(
                    "/usr/share/applications", "{}.desktop".format(selected_app)
                )

                if os.path.exists(desktop_entry_path):
                    msg_desktop_entry_exists = "Desktop entry already exists. Deleting it."
                    if self.verbose:
                        print(msg_desktop_entry_exists)
                    os.remove(desktop_entry_path)
                    logging.info(msg_desktop_entry_exists)
                    logging.debug(f'Desktop entry path: {desktop_entry_path}')

                with open(desktop_entry_path, "w") as f:
                    f.write("[Desktop Entry]\n")
                    f.write("Name={}\n".format(APP_LIST[selected_app]["help"]))
                    f.write(
                        "Icon={}/bin/{}.svg\n".format(
                            install_path, APP_LIST[selected_app]["executable"]
                        )
                    )
                    f.write(
                        'Exec="{}/bin/{}.sh" %f\n'.format(
                            install_path, APP_LIST[selected_app]["executable"]
                        )
                    )
                    f.write("Terminal=false\n")
                    f.write("Type=Application\n")
                    f.write("Categories=Development;\n")
                    f.write("StartupWMClass={}\n".format(APP_LIST[selected_app]["wm_class"]))

                    f.write("Comment={}\n".format(APP_LIST[selected_app]["comment"]))

                    # Create mimetypes
                    if APP_LIST[selected_app]["mimetype"] and update_mimetypes:
                        f.write("MimeType=")
                        for mimetype in APP_LIST[selected_app]["mimetype"]:
                            f.write(mimetype + ";")
                        f.write("\n")

                msg_desktop_entry_created = "Successfully created desktop entry at {}".format(desktop_entry_path)
                if self.verbose:
                    print(msg_desktop_entry_created)
                logging.info(msg_desktop_entry_created)
                logging.debug(f'Desktop entry created at {desktop_entry_path}')

            except Exception:
                logging.exception('Exception occurred')

            # Create symlink
            try:
                symlink_path = os.path.join("/usr/local/bin", selected_app)

                if os.path.exists(symlink_path):
                    msg_symlink_exists = "Symlink already exists. Deleting it."
                    if self.verbose:
                        print(msg_symlink_exists)
                    os.remove(symlink_path)
                    logging.info(msg_symlink_exists)
                    logging.debug(f'Deleted existing symlink: {symlink_path}')

                os.symlink(
                    os.path.join(
                        install_path,
                        "bin",
                        APP_LIST[selected_app]["executable"] + ".sh",
                    ),
                    symlink_path,
                )

                msg_symlink_create = "Successfully created symlink"
                if self.verbose:
                    print(msg_symlink_create)
                logging.info(msg_symlink_create)
                logging.debug("Successfully created symlink at {}".format(symlink_path))

            except Exception:
                logging.exception('Exception occurred')

            # Chmod +x on executable
            try:
                executable_path = os.path.join(
                    install_path, "bin", APP_LIST[selected_app]["executable"] + ".sh"
                )
                subprocess.call(["sudo", "chmod", "+x", executable_path])

                msg_executable_permissions = "Successfully set executable permissions"
                if self.verbose:
                    print(msg_executable_permissions)
                logging.info(msg_executable_permissions)
                logging.debug("Successfully set executable permissions on {}".format(executable_path))

            except Exception:
                logging.exception('Exception occurred')

            # Remove downloaded file
            if not only_update_data:
                try:
                    os.remove(download_path)
                    msg_download_remove = "Successfully removed downloaded file."
                    if self.verbose:
                        print(msg_download_remove)
                    logging.info(msg_download_remove)
                    logging.debug("Successfully removed downloaded file at {}".format(download_path))

                except Exception:
                    logging.exception('Exception occurred')

            # Log install/update completion
            logging.info(
                "{} {} completed successfully.".format(
                    APP_LIST[selected_app]["name"],
                    "update" if update else "installation",
                )
            )

    def __remove(self, no_confirm=False):
        """
        Remove the selected applications.

        This method performs the removal of applications that are specified in the `self.selected_apps` attribute.
        Removal involves deleting the installation directory, the associated desktop entry and any symlinks created.

        The method will first prompt the user for confirmation unless the `no_confirm` flag is set to True.
        For each app, it checks if it's already installed, and if so, it proceeds with the removal process.

        Parameters:
        - no_confirm (bool): If set to True, the function will not prompt the user for confirmation before
                             removing apps. Default is False.

        Attributes accessed:
        - self.selected_apps (list): List of application keys selected for removal.
        - self.installed_apps (dict): Dictionary mapping installed applications to their versions and build numbers.

        Note:
        - This method makes use of the `JETBRAINS_INSTALL_PATH` constant to determine where the applications
          are installed.

        Raises:
        - Potential OSError or other exceptions related to file and directory operations.
          These exceptions are caught and printed to the console.
        """

        # Removal confirmation
        if not no_confirm:
            if not self.__confirmation_prompt("remove", self.selected_apps):
                return

        for selected_app in self.selected_apps:
            if selected_app in self.installed_apps.keys():
                msg_removing_app = "Removing {}.".format(APP_LIST[selected_app]["name"])
                print(msg_removing_app + "\n")
                logging.info(msg_removing_app)

                # Remove directory
                try:
                    install_path = os.path.join(JETBRAINS_INSTALL_PATH, APP_LIST[selected_app]["folder"])
                    shutil.rmtree(install_path)
                    msg_removed_directory = "Successfully removed directory."
                    if self.verbose:
                        print(msg_removed_directory)
                    logging.info(msg_removed_directory)
                    logging.debug(f'Removed directory: {install_path}')

                except Exception:
                    logging.exception('Exception occurred')

                # Remove desktop entry
                try:
                    desktop_entry_path = os.path.join(
                        "/usr/share/applications", "{}.desktop".format(selected_app)
                    )

                    if os.path.exists(desktop_entry_path):
                        msg_remove_desktop_entry = "Removing desktop entry."
                        if self.verbose:
                            print(msg_remove_desktop_entry)
                        logging.info(msg_remove_desktop_entry)
                        logging.debug(f'Removing desktop entry at {desktop_entry_path}.')

                        os.remove(desktop_entry_path)

                except Exception:
                    logging.exception('Exception occurred')

                # Remove symlink
                try:
                    symlink_path = os.path.join("/usr/local/bin", selected_app)

                    if os.path.exists(symlink_path):
                        msg_remove_symlink = "Removing symlink."
                        if self.verbose:
                            print(msg_remove_symlink)
                        logging.info(msg_remove_symlink)
                        logging.debug(f"Removing symlink at {symlink_path}")

                        os.remove(symlink_path)

                except Exception:
                    logging.exception('Exception occurred')


def get_arguments_and_flags():
    global args

    # Parse arguments
    arg_parser = argparse.ArgumentParser(add_help=False)
    exclusive_group = arg_parser.add_mutually_exclusive_group(required=True)

    # Operation flags
    for operation in OPERATION_FLAGS.values():
        exclusive_group.add_argument(
            operation[0], operation[1], action=operation[3], help=operation[2]
        )

    # Application flags
    for app in APP_LIST.values():
        arg_parser.add_argument(app["flag"], action="store_true", help=app["help"])

    # Configuration flags/arguments
    for operation in CONFIGURATION_FLAGS.values():
        arg_parser.add_argument(
            operation[0], operation[1], action=operation[3], help=operation[2]
        )

    args = arg_parser.parse_args()

    # Change default directory
    if args.directory and os.path.exists(args.directory):
        global JETBRAINS_INSTALL_PATH
        JETBRAINS_INSTALL_PATH = args.directory
        msg_custom_path = f'Custom path: \"{JETBRAINS_INSTALL_PATH}\".'
        print(msg_custom_path)
        logging.info(msg_custom_path)

        # Create configuration file
        try:
            with open(os.path.join(os.path.expanduser('~'), '.config', 'jetbrains-manager-tool'), 'w') as config_file:
                config_file.write(f'JETBRAINS_INSTALL_PATH={JETBRAINS_INSTALL_PATH}\n')
            logging.debug(
                f'Created configuration file at {os.path.join(os.path.expanduser("~"), ".config", "jetbrains-manager-tool")}')
        except Exception:
            logging.exception('Exception occurred')
    elif args.directory and not os.path.exists(args.directory):
        msg_invalid_path = f'Invalid path: \"{args.directory}\".'
        print(msg_invalid_path)
        logging.error(msg_invalid_path)
        sys.exit(1)
    else:
        if os.path.exists(os.path.join(os.path.expanduser('~'), '.config', 'jetbrains-manager-tool')):
            with open(os.path.join(os.path.expanduser('~'), '.config', 'jetbrains-manager-tool'), 'r') as config_file:
                for line in config_file.readlines():
                    if line.startswith('JETBRAINS_INSTALL_PATH'):
                        JETBRAINS_INSTALL_PATH = line.split('=')[1].strip()
                        msg_custom_path = f'Custom path: \"{JETBRAINS_INSTALL_PATH}\".'
                        print(msg_custom_path)
                        logging.info(msg_custom_path)
                        break


def show_help_documentation():
    """
    Displays the help documentation using the 'less' command.

    This function attempts to open a Markdown file containing help documentation with the 'less' command for easy
    viewing. The documentation file is expected to be located in a 'docs' subdirectory within the script's directory.
    The path to the documentation is constructed using the script's directory path.

    Raises:
        FileNotFoundError: If the 'less' command is not installed or the documentation file does not exist.
        Exception: For any other exceptions that occur when attempting to open the documentation.
    """

    docs_path = os.path.join(SCRIPT_DIRECTORY, 'docs/help_pages.md')

    try:
        subprocess.run(['less', docs_path], shell=False)

    except FileNotFoundError:
        print(f"Unable to open documentation. Make sure 'less' is installed and the documentation file exists "
              f"at {docs_path}")

    except Exception:
        print('Error opening documentation.')


def request_root_permissions():
    """
    Ensure the script is run with root permissions.

    This function checks if the current process has root permissions. If not, it attempts to
    re-run the script using sudo to gain elevated permissions. If the subprocess fails for any reason,
    the script will exit with an error code.

    Raises:
    - SystemExit: This function will exit the script either with an error code (1) if the subprocess fails,
                  or normally (0) if the subprocess succeeds.
    """

    if os.geteuid() != 0:
        print("This script requires root permissions. Please enter your password.")
        ret = subprocess.call(["sudo", sys.executable] + sys.argv, shell=False)
        if ret != 0:
            sys.exit(1)
        sys.exit(0)


if __name__ == "__main__":
    # Get arguments and flags
    try:
        get_arguments_and_flags()
    except Exception:
        logging.exception('Exception occurred')
        print("Error parsing arguments. Stopping script.")
        sys.exit(1)

    # Display help documentation
    if args.help:
        show_help_documentation()
        sys.exit(0)

    if args.updatedir:
        update_path = input("Enter the new install path: ")
        if os.path.exists(update_path):
            with open(os.path.join(os.path.expanduser('~'), '.config', 'jetbrains-manager-tool'), 'w') as config_file:
                config_file.write(f'JETBRAINS_INSTALL_PATH={update_path}\n')
        else:
            print(f'Invalid path: \"{update_path}\".')
            logging.error(f'Invalid path: \"{update_path}\".')
            sys.exit(1)
        sys.exit(0)

    try:
        # Request root permissions
        request_root_permissions()

        # Run script
        managertool = JetbrainsManagerTool
        managertool()
    except KeyboardInterrupt:
        print("\n\nKeyboardInterrupt. Stopping script.")
        logging.info("KeyboardInterrupt. Stopping script.")
        sys.exit(1)
    except Exception:
        print("\n\nException occurred. Stopping script.")
        logging.exception('Exception occurred')
        sys.exit(1)
