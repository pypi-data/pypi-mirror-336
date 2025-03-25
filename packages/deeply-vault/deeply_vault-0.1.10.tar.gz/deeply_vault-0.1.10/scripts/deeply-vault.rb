class DeeplyVault < Formula
  include Language::Python::Virtualenv

  desc "Deeply Vault CLI tool for managing environment variables"
  homepage "https://github.com/deeply/deeply-vault"
  url "https://github.com/deeply/deeply-vault/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "YOUR_SHA256_HERE"  # 실제 SHA256 값으로 업데이트 필요

  depends_on "python@3.8"

  resource "click" do
    url "https://files.pythonhosted.org/packages/00/2e/d53fa4befbf2cfa713304affc7ca780f4bada3d6b5d6d6c3c1c5c0c0c0c0/click-8.1.7.tar.gz"
    sha256 "ca9853ad459e787e2192211578cc907e7594e294c7ccc834310722b41b9ca6de"
  end

  resource "requests" do
    url "https://files.pythonhosted.org/packages/9d/be/10918a2eac4ae9f02f6cfe6419b7bc055d031d1297a849b5d3e6f78b204c/requests-2.31.0.tar.gz"
    sha256 "942c5a404f8b07d1ba87304ac11e9c4318c8d604e50e0dac73033a4e6b5caa2e"
  end

  resource "rich" do
    url "https://files.pythonhosted.org/packages/11/23/814edf09ec7240ed1202a6ae9568ea91d3c4091c90ef8b0f0c9a92b039ee/rich-13.7.0.tar.gz"
    sha256 "bd2b367b2158d9fd67f0a4b1467a8e3c42f54b72629fb918691f2b5bbd82f1c"
  end

  resource "pyyaml" do
    url "https://files.pythonhosted.org/packages/cd/e5/aafb57811e3e81d69d43f23a8c7c1a9c4cc19f93183d726d457e82854657/PyYAML-6.0.1.tar.gz"
    sha256 "bfdf460b1736c775f2ba9f6a92bca30bc2095067b8a9d77876d1fad6cc3b4a43"
  end

  resource "cryptography" do
    url "https://files.pythonhosted.org/packages/8e/5d/2bf54672898375d081cb24b30baeb7793568ae5b68d04589d0ad0d2a2b6/cryptography-42.0.2.tar.gz"
    sha256 "8f79b5ff369374426080f95f9c4aae074330e32f1c635a80c378f7c94f7503e1"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/deeply-vault", "--help"
  end
end 