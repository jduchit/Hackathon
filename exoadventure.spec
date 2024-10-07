# -*- mode: python ; coding: utf-8 -*-

import cv2
block_cipher = None

a = Analysis(
    ['game-test.py'],  # Rename this to your actual main Python file name
    pathex=['.'],
    binaries=[],
    datas=[
        ('resources/background/new_background.jpeg', 'resources/background'),
        ('resources/flags/Flag_of_United_States-128x67.png', 'resources/flags'),
        ('resources/flags/Flag_of_Spain-128x85.png', 'resources/flags'),
        ('resources/flags/Flag_of_France-128x85.png', 'resources/flags'),
        ('resources/flags/Flag_of_Germany-128x77.png', 'resources/flags'),
        ('resources/flags/Flag_of_India-128x85.png', 'resources/flags'),
        ('resources/flags/Flag_of_Japan-128x85.png', 'resources/flags'),
        # Include the image resources
        ('resources/background/*.png', 'resources/background'),
        ('resources/planetAI/*.jpg', 'resources/planetAI'),
        
        # Include the fonts
        ('resources/font/*.otf', 'resources/font'),
        ('resources/font/*.ttf', 'resources/font'),

        # Include the sound files
        ('resources/sounds/*.wav', 'resources/sounds'),
        ('resources/character/astronaut.png', 'resources/character'),
        ('resources/character/cropped_face_with_transparent_bg.png', 'resources/character'),
        ('resources/planetAI', 'resources/planetAI'),
        ('Data/*.csv', 'Data'),  # Include all CSV files
        ('Data/*.pkl', 'Data'),  # Include all pickle files
        (cv2.data.haarcascades + 'haarcascade_frontalface_default.xml', 'cv2/data'),  # Include the Haar cascade file
    ],
    hiddenimports=[
        'pygame',
        'cv2',
        'numpy',
        'pandas',
        'sklearn',  # Add this if you're using scikit-learn
        'camera',
        'cropface',
        'Data.model'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ExoAdventure',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon=None
)