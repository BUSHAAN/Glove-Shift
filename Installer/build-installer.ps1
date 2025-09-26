<#
 Build script for Inno Setup
 Requirements: Inno Setup installed.
 This script will try to locate ISCC.exe automatically (PATH, common folders, registry),
 but you can also pass a custom path via -ISCCPath.
#>

param(
    [string]$ISCCPath = "",
    [string]$ScriptPath = "$(Split-Path -Parent $MyInvocation.MyCommand.Path)\\gloveshift.iss"
)

function Get-IsccPath {
    param([string]$Override)

    if ($Override) {
        # If user passed a drive root like C: or C:\, reject
        if ($Override -match '^[A-Za-z]:\\?$') {
            Write-Warning "Provided ISCC path looks like a drive root: $Override. Please provide the full path to ISCC.exe."
            return $null
        }
        elseif (Test-Path $Override) {
            $item = Get-Item $Override -ErrorAction SilentlyContinue
            if ($item) {
                if ($item.PSIsContainer) {
                    $candidate = Join-Path $item.FullName 'ISCC.exe'
                    if (Test-Path $candidate) { return (Resolve-Path $candidate).Path }
                } else {
                    if ($item.Name -ieq 'ISCC.exe') { return (Resolve-Path $item.FullName).Path }
                }
            }
            Write-Warning "Provided ISCC path not valid: $Override"
            return $null
        } else {
            Write-Warning "Provided ISCC path not found: $Override"
            return $null
        }
    }

    # 1) PATH lookup
    $fromPath = (Get-Command ISCC.exe -ErrorAction SilentlyContinue).Path
    if ($fromPath) { return $fromPath }

    # 2) Common install locations (64-bit, 32-bit, and per-user install)
    $candidates = @(
        (Join-Path ${env:ProgramFiles(x86)} 'Inno Setup 6\ISCC.exe'),
        (Join-Path $env:ProgramFiles 'Inno Setup 6\ISCC.exe'),
        (Join-Path $env:LOCALAPPDATA 'Programs\Inno Setup 6\ISCC.exe')
    ) | Where-Object { $_ -and (Test-Path $_) }
    if ($candidates.Count -gt 0) { return $candidates[0] }

    # 3) Registry lookup
    $regPaths = @(
        'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1',
        'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1'
    )
    foreach ($rp in $regPaths) {
        if (Test-Path $rp) {
            $instDir = (Get-ItemProperty -Path $rp -ErrorAction SilentlyContinue).InstallLocation
            if ($instDir) {
                $iscc = Join-Path $instDir 'ISCC.exe'
                if (Test-Path $iscc) { return $iscc }
            }
        }
    }

    return $null
}

$resolvedIscc = Get-IsccPath -Override $ISCCPath
if (-not $resolvedIscc) {
    Write-Error @"
ISCC.exe not found.
Please install Inno Setup (winget install --id JRSoftware.InnoSetup -e),
or provide the path to ISCC.exe, e.g.:
  powershell -ExecutionPolicy Bypass -File installer\\build-installer.ps1 -ISCCPath "C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe"
"@
    exit 1
}

Write-Host "Building installer using: $resolvedIscc" -ForegroundColor Cyan

# Preflight: ensure dist\main.exe exists
$installerDir = Split-Path -Parent $ScriptPath
$projectRoot = Split-Path -Parent $installerDir
$distDir = Join-Path $projectRoot 'dist'
$exeName = if ($defines.ContainsKey('APP_EXE_NAME') -and $defines['APP_EXE_NAME']) { $defines['APP_EXE_NAME'] } else { 'main.exe' }
$exePath = Join-Path $distDir $exeName
if (-not (Test-Path $exePath)) {
    Write-Error @"
$exePath not found.
Please build the executable first, e.g.:
  python -m pip install pyinstaller
  pyinstaller --onefile main.py
Then ensure images are available:
  Copy-Item -Recurse images dist\\images
"@
    exit 1
}

# Ensure images are present in dist for the installer
$imagesSrc = Join-Path $projectRoot 'images'
$imagesDst = Join-Path $distDir 'images'
if (-not (Test-Path $imagesDst)) {
    if (Test-Path $imagesSrc) {
        Write-Host "Copying images to dist..." -ForegroundColor Yellow
        Copy-Item -Recurse -Force $imagesSrc $imagesDst
    } else {
        Write-Warning "images source folder not found at '$imagesSrc'. If your app requires images at runtime, create this folder."
    }
}

# Load build variables from .env if present
$envFile = Join-Path $projectRoot '.env'
$defines = @{}
if (Test-Path $envFile) {
    Write-Host "Loading build variables from .env" -ForegroundColor Cyan
    Get-Content $envFile | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith('#')) { return }
        # support KEY=VALUE and KEY="VALUE"
        $eq = $line.IndexOf('=')
        if ($eq -gt 0) {
            $k = $line.Substring(0, $eq).Trim()
            $v = $line.Substring($eq + 1).Trim().Trim('"')
            $defines[$k] = $v
        }
    }
}

