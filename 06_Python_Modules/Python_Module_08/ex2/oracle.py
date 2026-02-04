from dotenv import load_dotenv
import os


def check_hardcoded_secrets(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            clean_line = line.strip().replace(" ", "")
            for key in ['API_KEY', 'PASSWORD', 'ACCESS_TOKEN']:
                if f'{key}=' in clean_line:
                    return False
        return True
    except Exception:
        return False


if __name__ == "__main__":
    print("ORACLE STATUS: Reading the Matrix...")

    if not os.path.isfile(".env"):
        print("\n[FAIL] .env not found\nPlease run: cp .env.example .env")
        exit(1)

    load_dotenv()
    print("Configuration loaded:")

    mode = os.getenv("MATRIX_MODE", "production")
    db_url = os.getenv("DATABASE_URL")
    api_key = os.getenv("API_KEY")
    log_level = os.getenv("LOG_LEVEL", "INFO")
    zion_url = os.getenv("ZION_ENDPOINT")

    missing = []

    for CONST in ["DATABASE_URL", "API_KEY"]:
        if not os.getenv(CONST):
            missing.append(CONST)

    if missing:
        print("\nWARNING: Missing configuration variables!")
        for m in missing:
            print(f" -> {m} is not set.")
        print("Please check your .env file\n")
        exit(1)

    print(f"Mode: {mode}")
    print(
        f"Database: Connected to "
        f"{'local' if '@localhost' in db_url else 'a remote'} instance"
    )
    print(f"API Access: {'Authenticated' if api_key else 'Access Denied'}")
    print(f"Log Level: {log_level}")
    print(f"Zion Network: {'Online' if zion_url else 'Offline'}")

    print("\nEnvironment security check:")

    env_in_gitignore = False
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            if ".env" in f.read():
                env_in_gitignore = True

    if not check_hardcoded_secrets(__file__):
        print("[FAIL] Hardcoded secret detected in source code!")
    else:
        print("[OK] No hardcoded secrets detected")

    if env_in_gitignore:
        print("[OK] .env file properly configured in .gitignore")
    else:
        print("[FAIL] .env file isn't properly configured in .gitignore")

    if mode == "production":
        print("[OK] Production overrides available")

    print("\nThe Oracle sees all configurations.")
