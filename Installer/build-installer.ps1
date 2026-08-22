<#
 Build script for Inno Setup
 Requirements: Inno Setup installed.
 Locates ISCC.exe automatically (PATH, common folders, registry),
 or pass -ISCCPath for a custom path.
#>

param(
    [string]$ISCCPath = "",
    [string]$ScriptPath = ""
)

if (-not $ScriptPath) {
    $ScriptPath = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "gloveshift.iss"
}

function Get-IsccPath {
    param([string]$Override)

    if ($Override) {
        if ($Override -match '^[A-Za-z]:\\?$') {
            Write-Warning "Provided ISCC path looks like a drive root: $Override. Provide the full path to ISCC.exe."
            return $null
        }
        if (-not (Test-Path -LiteralPath $Override)) {
            Write-Warning "Provided ISCC path not found: $Override"
            return $null
        }
        $item = Get-Item -LiteralPath $Override -ErrorAction SilentlyContinue
        if ($item.PSIsContainer) {
            $candidate = Join-Path $item.FullName 'ISCC.exe'
            if (Test-Path -LiteralPath $candidate) {
                return (Resolve-Path -LiteralPath $candidate).Path
            }
        }
        elseif ($item.Name -ieq 'ISCC.exe') {
            return (Resolve-Path -LiteralPath $item.FullName).Path
        }
        Write-Warning "Provided ISCC path not valid: $Override"
        return $null
    }

    $fromPath = (Get-Command ISCC.exe -ErrorAction SilentlyContinue).Path
    if ($fromPath) { return $fromPath }

    # Check known locations. Do NOT index a piped Where-Object result:
    # a single match becomes a string, and [0] would be the character "C".
    $programFilesX86 = [Environment]::GetEnvironmentVariable("ProgramFiles(x86)")
    $possible = @(
        $(if ($programFilesX86) { Join-Path $programFilesX86 'Inno Setup 6\ISCC.exe' })
        $(if ($env:ProgramFiles) { Join-Path $env:ProgramFiles 'Inno Setup 6\ISCC.exe' })
        $(if ($env:LOCALAPPDATA) { Join-Path $env:LOCALAPPDATA 'Programs\Inno Setup 6\ISCC.exe' })
    )
    foreach ($candidate in $possible) {
        if ($candidate -and (Test-Path -LiteralPath $candidate)) {
            return $candidate
        }
    }

    $regPaths = @(
        'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1',
        'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1'
    )
    foreach ($rp in $regPaths) {
        if (Test-Path $rp) {
            $instDir = (Get-ItemProperty -Path $rp -ErrorAction SilentlyContinue).InstallLocation
            if ($instDir) {
                $iscc = Join-Path $instDir 'ISCC.exe'
                if (Test-Path -LiteralPath $iscc) { return $iscc }
            }
        }
    }

    return $null
}

$resolvedIscc = Get-IsccPath -Override $ISCCPath
if (-not $resolvedIscc) {
    Write-Error @"
ISCC.exe not found.
Install Inno Setup (winget install --id JRSoftware.InnoSetup -e),
or pass -ISCCPath, e.g.:
  powershell -ExecutionPolicy Bypass -File Installer\build-installer.ps1 -ISCCPath "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
"@
    exit 1
}

Write-Host "Building installer using: $resolvedIscc" -ForegroundColor Cyan

$installerDir = Split-Path -Parent $ScriptPath
$projectRoot = Split-Path -Parent $installerDir
$distDir = Join-Path $projectRoot 'dist'

# Load .env before checking the EXE name
$envFile = Join-Path $projectRoot '.env'
$defines = @{}
if (Test-Path -LiteralPath $envFile) {
    Write-Host "Loading build variables from .env" -ForegroundColor Cyan
    Get-Content -LiteralPath $envFile | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith('#')) { return }
        $eq = $line.IndexOf('=')
        if ($eq -gt 0) {
            $k = $line.Substring(0, $eq).Trim()
            $v = $line.Substring($eq + 1).Trim().Trim('"')
            $defines[$k] = $v
        }
    }
}