# Map .env vars to Inno Setup defines
$defineArgs = @()
$desiredExeName = 'main.exe'
if ($defines.ContainsKey('APP_NAME') -and $defines['APP_NAME']) { $defineArgs += "/DMyAppName=`"$($defines['APP_NAME'])`"" }
if ($defines.ContainsKey('APP_VERSION') -and $defines['APP_VERSION']) { $defineArgs += "/DMyAppVersion=`"$($defines['APP_VERSION'])`"" }
if ($defines.ContainsKey('APP_PUBLISHER') -and $defines['APP_PUBLISHER']) { $defineArgs += "/DMyAppPublisher=`"$($defines['APP_PUBLISHER'])`"" }
if ($defines.ContainsKey('APP_URL') -and $defines['APP_URL']) { $defineArgs += "/DMyAppURL=`"$($defines['APP_URL'])`"" }
if ($defines.ContainsKey('APP_EXE_NAME') -and $defines['APP_EXE_NAME']) { $defineArgs += "/DMyAppExeName=`"$($defines['APP_EXE_NAME'])`""; $desiredExeName = $defines['APP_EXE_NAME'] }
if ($defines.ContainsKey('APP_ICON') -and $defines['APP_ICON']) {
    $iconVal = $defines['APP_ICON']
    if (-not ([System.IO.Path]::IsPathRooted($iconVal))) {
        $iconVal = Resolve-Path -LiteralPath (Join-Path $projectRoot $iconVal) -ErrorAction SilentlyContinue
        if ($iconVal) { $iconVal = $iconVal.Path } else { $iconVal = $defines['APP_ICON'] }
    }
    $defineArgs += "/DMyAppIcon=`"$iconVal`""
}

Write-Host ("ISCC defines: " + ($defineArgs -join ' ')) -ForegroundColor DarkGray

# Compute output filename and directory
$version = if ($defines.ContainsKey('APP_VERSION') -and $defines['APP_VERSION']) { $defines['APP_VERSION'] } else { '1.0.0' }
$baseFilename = "$($defines['APP_NAME']) setup $version"
$installerOutputDir = Join-Path $installerDir 'Output'
if (-not (Test-Path $installerOutputDir)) { New-Item -ItemType Directory -Path $installerOutputDir | Out-Null }

# Best effort: remove previous output installer to avoid lock errors
$outputPath = Join-Path $installerOutputDir ("$baseFilename.exe")
if (Test-Path $outputPath) {
    Write-Host "Removing previous installer: $outputPath" -ForegroundColor Yellow
    for ($i=0; $i -lt 5; $i++) {
        try { Remove-Item -LiteralPath $outputPath -Force -ErrorAction Stop; break }
        catch { Start-Sleep -Milliseconds 400 }
    }
    if (Test-Path $outputPath) { Write-Warning "Could not remove existing installer file. If the build fails, close any process locking it and retry." }
}

# Ensure the desired exe name exists in dist (rename/copy main.exe if necessary)
$desiredExePath = Join-Path $distDir $desiredExeName
if ($desiredExeName -ne 'main.exe' -and -not (Test-Path $desiredExePath)) {
    $srcExe = Join-Path $distDir 'main.exe'
    if (Test-Path $srcExe) {
        try {
            Copy-Item -LiteralPath $srcExe -Destination $desiredExePath -Force
            Write-Host "Created '$desiredExeName' in dist from main.exe to match APP_EXE_NAME." -ForegroundColor Yellow
        } catch {
            Write-Warning "Failed to create '$desiredExeName' in dist: $($_.Exception.Message)"
        }
    }
}

# Pass output directory and base filename to ISCC to avoid name contention
$outputArgs = @("/O$installerOutputDir", "/F$baseFilename")

# Invoke ISCC with a couple of retries to handle transient file locks by AV/Explorer
$maxAttempts = 3
$attempt = 1
do {
    if ($attempt -gt 1) { Write-Host "Retrying build (attempt $attempt of $maxAttempts)..." -ForegroundColor Yellow }
    & "$resolvedIscc" @outputArgs @defineArgs "$ScriptPath"
    $exit = $LASTEXITCODE
    if ($exit -eq 0) { break }
    if ($attempt -lt $maxAttempts) {
        Write-Warning "ISCC exited with code $exit. Waiting briefly before retry..."
        Start-Sleep -Seconds 2
    }
    $attempt++
} while ($attempt -le $maxAttempts)

if ($exit -ne 0) {
    Write-Error "Installer build failed after $maxAttempts attempts with exit code $exit"
    exit $exit
}

$builtPath = Join-Path $installerOutputDir ("$baseFilename.exe")
Write-Host "Installer built successfully: $builtPath" -ForegroundColor Green