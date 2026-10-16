$ErrorActionPreference = "Stop"
$ProjectDir = $PSScriptRoot
$Python = Join-Path $ProjectDir ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    throw "Python virtual environment not found. Create .venv and install requirements first."
}

Set-Location $ProjectDir
& $Python manage.py runserver 127.0.0.1:8000
