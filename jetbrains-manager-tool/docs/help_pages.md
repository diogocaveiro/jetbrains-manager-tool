JetBrains Manager Tool 0.4.1 (2024-02-26)

Usage: jetbrains-manager-tool [OPTIONS]

This tool provides a streamlined process for the installation, update, and removal of various JetBrains applications.

Options:
  -i, --install
    Install selected JetBrains applications. Use application flags to specify which applications to install.
    Example: jetbrains-manager-tool -i -P -S

  -u, --update
    Update all installed JetBrains applications. Does not require specification of individual applications.
    Example: jetbrains-manager-tool -u

  -r, --remove
    Remove selected JetBrains applications. Use application flags to specify which applications to remove.
    Example: jetbrains-manager-tool -r -P -S

  -l, --list
    Lists all installed Jetbrains applications.
    Example: jetbrains-manager-tool -l

  -h, --help
    Displays the help documentation.
    Example: jetbrains-manager-tool -h

  -l, --list
    List installed JetBrains applications.
    Example: ./jetbrains-manager-tool.py -l

  -n, --updatedir
    Update install directory in the configuration file.
    Example: ./jetbrains-manager-tool.py -n /custom/path

Application Flags:
  -A, --android-studio       Install or remove Android Studio.
  -O, --appcode              Install or remove AppCode.
  -Q, --aquacode             Install or remove AquaCode.
  -C, --clion                Install or remove CLion.
  -S, --datagrip             Install or remove DataGrip.
  -D, --dataspell            Install or remove DataSpell.
  -G, --goland               Install or remove GoLand.
  -I, --intellij-community   Install or remove IntelliJ IDEA Community.
  -U, --intellij-ultimate    Install or remove IntelliJ IDEA Ultimate.
  -H, --phpstorm             Install or remove PhpStorm.
  -P, --pycharm-community    Install or remove PyCharm Community.
  -E, --pycharm-edu          Install or remove PyCharm Edu.
  -Y, --pycharm-professional Install or remove PyCharm Professional.
  -M, --rider                Install or remove Rider.
  -B, --rubymine             Install or remove RubyMine.
  -R, --rustrover            Install or remove RustRover.
  -W, --webstorm             Install or remove WebStorm.

Configuration Flags:
  -z, --only-update-data    Update application menu and symlinks only.
  -m, --update-mimetypes    Update application mimetypes.
  -y, --no-confirm          Do not ask for confirmation during operations.
  -v, --verbose             Increase verbosity of output.

Configuration Arguments:
  -d [directory], --directory [directory]
    Set custom installation directory.
    Example: jetbrains-manager-tool -i -P -d /custom/path

Disclaimer:
  This software is provided "as is", without warranty of any kind. Not affiliated with JetBrains.

For more information, visit https://github.com/diogocaveiro/jetbrains-manager-tool
