a = Analysis(
    ['Account_Menu_GUI.py'],  # Replace with your entry script
    pathex=['.'],
    binaries=[],
    datas=[
        (r'C:\Users\didri\Desktop\LearnReflect VideoEnchancer\activation_window.py', 'activation_window.py'),
        (r'C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Decryption.py', 'Decryption.py'),
        (r'C:\Users\didri\Desktop\LearnReflect VideoEnchancer\encryption.py', 'encryption.py'),
        (r'C:\Users\didri\Desktop\LearnReflect VideoEnchancer\File_path.py', 'File_path.py'),
        (r'C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Forget_Password_frame.py', 'Forget_Password_frame.py'),
        (r'C:\Users\didri\Desktop\LearnReflect VideoEnchancer\LearnReflectAI_main.py', 'LearnReflectAI_main.py'),
        (r'C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Logger.py', 'Logger.py'),
        (r'C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Login.py', 'Login.py'),
        (r'C:\Users\didri\Desktop\LearnReflect VideoEnchancer\LoginAccount_GUI.py', 'LoginAccount_GUI.py'),
        (r'C:\Users\didri\Desktop\LearnReflect VideoEnchancer\RegisterAccount_GUI.py', 'RegisterAccount_GUI.py'),
        (r'C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Registration.py', 'Registration.py'),
        (r'C:\Users\didri\Desktop\LearnReflect VideoEnchancer\User_data_storage.py', 'User_data_storage.py'),
        (r'C:\Users\didri\Desktop\LearnReflect VideoEnchancer\UserAccount.py', 'UserAccount.py'),
        (r'C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Validate_key.py', 'Validate_key.py'),
        (r'C:\Users\didri\Desktop\LearnReflect VideoEnchancer\dist\VideoEnchancer.exe', 'VideoEnchancer.exe'),
        (r"C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Assets", "Assets"),

    ],
    hiddenimports=[
        'numpy.core',
        'threadpoolctl',
        'win32pdh',
        'yaml',
        'numpy.core',
        'numpy._typing',
        'numpy.lib',
        'numpy.ma',
        'numpy.linalg',
        'numpy.fft',
        'numpy.testing',
        'numpy.array_api',
        'numpy.core.arrayprint',
        'psutil',
        'brotli',
        'brotlicffi',
        'socks',
        'numpy.*',
    ],
    hookspath=[],
    hooksconfig={},
)

# PYZ creation
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# EXE creation
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Account_Menu_GUI',  # Output name of your GUI exe
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  
    manifest=r"C:\Users\didri\Desktop\LearnReflect VideoEnchancer\Program.manifest",
)

# Collect everything
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,  # Include all data files and the VideoEnchancer.exe
    strip=False,
    upx=True,
    name='Account_Menu_GUI',  # Output directory name
)
