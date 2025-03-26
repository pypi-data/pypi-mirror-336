# Install git lfs
git lfs fetch --all
git lfs pull

# Install
# Check if AISI_PLATFORM_USER is set to see if this is an internal AISI user
if [ -z "${AISI_PLATFORM_USER}" ]; then
  uv sync --dev --all-extras
else
  uv sync --dev --all-extras --group aisi-internal
fi

# Install pre-commit
pipx install pre-commit
pre-commit install

# CLI support
pipx install poethepoet

# Install kind. For some reason the kind feature I tried didn't work, so just installing the binaries here
# From https://kind.sigs.k8s.io/docs/user/quick-start/#installing-from-release-binaries
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.27.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Install AWS CLI v2
if ! command -v aws &> /dev/null || ! aws --version | grep -q "aws-cli/2"; then
  echo "Installing AWS CLI v2..."
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip -q awscliv2.zip
  sudo ./aws/install
  rm -rf aws awscliv2.zip
  echo "AWS CLI v2 installed successfully"
fi

# Add sourcing of /etc/environment to shell config files if it doesn't already exist
if ! grep -q "source /etc/environment" ~/.bashrc; then
  echo 'if [ -f /etc/environment ]; then set -a; source /etc/environment; set +a; fi' >> ~/.bashrc
fi

if ! grep -q "source /etc/environment" ~/.zshrc; then
  echo 'if [ -f /etc/environment ]; then set -a; source /etc/environment; set +a; fi' >> ~/.zshrc
fi
