"""
Build script for creating standalone executable.

Bu script, hayvan sınıflandırma uygulamasını tek bir .exe dosyasına
paketler. PyInstaller kullanarak tüm bağımlılıkları içeren
portable bir uygulama oluşturur.
"""

import os
import sys
import subprocess
import shutil


def check_requirements():
    """
    Gerekli dosyaların varlığını kontrol eder.

    Returns:
        bool: Tüm dosyalar mevcutsa True
    """
    required_files = [
        'app.py',
        'backend.py',
        'ResNet18_Animals_Best_Acc87.38.pth'
    ]

    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)

    if missing:
        print(f"[ERROR] Missing required files: {', '.join(missing)}")
        return False

    print("[OK] All required files found")
    return True


def create_spec_file():
    """
    PyInstaller spec dosyasını oluşturur.

    Spec dosyası, executable'ın nasıl oluşturulacağını tanımlar:
    - Hangi dosyaların dahil edileceği
    - Icon, versiyon bilgisi gibi metadata
    - Bundle yapısı (tek dosya vs klasör)
    """
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ResNet18_Animals_Best_Acc87.38.pth', '.'),
        ('backend.py', '.'),
    ],
    hiddenimports=[
        'gradio',
        'torch',
        'torchvision',
        'PIL',
        'pillow_avif',
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
    [],
    exclude_binaries=True,
    name='AnimalClassifierAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AnimalClassifierAI',
)
"""

    with open('AnimalClassifierAI.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

    print("[OK] Spec file created: AnimalClassifierAI.spec")


def build_executable():
    """
    PyInstaller ile executable oluşturur.

    Raises:
        subprocess.CalledProcessError: Build başarısız olursa
    """
    print("\n" + "="*60)
    print("Building executable...")
    print("="*60)
    print("\n[INFO] This may take several minutes...\n")

    try:
        # PyInstaller'ı spec dosyası ile çalıştır
        subprocess.run(
            ['pyinstaller', 'AnimalClassifierAI.spec', '--clean'],
            check=True
        )

        print("\n[OK] Build completed successfully!")
        print(f"[INFO] Executable location: dist/AnimalClassifierAI/AnimalClassifierAI.exe")

    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Build failed: {str(e)}")
        raise


def create_readme():
    """
    Executable için README dosyası oluşturur.
    """
    readme_content = """# Animal Classifier AI - Standalone Application

## How to Run

1. Navigate to the `dist/AnimalClassifierAI/` folder
2. Double-click `AnimalClassifierAI.exe`
3. Wait for the application to start (may take 30-60 seconds on first run)
4. Your default browser will open with the application interface
5. If browser doesn't open automatically, visit: http://127.0.0.1:7860

## System Requirements

- Windows 10/11 (64-bit)
- Minimum 4GB RAM
- Internet connection (for first launch only)

## Troubleshooting

**Application won't start:**
- Check if port 7860 is available
- Run as Administrator if needed
- Check Windows Defender / Antivirus settings

**Slow predictions:**
- This is normal on CPU-only systems
- GPU acceleration requires CUDA drivers

## Technical Details

- Model: ResNet18
- Classes: 50 animal types
- Accuracy: 87.38%
- Framework: PyTorch + Gradio

## Support

For issues or questions, refer to the main README.md in the source directory.
"""

    os.makedirs('dist/AnimalClassifierAI', exist_ok=True)

    with open('dist/AnimalClassifierAI/README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print("[OK] README.txt created in dist folder")


def main():
    """
    Ana build süreci.
    """
    print("="*60)
    print("Animal Classifier AI - Executable Builder")
    print("="*60)

    # 1. Gereksinimleri kontrol et
    if not check_requirements():
        sys.exit(1)

    # 2. Spec dosyası oluştur
    create_spec_file()

    # 3. Executable oluştur
    try:
        build_executable()
    except Exception as e:
        print(f"\n[ERROR] Build process failed: {str(e)}")
        sys.exit(1)

    # 4. README oluştur
    create_readme()

    # 5. Başarı mesajı
    print("\n" + "="*60)
    print("BUILD SUCCESSFUL!")
    print("="*60)
    print("\nYou can now run the application:")
    print("  dist/AnimalClassifierAI/AnimalClassifierAI.exe")
    print("\nThe entire 'dist/AnimalClassifierAI' folder is portable.")
    print("You can copy it to any Windows computer and run it.")
    print("="*60)


if __name__ == "__main__":
    main()
