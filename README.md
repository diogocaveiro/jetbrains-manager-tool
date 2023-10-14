# JetBrains Manager Tool

This tool allows for the streamlined installation of various JetBrains applications. Below is a guide to each application and its associated flags.

## Usage

### Installation

**Install Specific JetBrains Applications**:  
Use the `-i` or `--install` flag followed by the flags for the applications you wish to install.  
Example:  
   ```bash
   ./jetbrains-manager-tool.py -i -p -d
   ```
This will install PyCharm Professional and DataGrip.

### Update

**Update All Installed JetBrains Applications**:
Simply use the `-u` or `--update` flag. You don't need to specify individual applications.
Example:
   ```bash
   ./jetbrains-manager-tool.py -u
   ```

### Removal
**Uninstall Specific JetBrains Applications**:
Use the `-r` or `--remove` flag followed by the flags of the applications you wish to uninstall.
Example:
   ```bash
   ./jetbrains-manager-tool.py -r -p -d
   ```
This command will uninstall PyCharm Professional and DataGrip.

## Flags

### Operation Flags

| Operation                 | Short Flag | Long Flag                | Description                                               |
|:--------------------------|:----------:|:-------------------------|:----------------------------------------------------------|
| Install                   | `-i`       | `--install`              | Install selected JetBrains applications.                  |
| Update                    | `-u`       | `--update`               | Update all installed JetBrains applications.               |
| Uninstall                 | `-r`       | `--remove`               | Uninstall selected JetBrains applications.                |

### Application Flags

| Application               | Short Flag | Long Flag                | Description                                               |
|:--------------------------|:----------:|:-------------------------|:----------------------------------------------------------|
| PyCharm Professional      | `-p`       | `--pycharm`              | The full stack Python IDE.                                |
| CLion                     | `-c`       | `--clion`                | A cross-platform IDE for C and C++.                       |
| DataGrip                  | `-d`       | `--datagrip`             | Your Swiss Army Knife for Databases and SQL.              |
| GoLand                    | `-g`       | `--goland`               | A Clever IDE to Go.                                       |
| IntelliJ IDEA Community   | `-n`       | `--intellij-community`   | Capable and Ergonomic IDE for JVM.                        |
| IntelliJ IDEA Ultimate    | `-m`       | `--intellij-ultimate`    | Capable and Ergonomic IDE for JVM.                        |
| PhpStorm                  | `-k`       | `--phpstorm`             | The Lightning-Smart IDE for PHP Programming by JetBrains. |
| PyCharm Community         | `-y`       | `--pycharm-community`    | The Python IDE for Professional Developers.               |
| PyCharm Edu               | `-e`       | `--pycharm-edu`          | The Python IDE for Professional Developers.               |
| Rider                     | `-x`       | `--rider`                | Cross-platform .NET IDE based on IntelliJ and ReSharper.  |
| RubyMine                  | `-b`       | `--rubymine`             | The Most Intelligent Ruby and Rails IDE.                  |
| WebStorm                  | `-w`       | `--webstorm`             | The Smartest JavaScript IDE.                              |
| AppCode                   | `-a`       | `--appcode`              | Smart IDE for iOS/macOS development.                      |
| AquaCode                  | `-q`       | `--aquacode`             | A powerful IDE for test automation.                       |
| DataSpell                 | `-s`       | `--dataspell`            | The data science IDE.                                     |
| RustRover                 | `-o`       | `--rustrover`            | The IDE for Rust.                                         |

