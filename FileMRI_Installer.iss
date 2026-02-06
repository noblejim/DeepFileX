; FileMRI Professional Installer Script
; Everything-style System App Installation
; Created: 2025-08-27

[Setup]
; App Information
AppName=FileMRI
AppVersion=1.3.0
AppVerName=FileMRI v1.3.0
AppPublisher=Zianni Development
AppPublisherURL=https://github.com/noblejim/filemri
AppSupportURL=https://github.com/noblejim/filemri/issues
AppUpdatesURL=https://github.com/noblejim/filemri/releases

; Installation Settings  
DefaultDirName={autopf}\FileMRI
DefaultGroupName=FileMRI
AllowNoIcons=yes
LicenseFile=LICENSE.txt
InfoBeforeFile=README.md
OutputDir=installer_output
OutputBaseFilename=FileMRI_v1.3.0_Setup
; SetupIconFile={app}\FileMRI.ico   ; Icon file not available yet
Compression=lzma
SolidCompression=yes
WizardStyle=modern

; System Requirements
MinVersion=0,6.1sp1
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1
Name: "addtopath"; Description: "Add FileMRI to system PATH"; GroupDescription: "System Integration"; Flags: unchecked
Name: "startuprun"; Description: "Run FileMRI at Windows startup"; GroupDescription: "System Integration"; Flags: unchecked

[Files]
; Main Application
Source: "dist\FileMRI_Phase11_Fixed.exe"; DestDir: "{app}"; DestName: "FileMRI.exe"; Flags: ignoreversion

; Documentation
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion  
Source: "system_requirements.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "filemri_guide_v4.md"; DestDir: "{app}"; Flags: ignoreversion

; Support Files
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "version_info.py"; DestDir: "{app}"; Flags: ignoreversion

; Batch Files for System Integration
Source: "FileMRI.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "run_filemri.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "system_check.bat"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu Icons
Name: "{group}\FileMRI"; Filename: "{app}\FileMRI.exe"; Comment: "File Medical Resonance Imaging - Diagnose your file system"; IconIndex: 0
Name: "{group}\FileMRI System Check"; Filename: "{app}\system_check.bat"; Comment: "Check system requirements"
Name: "{group}\FileMRI User Guide"; Filename: "{app}\filemri-enhanced-guide.md"; Comment: "Complete user guide"
Name: "{group}\{cm:UninstallProgram,FileMRI}"; Filename: "{uninstallexe}"

; Desktop Icon (optional)
Name: "{autodesktop}\FileMRI"; Filename: "{app}\FileMRI.exe"; Tasks: desktopicon; Comment: "File Medical Resonance Imaging"

; Quick Launch Icon (optional)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\FileMRI"; Filename: "{app}\FileMRI.exe"; Tasks: quicklaunchicon

[Run]
; Post-installation actions
Filename: "{app}\system_check.bat"; Parameters: "/silent"; StatusMsg: "Running system compatibility check..."; Flags: nowait postinstall skipifsilent
Filename: "{app}\FileMRI.exe"; Description: "{cm:LaunchProgram,FileMRI}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up user data (optional)
Type: files; Name: "{userappdata}\FileMRI\filemri.db"
Type: files; Name: "{userappdata}\FileMRI\filemri.log"
Type: dirifempty; Name: "{userappdata}\FileMRI"

[Registry]
; Add to Windows Search (Everything-style)
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\FileMRI.exe"; ValueType: string; ValueName: ""; ValueData: "{app}\FileMRI.exe"
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\FileMRI.exe"; ValueType: string; ValueName: "Path"; ValueData: "{app}"

; Add PATH environment variable (if selected)
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Tasks: addtopath; Check: NeedsAddPath('{app}')

; Startup registry entry (if selected)  
Root: HKCU; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "FileMRI"; ValueData: """{app}\FileMRI.exe"" --minimize"; Tasks: startuprun

[Code]
// Custom Pascal Script Functions

function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Custom post-install actions
    MsgBox('FileMRI has been successfully installed!'#13#10#13#10 + 
           'You can now:'#13#10 + 
           '• Search "FileMRI" in Windows Start Menu'#13#10 + 
           '• Run from command line: FileMRI.exe'#13#10 + 
           '• Use global shortcut: Ctrl+Alt+F (coming soon)', 
           mbInformation, MB_OK);
  end;
end;

function InitializeSetup(): Boolean;
begin
  // Pre-installation checks
  if not IsDotNetInstalled(net48, 0) then
  begin
    MsgBox('FileMRI requires .NET Framework 4.8 or higher.'#13#10 + 
           'Please install it from Microsoft website first.', 
           mbError, MB_OK);
    Result := False;
  end
  else
    Result := True;
end;