import os
import subprocess

def main():
    exe_path = os.path.join(os.path.dirname(__file__), "bin", "jomfish.exe")
    
    if not os.path.exists(exe_path):
        raise FileNotFoundError(f"Jomfish.exe nicht gefunden unter {exe_path}")

    subprocess.run([exe_path] + os.sys.argv[1:])

if __name__ == "__main__":
    main()
