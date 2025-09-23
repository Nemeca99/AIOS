
import importlib.util
import sys
from pathlib import Path

# Use the current directory as the directive source
DIRECTIVES_DIR = Path(__file__).parent

def import_and_run_module(file_path):
    module_name = file_path.stem
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            print(f"✅ Loaded: {module_name}")
        except Exception as e:
            print(f"⚠️ Failed to run {module_name}: {e}")
    else:
        print(f"⚠️ Could not load spec for {file_path}")

def main():
    print(f"📂 Scanning for directives in {DIRECTIVES_DIR}")
    for directive in sorted(DIRECTIVES_DIR.glob("directive_*.py")):
        if "placeholder" in directive.name.lower():
            continue  # Skip placeholders
        import_and_run_module(directive)

if __name__ == "__main__":
    print("📜 Beginning Archive Directive Ingestion")
    main()
