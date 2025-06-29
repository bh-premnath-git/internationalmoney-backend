<#
.SYNOPSIS
    Stops and removes the Docker containers for the project.
.DESCRIPTION
    This script provides a clean way to shut down the entire stack
    that was started with quick-start.ps1.
.EXAMPLE
    .\stop-stack.ps1
#>

# Stop on any error
$ErrorActionPreference = "Stop"

function Log-Message {
    param([string]$Message)
    Write-Host "🛑 $($Message)" -ForegroundColor Yellow
}

Log-Message "Stopping Docker stack..."
docker compose down --remove-orphans

Log-Message "✅ Stack stopped and removed."