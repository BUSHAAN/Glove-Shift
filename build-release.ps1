<#
.SYNOPSIS
  Build Glove Shift release assets ready to upload to GitHub Releases.

.DESCRIPTION
  1. Builds the portable one-file EXE with PyInstaller
  2. Builds the Windows installer (Inno Setup)
  3. Zips portable + setup
  4. Writes SHA256SUMS.txt
  5. Copies the three files into releases\<version>\ (gitignored)

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File .\build-release.ps1

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File .\build-release.ps1 -SkipExe
#>

param(
    [switch]$SkipExe,
    [switch]$SkipInstaller,
    [string]$ISCCPath = ""
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $ProjectRoot

function Read-DotEnv {
    param([string]$Path)
    $map = @{}
    if (-not (Test-Path -LiteralPath $Path)) { return $map }
    Get-Content -LiteralPath $Path | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith("#")) { return }
        $eq = $line.IndexOf("=")
        if ($eq -gt 0) {
            $k = $line.Substring(0, $eq).Trim()
            $v = $line.Substring($eq + 1).Trim().Trim('"').Trim("'")
            $map[$k] = $v
        }
    }
    return $map
}

function Write-Step([string]$Message) {
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

$envMap = Read-DotEnv (Join-Path $ProjectRoot ".env")
if ($envMap.Count -eq 0) {
    $envMap = Read-DotEnv (Join-Path $ProjectRoot ".env.example")
}

$AppName = if ($envMap["APP_NAME"]) { $envMap["APP_NAME"] } else { "GloveShift" }
$Version = if ($envMap["APP_VERSION"]) { $envMap["APP_VERSION"] } else { "1.0.0" }
$ExeName = if ($envMap["APP_EXE_NAME"]) { $envMap["APP_EXE_NAME"] } else { "$AppName.exe" }
if ($ExeName -notlike "*.exe") { $ExeName = "$ExeName.exe" }
$IconRel = if ($envMap["APP_ICON"]) { $envMap["APP_ICON"] } else { "images\icon.ico" }
$IconPath = Join-Path $ProjectRoot $IconRel

$DistDir = Join-Path $ProjectRoot "dist"
$ExePath = Join-Path $DistDir $ExeName
$ReleaseDir = Join-Path $ProjectRoot "releases\$Version"
$PortableZipName = "$AppName.Portable.exe.zip"
$SetupZipName = "$AppName.Setup.$Version.zip"
$ChecksumName = "SHA256SUMS.txt"

Write-Host "Glove Shift release build" -ForegroundColor Green
Write-Host "  App:     $AppName"
Write-Host "  Version: $Version"
Write-Host "  EXE:     $ExeName"
Write-Host "  Output:  $ReleaseDir"

# Prefer project venv Python/PyInstaller
$python = Join-Path $ProjectRoot "venv\Scripts\python.exe"
$pyinstaller = Join-Path $ProjectRoot "venv\Scripts\pyinstaller.exe"
if (-not (Test-Path -LiteralPath $python)) {
    $python = (Get-Command python -ErrorAction SilentlyContinue).Source
}
if (-not (Test-Path -LiteralPath $pyinstaller)) {
    $pyinstallerCmd = Get-Command pyinstaller -ErrorAction SilentlyContinue
    if ($pyinstallerCmd) { $pyinstaller = $pyinstallerCmd.Source }
}

if (-not $SkipExe) {
    Write-Step "Building portable EXE (PyInstaller)"
    if (-not $python) { throw "python not found. Activate/create venv first." }
    if (-not (Test-Path -LiteralPath $pyinstaller)) {
        Write-Host "Installing PyInstaller into current environment..." -ForegroundColor Yellow
        & $python -m pip install --upgrade pyinstaller
        $pyinstaller = Join-Path $ProjectRoot "venv\Scripts\pyinstaller.exe"
        if (-not (Test-Path -LiteralPath $pyinstaller)) {
            $pyinstaller = (Get-Command pyinstaller -ErrorAction Stop).Source
        }
    }
    if (-not (Test-Path -LiteralPath $IconPath)) {
        throw "Icon not found: $IconPath"
    }
    if (-not (Test-Path -LiteralPath (Join-Path $ProjectRoot "images"))) {
        throw "images/ folder not found"
    }
    if (-not (Test-Path -LiteralPath (Join-Path $ProjectRoot "models"))) {
        throw "models/ folder not found (MediaPipe .task model required)"
    }

    $nameNoExt = [System.IO.Path]::GetFileNameWithoutExtension($ExeName)
    & $pyinstaller --noconfirm --onefile --windowed `
        --name $nameNoExt `
        --icon $IconPath `
        --add-data "images;images" `
        --add-data "models;models" `
        --collect-all mediapipe `
        app.py
    if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed with exit code $LASTEXITCODE" }

    if (-not (Test-Path -LiteralPath $ExePath)) {
        throw "Expected EXE not found after build: $ExePath"
    }

    # Installer script expects dist\images\
    $distImages = Join-Path $DistDir "images"
    if (Test-Path -LiteralPath $distImages) {
        Remove-Item -LiteralPath $distImages -Recurse -Force
    }
    Copy-Item -Recurse -Force (Join-Path $ProjectRoot "images") $distImages
    Write-Host "Portable EXE ready: $ExePath" -ForegroundColor Green
} else {
    Write-Step "Skipping EXE build (-SkipExe)"
    if (-not (Test-Path -LiteralPath $ExePath)) {
        throw "EXE not found at $ExePath. Build it first or omit -SkipExe."
    }
}

$SetupExePath = $null
if (-not $SkipInstaller) {
    Write-Step "Building Windows installer (Inno Setup)"
    $installerScript = Join-Path $ProjectRoot "Installer\build-installer.ps1"
    if (-not (Test-Path -LiteralPath $installerScript)) {
        throw "Missing $installerScript"
    }
    if ($ISCCPath) {
        & powershell -ExecutionPolicy Bypass -File $installerScript -ISCCPath $ISCCPath
    } else {
        & powershell -ExecutionPolicy Bypass -File $installerScript
    }
    if ($LASTEXITCODE -ne 0) { throw "Installer build failed with exit code $LASTEXITCODE" }

    $SetupExePath = Join-Path $ProjectRoot "Installer\Output\$AppName.Setup.$Version.exe"
    if (-not (Test-Path -LiteralPath $SetupExePath)) {
        # Fallback: newest setup exe in Output
        $SetupExePath = Get-ChildItem (Join-Path $ProjectRoot "Installer\Output") -Filter "*.exe" |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 1 -ExpandProperty FullName
    }
    if (-not $SetupExePath -or -not (Test-Path -LiteralPath $SetupExePath)) {
        throw "Installer EXE not found under Installer\Output"
    }
    Write-Host "Installer ready: $SetupExePath" -ForegroundColor Green
} else {
    Write-Step "Skipping installer build (-SkipInstaller)"
    $SetupExePath = Join-Path $ProjectRoot "Installer\Output\$AppName.Setup.$Version.exe"
    if (-not (Test-Path -LiteralPath $SetupExePath)) {
        throw "Installer not found at $SetupExePath"
    }
}

Write-Step "Creating release folder and zip assets"
if (Test-Path -LiteralPath $ReleaseDir) {
    Remove-Item -LiteralPath $ReleaseDir -Recurse -Force
}
New-Item -ItemType Directory -Path $ReleaseDir | Out-Null

$portableZip = Join-Path $ReleaseDir $PortableZipName
$setupZip = Join-Path $ReleaseDir $SetupZipName
$checksumFile = Join-Path $ReleaseDir $ChecksumName

if (Test-Path -LiteralPath $portableZip) { Remove-Item -LiteralPath $portableZip -Force }
if (Test-Path -LiteralPath $setupZip) { Remove-Item -LiteralPath $setupZip -Force }

# Compress-Archive needs the file name inside the zip to be clean
$tempPortableDir = Join-Path $env:TEMP "gloveshift-portable-$Version"
$tempSetupDir = Join-Path $env:TEMP "gloveshift-setup-$Version"
foreach ($d in @($tempPortableDir, $tempSetupDir)) {
    if (Test-Path -LiteralPath $d) { Remove-Item -LiteralPath $d -Recurse -Force }
    New-Item -ItemType Directory -Path $d | Out-Null
}
Copy-Item -LiteralPath $ExePath -Destination (Join-Path $tempPortableDir $ExeName) -Force
Copy-Item -LiteralPath $SetupExePath -Destination (Join-Path $tempSetupDir (Split-Path $SetupExePath -Leaf)) -Force

Compress-Archive -Path (Join-Path $tempPortableDir "*") -DestinationPath $portableZip -Force
Compress-Archive -Path (Join-Path $tempSetupDir "*") -DestinationPath $setupZip -Force

Remove-Item -LiteralPath $tempPortableDir -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $tempSetupDir -Recurse -Force -ErrorAction SilentlyContinue

Write-Step "Writing $ChecksumName"
$hashes = @()
foreach ($file in @($portableZip, $setupZip)) {
    $hash = (Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash.ToLower()
    $name = Split-Path $file -Leaf
    $hashes += "$hash  $name"
}
$hashes | Set-Content -LiteralPath $checksumFile -Encoding ascii

Write-Host ""
Write-Host "Release assets ready - drag these into GitHub Releases:" -ForegroundColor Green
Get-ChildItem -LiteralPath $ReleaseDir | ForEach-Object {
    $mb = [math]::Round($_.Length / 1MB, 1)
    Write-Host ("  {0,-40} {1,8} MB" -f $_.Name, $mb)
}
Write-Host ""
Write-Host "Folder: $ReleaseDir" -ForegroundColor Green
