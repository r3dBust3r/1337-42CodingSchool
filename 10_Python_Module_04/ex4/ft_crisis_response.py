print("=== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===\n")

lost_archive = "lost_archive.txt"
try:
    print(f"CRISIS ALERT: Attempting access to '{lost_archive}'...")
    with open(lost_archive, "r") as f_name:
        pass
except FileNotFoundError:
    print("RESPONSE: Archive not found in storage matrix")
    print("STATUS: Crisis handled, system stable")

classified_vault = "classified_vault.txt"
print()
try:
    print(f"CRISIS ALERT: Attempting access to '{classified_vault}'...")
    with open(classified_vault, "r") as f_name:
        pass
except PermissionError:
    print("RESPONSE: Security protocols deny access")
    print("STATUS: Crisis handled, security maintained")

standard_archive = "standard_archive.txt"
print()
try:
    print(f"ROUTINE ACCESS: Attempting access to '{standard_archive}'...")
    with open(standard_archive, "r") as f_name:
        print(f"SUCCESS: Archive recovered - '{f_name.read()}'")
except Exception:
    pass

print("\nAll crisis scenarios handled successfully. Archives secure.")
