# Build and Package (Windows)

This guide shows how to build the standalone EXE and the Windows installer.

## 1) Prerequisites
- Windows 10/11
- Python 3
- PowerShell
- Inno Setup 6 (for the installer)

Install Inno Setup (if not installed):
```powershell
winget install --id JRSoftware.InnoSetup -e
```

## 2) Clone and set up a virtual environment
```powershell
git clone https://github.com/BUSHAAN/Glove-Shift.git

py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install pyinstaller
```

If you hit a "ModuleNotFoundError" later, install the missing package the same way:
```powershell
python -m pip install <package-name>
```

## 3) Configure build metadata (.env)
Copy the example file and adjust values:
```powershell
Copy-Item .env.example .env -Force
```

Edit `.env` to suit your app (examples):
```
APP_NAME="GloveShift"
APP_VERSION="1.0.1"
APP_PUBLISHER="Your Name"
APP_URL="https://example.com"
APP_EXE_NAME="GloveShift.exe"  # name shown in dist and shortcuts
APP_ICON="images\icon.ico"     # path to .ico (relative is OK)
```
Notes:
- You can include or omit ".exe" in APP_EXE_NAME; both work.
- If APP_ICON is relative, it’s resolved from the project root.
- The PyInstaller spec (`main.spec`) reads APP_EXE_NAME and APP_ICON from `.env`.

## 4) Build the standalone EXE
```powershell
.\.venv\Scripts\Activate.ps1
pyinstaller --noconfirm --onefile --windowed `
    --name GloveShift `
    --icon "Images/icon.ico" `
    --add-data "Images/icon.ico;." `
    --collect-all mediapipe `
    app.py 
```

Check outputs:
- EXE: `dist\<APP_EXE_NAME>` (e.g., `dist\GloveShift.exe`)
- Assets: `dist\images\...` (included by the spec)

## 5) Build the Windows installer
```powershell
# Auto-detects Inno Setup (ISCC.exe); pass -ISCCPath if needed
powershell -ExecutionPolicy Bypass -File installer\build-installer.ps1
```

Optional explicit path (if auto-detect fails):
```powershell
powershell -ExecutionPolicy Bypass -File installer\build-installer.ps1 -ISCCPath "C:\Users\<you>\AppData\Local\Programs\Inno Setup 6\ISCC.exe"
```

Installer output:
- `installer\Output\GloveShift-<APP_VERSION>.exe`

## 6) Install and verify
- Run the installer from `installer\Output`.
- Verify:
  - Desktop/Start Menu shortcuts use your EXE icon.
  - Control Panel (Apps & Features) shows your icon.
  - App launches and images are visible.

If icons don’t update immediately:
- Restart Windows Explorer (Task Manager → Windows Explorer → Restart), or log out/in.

## 7) Common troubleshooting
- File locked during installer build (ISCC error “being used by another process”): re-run the build; the script retries automatically. Close any antivirus scan or Explorer preview pane holding the output.
- Missing images at runtime: confirm `dist\images\...` exists. Re-run the EXE build (the spec includes images).
- Inno Setup not found: install via winget or pass `-ISCCPath` to `installer\build-installer.ps1`.
- Change icon or name: update `.env` (APP_ICON, APP_EXE_NAME), then rebuild the EXE and installer.

## 8) Clean build (optional)
```powershell
Remove-Item -Recurse -Force build, dist
# then rebuild:
pyinstaller --noconfirm main.spec
powershell -ExecutionPolicy Bypass -File installer\build-installer.ps1
```

That’s it—update `.env` to change naming/version/icon, rebuild the EXE with PyInstaller, and package it with the installer script.