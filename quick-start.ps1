<#
.SYNOPSIS
    Quick bootstrap for Enterprise Money-Transfer (LOCAL on Windows).
.DESCRIPTION
    This script sets up the development environment by installing Poetry,
    setting up the virtual environment, generating gRPC stubs, and
    launching the Docker stack.
.EXAMPLE
    .\quick-start.ps1
#>

# Stop on any error
$ErrorActionPreference = "Stop"

# --- Helper Functions ---
function Log-Message {
    param([string]$Message)
    # Using a Unicode arrow that works well in modern terminals
    Write-Host "👉 $($Message)" -ForegroundColor Green
}

# --- Configuration ---
Log-Message "Detecting Python executable..."
$pythonBin = if (Get-Command python -ErrorAction SilentlyContinue) {
    'python'
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    'python3'
} else {
    Write-Error "❌ Python not found. Please install Python and ensure it's in your PATH."
    exit 1
}
Log-Message "Using Python at: $($pythonBin)"

$composeFile = if ($env:COMPOSE_FILE) { $env:COMPOSE_FILE } else { "docker-compose.yml" }

# --- Script Body ---

# 1. Ensure Poetry is available
if (-not (Get-Command poetry -ErrorAction SilentlyContinue)) {
    Log-Message "Installing Poetry locally..."
    $installerScript = (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content
    $installerScript | & $pythonBin -
    
    # Add poetry to the PATH for the current session.
    # The installer places it in %APPDATA%\Python\Scripts on Windows.
    $poetryPath = "$env:APPDATA\Python\Scripts"
    $env:PATH = "$poetryPath;$env:PATH"
}

# 2. Create venv only inside project
Log-Message "Creating local Poetry virtualenv..."
poetry config virtualenvs.in-project true
Log-Message "Updating lock file if needed..."
poetry lock
Log-Message "Installing dependencies..."
poetry install --no-root --no-interaction --with dev
poetry sync

# 3. Generate gRPC stubs
Log-Message "Generating gRPC stubs..."
Log-Message "Finding venv Python to bypass fnm..."
$venv_python = (poetry env info --path) + "\Scripts\python.exe"
& $venv_python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. proto/userprofile.proto proto/banktransaction.proto

# 4. Build and run stack
Log-Message "Launching Docker stack..."
docker compose -f $composeFile build --quiet
docker compose -f $composeFile up -d

Log-Message "✅ Stack is running!"
Write-Host "➡️  REST + GraphQL: http://localhost:8000"
Write-Host "➡️  Swagger:        http://localhost:8000/docs"
Write-Host "➡️  Keycloak:       http://localhost:8080"
Write-Host "➡️  Grafana:        http://localhost:3000"