import sys
import os
import site

if sys.prefix == sys.base_prefix:
    ve_name = "matrix_env"
    print("MATRIX STATUS: You're still plugged in")
    print(f"\nCurrent Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print("\nWARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print("\nTo enter the construct, run:")
    print(f"python3 -m venv {ve_name}")
    print(f"source {ve_name}/bin/activate # On Unix")
    print(f"{ve_name}\\Scripts\\activate # On Windows")
    print("\nThen run this program again.")

else:
    print("MATRIX STATUS: Welcome to the construct")
    print(f"\nCurrent Python: {sys.executable}")
    print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
    print(f"Environment Path: {sys.prefix}")
    print("\nSUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting the global system.")
    print("\nPackage installation path:")
    print(f"{site.getsitepackages()[0]}")