$exeName = 'GloveShift.exe'
if ($defines.ContainsKey('APP_EXE_NAME') -and $defines['APP_EXE_NAME']) {
    $exeName = $defines['APP_EXE_NAME']
    if ($exeName -notlike '*.exe') { $exeName = "$exeName.exe" }
}
$exePath = Join-Path $distDir $exeName
if (-not (Test-Path -LiteralPath $exePath)) {
    Write-Error @"
$exePath not found.
Build the executable first, then re-run this script.
"@
    exit 1
}

# Ensure images are present in dist for the installer
$imagesSrc = Join-Path $projectRoot 'images'
$imagesDst = Join-Path $distDir 'images'
if (-not (Test-Path -LiteralPath $imagesDst)) {
    if (Test-Path -LiteralPath $imagesSrc) {
        Write-Host "Copying images to dist..." -ForegroundColor Yellow
        Copy-Item -Recurse -Force -LiteralPath $imagesSrc -Destination $imagesDst
    } else {
        Write-Warning "images folder not found at '$imagesSrc'."
    }
}

# Map .env vars to Inno Setup defines
$defineArgs = @()
if ($defines.ContainsKey('APP_NAME') -and $defines['APP_NAME']) {
    $defineArgs += "/DMyAppName=`"$($defines['APP_NAME'])`""
}
if ($defines.ContainsKey('APP_VERSION') -and $defines['APP_VERSION']) {
    $defineArgs += "/DMyAppVersion=`"$($defines['APP_VERSION'])`""
}
if ($defines.ContainsKey('APP_PUBLISHER') -and $defines['APP_PUBLISHER']) {
    $defineArgs += "/DMyAppPublisher=`"$($defines['APP_PUBLISHER'])`""
}
if ($defines.ContainsKey('APP_URL') -and $defines['APP_URL']) {
    $defineArgs += "/DMyAppURL=`"$($defines['APP_URL'])`""
}
$defineArgs += "/DMyAppExeName=`"$exeName`""
if ($defines.ContainsKey('APP_ICON') -and $defines['APP_ICON']) {
    $iconVal = $defines['APP_ICON']
    if (-not ([System.IO.Path]::IsPathRooted($iconVal))) {
        $resolvedIcon = Resolve-Path -LiteralPath (Join-Path $projectRoot $iconVal) -ErrorAction SilentlyContinue
        if ($resolvedIcon) { $iconVal = $resolvedIcon.Path }
    }
    $defineArgs += "/DMyAppIcon=`"$iconVal`""
}

Write-Host ("ISCC defines: " + ($defineArgs -join ' ')) -ForegroundColor DarkGray

$version = if ($defines.ContainsKey('APP_VERSION') -and $defines['APP_VERSION']) {
    $defines['APP_VERSION']
} else {
    '1.0.0'
}
$appName = if ($defines.ContainsKey('APP_NAME') -and $defines['APP_NAME']) {
    $defines['APP_NAME']
} else {
    'GloveShift'
}
$baseFilename = "$appName.Setup.$version"
$installerOutputDir = Join-Path $installerDir 'Output'
if (-not (Test-Path -LiteralPath $installerOutputDir)) {
    New-Item -ItemType Directory -Path $installerOutputDir | Out-Null
}

$outputPath = Join-Path $installerOutputDir ("$baseFilename.exe")
if (Test-Path -LiteralPath $outputPath) {
    Write-Host "Removing previous installer: $outputPath" -ForegroundColor Yellow
    for ($i = 0; $i -lt 5; $i++) {
        try {
            Remove-Item -LiteralPath $outputPath -Force -ErrorAction Stop
            break
        } catch {
            Start-Sleep -Milliseconds 400
        }
    }
}

$outputArgs = @("/O$installerOutputDir", "/F$baseFilename")

$maxAttempts = 3
$attempt = 1
$exit = 1
do {
    if ($attempt -gt 1) {
        Write-Host "Retrying build (attempt $attempt of $maxAttempts)..." -ForegroundColor Yellow
    }
    & $resolvedIscc @outputArgs @defineArgs $ScriptPath
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
