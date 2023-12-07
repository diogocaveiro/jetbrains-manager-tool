pkgname='jetbrains-manager-tool'
pkgver=PACKAGE_VERSION
pkgrel=1
pkgdesc="JetBrains Manager Tool provides a streamlined process for the installation, update, and removal of various JetBrains applications."
checksum=PACKAGE_CHECKSUM
arch=('any')
url='https://github.com/diogocaveiro/jetbrains-manager-tool'
license=('GPL-3.0-only')
depends=('python' 'python-requests' 'python-poetry' 'less')
source=("jetbrains-manager-tool_V$pkgver.tar.gz")
sha256sums=("${checksum}")

build() {
  cd "$srcdir"
  poetry build
}

package() {
  # Install
  cd "$srcdir"
  install -d "$pkgdir/usr/share/jetbrains-manager-tool/"
  install -Dm555 jetbrains-manager-tool/jetbrains-manager-tool.py "$pkgdir/usr/share/jetbrains-manager-tool/jetbrains-manager-tool.py"
  install -Dm444 jetbrains-manager-tool/apps_data.json "$pkgdir/usr/share/jetbrains-manager-tool/apps_data.json"
  install -d "$pkgdir/usr/share/jetbrains-manager-tool/docs/"
  install -Dm444 jetbrains-manager-tool/docs/help_docs.md "$pkgdir/usr/share/jetbrains-manager-tool/docs/help_docs.md"

  # Symbolic Link
  mkdir -p "$pkgdir/usr/bin"
  ln -s "/usr/share/jetbrains-manager-tool/jetbrains-manager-tool.py" "$pkgdir/usr/bin/jetbrains-manager-tool"

  # Alias as jmtools

  # License and README
  install -d "$pkgdir/usr/share/doc/$pkgname/"
  install -Dm444 LICENSE "$pkgdir/usr/share/doc/$pkgname/LICENSE"
  install -Dm444 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
}
