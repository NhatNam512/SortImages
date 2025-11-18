# Script PowerShell tạo shortcut với icon
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$mainPy = Join-Path $scriptDir "main.py"
$pythonExe = (Get-Command python).Source
$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "Sao chep anh nang cao.lnk"

# Tìm icon
$iconPath = Join-Path $scriptDir "icon.ico"
if (-not (Test-Path $iconPath)) {
    $iconPath = Join-Path $scriptDir "icon.png"
}

# Tạo shortcut
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = $pythonExe
$Shortcut.Arguments = "`"$mainPy`""
$Shortcut.WorkingDirectory = $scriptDir
$Shortcut.Description = "Ung dung sao chep anh nang cao"
if (Test-Path $iconPath) {
    $Shortcut.IconLocation = "$iconPath,0"
    Write-Host "[OK] Da gan icon: $iconPath"
}
$Shortcut.Save()

Write-Host "[OK] Da tao shortcut tren Desktop: $shortcutPath"
Write-Host "[HOAN THANH] Shortcut da duoc tao!"

