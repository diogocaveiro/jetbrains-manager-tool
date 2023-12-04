pkgname='jetbrains-manager-tool'
pkgver=0.3.0
pkgrel=1
pkgdesc="JetBrains Manager Tool provides a streamlined process for the installation, update, and removal of various JetBrains applications."
arch=('any')
url='https://github.com/diogocaveiro/jetbrains-manager-tool'
license=('GPL-3.0-only')
depends=('python' 'python-requests' 'python-poetry' 'less')
source=("jetbrains-manager-tool_V$pkgver.tar.gz")
sha256sums=('01d6e7b4109eecb13f7c3162ddc42f682e72a0ab9100f95554da304f5b020125')

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
  install -d "$pkgdir/usr/share/jetbrains-manager-tool/docs/"
  install -Dm644 jetbrains-manager-tool/docs/help_docs.md "$pkgdir/usr/share/jetbrains-manager-tool/docs/help_docs.md"

  # Symbolic Link
  mkdir -p "$pkgdir/usr/bin"
  ln -s "/usr/share/jetbrains-manager-tool/jetbrains-manager-tool.py" "$pkgdir/usr/bin/jetbrains-manager-tool"

  # License and README
  install -d "$pkgdir/usr/share/doc/$pkgname/"
  install -Dm644 LICENSE "$pkgdir/usr/share/doc/$pkgname/LICENSE"
  install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
}
