& "$PSScriptRoot\cleanup.ps1"

Write-Host "Starting the application..."
nodemon --exec python -m app
