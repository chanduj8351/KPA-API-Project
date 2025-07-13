#!/usr/bin/env python3
"""
Setup script for KPA Form Data API project
Run this script to set up the project automatically
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")

def setup_virtual_environment():
    """Create and activate virtual environment"""
    venv_path = "venv"
    
    if os.path.exists(venv_path):
        print("📁 Virtual environment already exists")
        return
    
    # Create virtual environment
    run_command(f"{sys.executable} -m venv {venv_path}", "Creating virtual environment")
    
    # Activate virtual environment instructions
    if os.name == 'nt':  # Windows
        activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
        print(f"\n💡 To activate virtual environment on Windows, run: {activate_script}")
    else:  # Unix/Linux/macOS
        activate_script = os.path.join(venv_path, "bin", "activate")
        print(f"\n💡 To activate virtual environment on Unix/Linux/macOS, run: source {activate_script}")

def install_dependencies():
    """Install required Python packages"""
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
        pip_command = "pip"
    else:
        print("⚠️  Virtual environment not detected, using system pip")
        pip_command = f"{sys.executable} -m pip"
    
    # Upgrade pip
    run_command(f"{pip_command} install --upgrade pip", "Upgrading pip")
    
    # Install dependencies
    run_command(f"{pip_command} install -r requirements.txt", "Installing dependencies")

def create_env_file():
    """Create .env file from template"""
    env_file = ".env"
    env_example = ".env.example"
    
    if os.path.exists(env_file):
        print("📁 .env file already exists")
        return
    
    if os.path.exists(env_example):
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please update the SECRET_KEY in .env file for production!")
    else:
        # Create basic .env file
        with open(env_file, 'w') as f:
            f.write("DATABASE_URL=sqlite:///./kpa_forms.db\n")
            f.write("SECRET_KEY=your-super-secret-key-change-in-production\n")
            f.write("ACCESS_TOKEN_EXPIRE_MINUTES=30\n")
        print("✅ Created basic .env file")

def test_installation():
    """Test if the installation was successful"""
    print("\n🧪 Testing installation...")
    
    try:
        # Try importing main modules
        import fastapi
        import sqlalchemy
        import uvicorn
        print("✅ All required modules imported successfully")
        
        # Check if main.py exists
        if os.path.exists("main.py"):
            print("✅ main.py found")
        else:
            print("❌ main.py not found")
            
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 KPA Form Data API - Project Setup")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Setup virtual environment
    setup_virtual_environment()
    
    # Install dependencies
    install_dependencies()
    
    # Create .env file
    create_env_file()
    
    # Test installation
    if test_installation():
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Activate virtual environment (see instructions above)")
        print("2. Run the application: python main.py")
        print("3. Open browser: http://localhost:8000")
        print("4. View API docs: http://localhost:8000/docs")
        print("5. Test with Postman using the provided collection")
    else:
        print("\n❌ Setup encountered issues. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()