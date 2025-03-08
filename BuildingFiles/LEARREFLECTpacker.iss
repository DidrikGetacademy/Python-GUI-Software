[Setup]
AppName=LearnReflect Video Enhancer
AppVersion=1.0
DefaultDirName={pf}\LearnReflect Video Enhancer
DefaultGroupName=LearnReflect Video Enhancer
OutputBaseFilename=LearnReflectVideoEnhancerInstaller
Compression=lzma
SolidCompression=yes
SetupIconFile=C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Assets\icon.ico

[Files]
; Add the main GUI executable
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\dist\Account_Menu_GUI\Account_Menu_GUI.exe"; DestDir: "{app}"; Flags: ignoreversion

; Add the _internal folder recursively (includes VideoEnchancer.exe)
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\dist\Account_Menu_GUI\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

; Add Video Enhancer executable
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\dist\VideoEnchancer.exe"; DestDir: "{app}"; Flags: ignoreversion

; Include all Python scripts as data files
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\activation_window.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Decryption.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\encryption.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\File_path.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Forget_Password_frame.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\LearnReflectAI_main.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Logger.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Login.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\LoginAccount_GUI.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\RegisterAccount_GUI.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Registration.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\User_data_storage.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\UserAccount.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Validate_key.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\dist\Account_Menu_GUI\_internal\*.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\dist\Account_Menu_GUI\_internal\*.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\dist\Account_Menu_GUI\_internal\*.pyd"; DestDir: "{app}"; Flags: ignoreversion
; Include DLL and manifest files
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\dist\Account_Menu_GUI\_internal\libcrypto-3.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\dist\Account_Menu_GUI\_internal\libffi-8.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\dist\Account_Menu_GUI\_internal\libssl-3.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\dist\Account_Menu_GUI\_internal\python3.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\dist\Account_Menu_GUI\_internal\python312.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\dist\Account_Menu_GUI\_internal\tcl86t.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\dist\Account_Menu_GUI\_internal\tk86t.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\dist\Account_Menu_GUI\_internal\VCRUNTIME140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\dist\Account_Menu_GUI\_internal\VCRUNTIME140_1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\dist\Account_Menu_GUI\_internal\zlib1.dll"; DestDir: "{app}"; Flags: ignoreversion

; Add manifest file
Source: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Program.manifest"; DestDir: "{app}"; Flags: ignoreversion


[Icons]
; Create shortcuts in the Start Menu and Desktop
Name: "{group}\LearnReflect Video Enhancer"; Filename: "{app}\Account_Menu_GUI.exe"; IconFilename: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Assets\icon.ico"
Name: "{commondesktop}\LearnReflect Video Enhancer"; Filename: "{app}\Account_Menu_GUI.exe"; IconFilename: "C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Assets\icon.ico"

[Run]
; Optionally run the application after installation
Filename: "{app}\Account_Menu_GUI.exe"; Description: "Launch LearnReflect Video Enhancer"; Flags: nowait postinstall
