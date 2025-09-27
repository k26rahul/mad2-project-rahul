Write-Host "Cleaning up database file..."
Remove-Item -Path "instance\demo.db" -ErrorAction SilentlyContinue

Write-Host "Cleaning up Redis dump..."
Remove-Item -Path "dump.rdb" -ErrorAction SilentlyContinue

Write-Host "Cleaning up Celery schedule file..."
Remove-Item -Path "celerybeat-schedule" -ErrorAction SilentlyContinue

Write-Host "Cleaning up Python cache directories..."
Get-ChildItem -Path . -Filter "__pycache__" -Recurse -Directory | Remove-Item -Recurse -Force
