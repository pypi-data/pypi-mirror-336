{
  description = "NixMCP - Model Context Protocol server for NixOS resources";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    devshell.url = "github:numtide/devshell";
  };

  outputs = { self, nixpkgs, flake-utils, devshell }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # Configuration variables
        pythonVersion = "311";
        
        # Import nixpkgs with overlays
        pkgs = import nixpkgs { 
          inherit system; 
          overlays = [ 
            devshell.overlays.default
          ];
        };
        
        # Create a Python environment with base dependencies
        python = pkgs."python${pythonVersion}";
        pythonEnv = python.withPackages (ps: with ps; [
          pip
          setuptools
          wheel
          # Note: venv is built into Python, not a separate package
        ]);
        
        # Create a reusable uv installer derivation
        uvInstaller = pkgs.stdenv.mkDerivation {
          name = "uv-installer";
          buildInputs = [];
          unpackPhase = "true";
          installPhase = ''
            mkdir -p $out/bin
            echo '#!/usr/bin/env bash' > $out/bin/install-uv
            echo 'if ! command -v uv >/dev/null 2>&1; then' >> $out/bin/install-uv
            echo '  echo "Installing uv for faster Python package management..."' >> $out/bin/install-uv
            echo '  curl -LsSf https://astral.sh/uv/install.sh | sh' >> $out/bin/install-uv
            echo 'else' >> $out/bin/install-uv
            echo '  echo "uv is already installed."' >> $out/bin/install-uv
            echo 'fi' >> $out/bin/install-uv
            chmod +x $out/bin/install-uv
          '';
        };
        
        # Unified venv setup function
        setupVenvScript = ''
          if [ ! -d .venv ]; then
            echo "Creating Python virtual environment..."
            ${pythonEnv}/bin/python -m venv .venv
            source .venv/bin/activate
            
            # Ensure pip is installed and up-to-date in the venv
            echo "Ensuring pip is installed and up-to-date..."
            python -m ensurepip --upgrade
            python -m pip install --upgrade pip setuptools wheel
            
            # Check if uv is available and use it, otherwise fall back to pip
            if command -v uv >/dev/null 2>&1; then
              echo "Using uv to install dependencies..."
              uv pip install -r requirements.txt
            else
              echo "Using pip to install dependencies..."
              python -m pip install -r requirements.txt
            fi
          else
            source .venv/bin/activate
            # Verify pip is using the venv version
            VENV_PIP="$(which pip)"
            if [[ "$VENV_PIP" != *".venv/bin/pip"* ]]; then
              echo "Warning: Not using virtual environment pip. Fixing PATH..."
              export PATH="$PWD/.venv/bin:$PATH"
            fi
          fi
        '';

      in {
        # DevShell implementations
        devShells = {
          # Use devshell as default for better developer experience
          default = pkgs.devshell.mkShell {
            name = "nixmcp";
            
            # Better prompt appearance
            motd = ''
              NixMCP Dev Environment - Model Context Protocol for NixOS resources
            '';
            
            # Environment variables
            env = [
              { name = "PYTHONPATH"; value = "."; }
              { name = "NIXMCP_ENV"; value = "development"; }
              { name = "PS1"; value = "\\[\\e[1;36m\\][nixmcp]\\[\\e[0m\\]$ "; }
              # Ensure Python uses the virtual environment
              { name = "VIRTUAL_ENV"; eval = "$PWD/.venv"; }
              { name = "PATH"; eval = "$PWD/.venv/bin:$PATH"; }
            ];
            
            packages = with pkgs; [
              # Python environment
              pythonEnv
              
              # Required Nix tools
              nix
              nixos-option
              
              # Development tools
              black
              (pkgs."python${pythonVersion}Packages".pytest)
              
              # uv installer tool
              uvInstaller
            ];
            
            # Startup commands
            commands = [
              {
                name = "setup";
                category = "development";
                help = "Set up Python environment and install dependencies";
                command = ''
                  echo "Setting up Python virtual environment..."
                  ${setupVenvScript}
                  echo "✓ Setup complete!"
                '';
              }
              {
                name = "setup-uv";
                category = "development";
                help = "Install uv for faster Python package management";
                command = ''
                  if ! command -v uv >/dev/null 2>&1; then
                    echo "Installing uv for faster Python package management..."
                    curl -LsSf https://astral.sh/uv/install.sh | sh
                    echo "✓ uv installed successfully!"
                    echo "Run 'setup' again to use uv for dependency installation"
                  else
                    echo "✓ uv is already installed"
                  fi
                '';
              }
              {
                name = "run";
                category = "server";
                help = "Run the NixMCP server";
                command = ''
                  echo "Starting NixMCP server..."
                  source .venv/bin/activate
                  
                  # Verify pip is using the venv version
                  VENV_PIP="$(which pip)"
                  if [[ "$VENV_PIP" != *".venv/bin/pip"* ]]; then
                    echo "Warning: Not using virtual environment pip. Fixing PATH..."
                    export PATH="$PWD/.venv/bin:$PATH"
                  fi
                  
                  python server.py
                '';
              }
              {
                name = "run-tests";
                category = "testing";
                help = "Run tests with coverage report";
                command = ''
                  echo "Running tests with coverage..."
                  source .venv/bin/activate
                  
                  # Ensure pytest and pytest-cov are installed
                  NEED_INSTALL=0
                  if ! python -c "import pytest" &>/dev/null; then
                    echo "Need to install pytest..."
                    NEED_INSTALL=1
                  fi
                  
                  if ! python -c "import pytest_cov" &>/dev/null; then
                    echo "Need to install pytest-cov..."
                    NEED_INSTALL=1
                  fi
                  
                  if [ $NEED_INSTALL -eq 1 ]; then
                    echo "Installing test dependencies..."
                    if command -v uv >/dev/null 2>&1; then
                      uv pip install pytest pytest-cov
                    else
                      pip install pytest pytest-cov
                    fi
                  fi
                  
                  # Parse arguments to see if we should include coverage
                  COVERAGE_ARG="--cov=server --cov-report=term --cov-report=html"
                  for arg in "$@"; do
                    case $arg in
                      --no-coverage)
                        COVERAGE_ARG=""
                        echo "Running without coverage reporting..."
                        shift
                        ;;
                      *)
                        # Unknown option
                        ;;
                    esac
                  done
                  
                  # Run pytest with proper configuration
                  python -m pytest tests/ -v $COVERAGE_ARG
                  
                  # Show coverage message if enabled
                  if [ -n "$COVERAGE_ARG" ]; then
                    echo "✅ Coverage report generated. HTML report available in htmlcov/"
                  fi
                '';
              }
              {
                name = "lint";
                category = "development";
                help = "Lint Python code with Black and Flake8";
                command = ''
                  echo "Linting Python code..."
                  source .venv/bin/activate
                  
                  # Ensure flake8 is installed
                  if ! python -c "import flake8" &>/dev/null; then
                    echo "Installing flake8..."
                    if command -v uv >/dev/null 2>&1; then
                      uv pip install flake8
                    else
                      pip install flake8
                    fi
                  fi
                  
                  # Format with Black
                  echo "Running Black formatter..."
                  black *.py tests/
                  
                  # Run flake8 to check for issues
                  echo "Running Flake8 linter..."
                  flake8 server.py tests/
                '';
              }
              {
                name = "format";
                category = "development";
                help = "Format Python code with Black";
                command = ''
                  echo "Formatting Python code..."
                  source .venv/bin/activate
                  black *.py tests/
                  echo "✅ Code formatted"
                '';
              }
            ];
            
            # Define startup hook to create/activate venv
            devshell.startup.venv_setup.text = ''
              # Set up virtual environment
              ${setupVenvScript}
              
              # Print environment info
              echo ""
              echo "┌─────────────────────────────────────────────────┐"
              echo "│            NixMCP Development Environment        │"
              echo "└─────────────────────────────────────────────────┘"
              echo ""
              echo "• Python: $(python --version)"
              echo "• Nix:    $(nix --version)"
              echo ""
              echo "┌─────────────────────────────────────────────────┐"
              echo "│                 Quick Commands                   │"
              echo "└─────────────────────────────────────────────────┘"
              echo ""
              echo "  ⚡ run          - Start the NixMCP server"
              echo "  🧪 run-tests    - Run tests with coverage (--no-coverage to disable)"
              echo "  🧹 lint         - Run linters (Black + Flake8)"
              echo "  ✨ format       - Format code with Black"
              echo "  🔧 setup        - Set up Python environment"
              echo "  🚀 setup-uv     - Install uv for faster dependency management"
              echo ""
              echo "Use 'menu' to see all available commands."
              echo "─────────────────────────────────────────────────────"
            '';
          };
          
          # Legacy devShell for backward compatibility (simplified)
          legacy = pkgs.mkShell {
            name = "nixmcp-legacy";
            
            packages = [
              pythonEnv
              pkgs.nix
              pkgs.nixos-option
              uvInstaller
            ];
            
            # Simple shell hook that uses the same setup logic
            shellHook = ''
              export SHELL=${pkgs.bash}/bin/bash
              export PS1="(nixmcp) $ "
              
              # Set up virtual environment
              ${setupVenvScript}
              
              echo "NixMCP Legacy Shell activated"
              echo "Run 'python server.py' to start the server"
            '';
          };
        };
      });
}
