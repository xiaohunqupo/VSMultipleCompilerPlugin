;Create by MakeSetup.py
#define AppName "VSMultipleCompilerPlugin"
#define AppNameShort "VSMCP"
#define AppVersion "1.0"
[Setup]
AppName={#AppName}
AppVersion={#AppVersion}
DefaultDirName={pf}\{#AppName}
DisableProgramGroupPage=no
DefaultGroupName={#AppName}
UninstallDisplayIcon={app}\Uninstall{#AppNameShort}.exe
OutputDir=Setup


[Types]
Name: "full"; Description: "Full installation"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: "VC90"; Description: "Visual Studio 9.0"; Types: full; 
Name: "VC100"; Description: "Visual Studio 10.0"; Types: full; 
Name: "VC110"; Description: "Visual Studio 11.0"; Types: full;
Name: "VC120"; Description: "Visual Studio 12.0"; Types: full;
Name: "VC140"; Description: "Visual Studio 14.0"; Types: full;

[Files]
;Source: "MyProg.exe"; DestDir: "{app}"; Components: program
;Source: "MyProg.chm"; DestDir: "{app}"; Components: help
;Source: "Readme.txt"; DestDir: "{app}"; Components: readme\en; Flags: isreadme
;Source: "Readme-German.txt"; DestName: "Liesmich.txt"; DestDir: "{app}"; Components: readme\de; Flags: isreadme

;[Files]
;Source: "MyProg.exe"; DestDir: "{app}"
;Source: "MyProg.chm"; DestDir: "{app}"
;Source: "Readme.txt"; DestDir: "{app}"; Flags: isreadme

[Dirs]
;Name: {code:GetDataDir}; Flags: uninsneveruninstall

[Icons]
Name: "{group}\Uninstall{#AppNameShort}"; Filename: "{app}\unins000.exe"

[Registry]
Root: HKCU; Subkey: "Software\{#AppName}"; Flags: uninsdeletekeyifempty
Root: HKLM; Subkey: "Software\{#AppName}"; Flags: uninsdeletekeyifempty
Root: HKLM; Subkey: "Software\{#AppName}\Settings"; ValueType: string; ValueName: "Path"; ValueData: "{app}"