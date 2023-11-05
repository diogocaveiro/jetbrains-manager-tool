# JetBrains Manager Tool

This tool provides a streamlined process for the installation, update, and removal of various JetBrains applications.
  
## Usage

### Installation

**Install Specific JetBrains Applications**:  
Use the `-i` or `--install` flag followed by the flags for the applications you wish to install.  
Example:  
   ```bash
   ./jetbrains-manager-tool.py -i -p -j
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
**Remove Specific JetBrains Applications**:  
Use the `-r` or `--remove` flag followed by the flags of the applications you wish to remove.  
Example:  
   ```bash
   ./jetbrains-manager-tool.py -r -p -d
   ```
This command will remove PyCharm Professional and DataGrip.
  
## Flags

### Operation Flags (Choose one)

| Operation | Short Flag | Long Flag                | Description                                  |
|:----------|:----------:|:-------------------------|:---------------------------------------------|
| Install   |    `-i`    | `--install`              | Install selected JetBrains applications.     |
| Update    |    `-u`    | `--update`               | Update all installed JetBrains applications. |
| Remove    |    `-r`    | `--remove`               | Remove selected JetBrains applications.      |

### Application Flags

| Application               | Short Flag | Long Flag                | Description                                               |
|:--------------------------|:----------:|:-------------------------|:----------------------------------------------------------|
| Android Studio            |    `-A`    | `--android-studio`       | An IDE for Android app development.                       |
| AppCode                   |    `-O`    | `--appcode`              | Smart IDE for iOS/macOS development.                      |
| AquaCode                  |    `-Q`    | `--aquacode`             | A powerful IDE for test automation.                       |
| CLion                     |    `-C`    | `--clion`                | A cross-platform IDE for C and C++.                       |
| DataGrip                  |    `-S`    | `--datagrip`             | Your Swiss Army Knife for Databases and SQL.              |
| DataSpell                 |    `-D`    | `--dataspell`            | The data science IDE.                                     |
| GoLand                    |    `-G`    | `--goland`               | A Clever IDE to Go.                                       |
| IntelliJ IDEA Community   |    `-I`    | `--intellij-community`   | The IDE for pure Java and Kotlin development.             |
| IntelliJ IDEA Ultimate    |    `-U`    | `--intellij-ultimate`    | The Leading Java and Kotlin IDE                           |
| PhpStorm                  |    `-H`    | `--phpstorm`             | The Lightning-Smart IDE for PHP Programming by JetBrains. |
| PyCharm Community         |    `-P`    | `--pycharm-community`    | The Python IDE for Professional Developers.               |
| PyCharm Edu               |    `-E`    | `--pycharm-edu`          | The Python IDE for Professional Developers.               |
| PyCharm Professional      |    `-Y`    | `--pycharm-professional` | The full stack Python IDE.                                |
| Rider                     |    `-M`    | `--rider`                | Cross-platform .NET IDE based on IntelliJ and ReSharper.  |
| RubyMine                  |    `-B`    | `--rubymine`             | The Most Intelligent Ruby and Rails IDE.                  |
| RustRover                 |    `-R`    | `--rustrover`            | The IDE for Rust.                                         |
| WebStorm                  |    `-W`    | `--webstorm`             | The Smartest JavaScript IDE.                              |

### Configuration Flags

| Configuration     | Short Flag | Long Flag            | Description                                                         |
|:------------------|:----------:|:---------------------|:--------------------------------------------------------------------|
| Only update data  |    `-z`    | `--only-update-data` | Update application menu and symlinks only.                          |
| Update mimetypes  |    `-v`    | `--update-mimetypes` | Update application mimetypes.                                       |
| No confirm        |    `-y`    | `--no-confirm`       | Do not ask for confirmation.                                        |


### Configuration Arguments
| Configuration     |    Short Flag    | Long Flag                 | Description                                                |
|:------------------|:----------------:|:--------------------------|:-----------------------------------------------------------|
| Install directory | `-d [directory]` | `--directory [directory]` | Set custom directory.                                      |


## Disclaimer of Liability

The software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.
  
## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.
  
## No Affiliation
  
This software is an independent project and has not been authorized, sponsored, or otherwise approved by JetBrains. All product names, logos, and brands are property of their respective owners. All company, product, and service names used in this software are for identification purposes only. Use of these names, logos, and brands does not imply endorsement.
