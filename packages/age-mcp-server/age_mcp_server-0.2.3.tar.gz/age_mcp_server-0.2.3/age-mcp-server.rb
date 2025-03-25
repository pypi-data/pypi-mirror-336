class AgeMcpServer < Formula
  include Language::Python::Virtualenv

  desc "Apache AGE MCP Server"
  homepage "https://github.com/rioriost/homebrew-age-mcp-server/"
  url "https://files.pythonhosted.org/packages/d4/5f/c18b10cb3f30c4febcd0cde47067634b12bfd6674971e831b33fc7fbb7b0/age_mcp_server-0.2.2.tar.gz"
  sha256 "70d2ba963b6b918b35124cbd16d166c49544999e57781475250f4a1090e233f3"
  license "MIT"

  depends_on "python@3.13"

  resource "agefreighter" do
    url "https://files.pythonhosted.org/packages/9a/71/d31b5178dd104e620ef70d8e9d54b04312ed26a28273167af13ecb446e3c/agefreighter-1.0.2.tar.gz"
    sha256 "c1165229f9d0d938866a8d88ffc6ff9d221c80e22cb16aea8432e4119515e4e6"
  end

  resource "ply" do
    url "https://files.pythonhosted.org/packages/e5/69/882ee5c9d017149285cab114ebeab373308ef0f874fcdac9beb90e0ac4da/ply-3.11.tar.gz"
    sha256 "00c7c1aaa88358b9c765b6d3000c6eec0ba42abca5351b095321aef446081da3"
  end

  def install
    virtualenv_install_with_resources
    system libexec/"bin/python", "-m", "pip", "install", "psycopg[binary,pool]", "mcp"
  end

  test do
    system "#{bin}/age-mcp-server", "--help"
  end
end
