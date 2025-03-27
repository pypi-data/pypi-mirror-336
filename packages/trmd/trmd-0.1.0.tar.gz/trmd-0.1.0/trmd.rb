class Trmd < Formula
  include Language::Python::Virtualenv

  desc "Translate Markdown using OpenAI"
  homepage "https://github.com/rioriost/homebrew-trmd/"
  url "https://files.pythonhosted.org/packages/c0/54/42a9591a339d82cf5bfe6dd8bf23472208dc92e16f305f291529742150af/parasync-0.1.1.tar.gz"
  sha256 "113d5d5b98de60faadf0a7e43c0afeb785679ee07d23ad93b2e5cd9741ad0977"
  license "MIT"

  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources
    system libexec/"bin/python", "-m", "pip", "install", "openai"
  end

  test do
    system "#{bin}/trmd", "--help"
  end
end
