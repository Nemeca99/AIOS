import os
import subprocess
import sys

def main():
    try:
        while True:
            print("UML Calculator Launcher")
            print("1. Command-Line Calculator (CLI)")
            print("2. Graphical Calculator (GUI)")
            print("Q. Quit")
            choice = input("Select mode (1=CLI, 2=GUI, Q=Quit): ").strip().lower()
            base = os.path.dirname(sys.executable)
            if choice == '1':
                exe = os.path.join(base, "calculator_cli.exe")
                subprocess.run([exe])
            elif choice == '2':
                exe = os.path.join(base, "calculator_gui.exe")
                subprocess.Popen([exe])
                input("GUI launched. Press Enter to return to menu...")
            elif choice == 'q':
                print("Exiting.")
                break
            else:
                print("Invalid selection. Try again.")
    finally:
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
