pkgname='jetbrains-manager-tool'
pkgver=0.1
pkgrel=1
pkgdesc="JetBrains Manager Tool provides a streamlined process for the installation, update, and removal of various JetBrains applications."
arch=('any')
url='https://github.com/diogocaveiro/jetbrains-manager-tool'
license=('GPL-3.0-only')
depends=('python' 'python-requests' 'python-poetry')
source=("jetbrains-manager-tool_V0.1.tar.gz")
sha256sums=('f160480933ef45ab50a0a7f19dc972fa7c04e5205366fadeaa45bc242b4809b4')

build() {
  cd "$srcdir"
  poetry build
}

package() {
  # Install
  cd "$srcdir"
  install -d "$pkgdir/usr/share/jetbrains-manager-tool/"
  install -Dm755 jetbrains-manager-tool/jetbrains-manager-tool.py "$pkgdir/usr/share/jetbrains-manager-tool/jetbrains-manager-tool.py"
  install -Dm644 jetbrains-manager-tool/apps_data.json "$pkgdir/usr/share/jetbrains-manager-tool/apps_data.json"

  # Symbolic Link
  mkdir -p "$pkgdir/usr/bin"
  ln -s "/usr/share/jetbrains-manager-tool/jetbrains-manager-tool.py" "$pkgdir/usr/bin/jetbrains-manager-tool"

  # License and README
  install -d "$pkgdir/usr/share/doc/$pkgname/"
  install -Dm644 LICENSE "$pkgdir/usr/share/doc/$pkgname/LICENSE"
  install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
}