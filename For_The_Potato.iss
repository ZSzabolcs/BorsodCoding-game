[Setup]
#define MyAppName "For The Potato Demo"
#define MyAppExeName "main.exe"

AppId={{53FCCA29-1A5C-436D-B78C-804BCBAFE0EB}}
AppName={#MyAppName}
AppVersion=1.0
AppPublisher=Borsod Coding
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputBaseFilename=For_The_Potato_Demo_SETUP
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DefaultDirName=ForThePotatoDemo
UninstallDisplayIcon={app}\{#MyAppExeName}


[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "hungarian"; MessagesFile: "compiler:Languages\Hungarian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "Desktop icons:"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "Additional icons:"; Flags: unchecked;

[Icons]
Name: "{group}\For_The_Potato"; Filename: "{app}\main.exe"; WorkingDir: "{app}"; IconFilename: "{app}\main.exe"; IconIndex: 0
Name: "{commondesktop}\For_The_Potato"; Filename: "{app}\main.exe"; WorkingDir: "{app}"; IconFilename: "{app}\main.exe"; IconIndex: 0; Tasks: desktopicon

[CustomMessages]
CreateDesktopIcon=Create a &desktop icon
CreateQuickLaunchIcon=Create a &Quick Launch icon

[UninstallDelete]
Type: filesandordirs; Name: "{app}"




[Files]
Source: "..\BorsodCoding-game\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\BorsodCoding-game\kepek\*"; DestDir: "{app}\kepek"; Flags: ignoreversion recursesubdirs
Source: "..\BorsodCoding-game\zenek\*"; DestDir: "{app}\zenek"; Flags: ignoreversion recursesubdirs

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent; WorkingDir: "{app}"