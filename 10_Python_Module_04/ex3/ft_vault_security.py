print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===\n")

print("Initiating secure vault access...")
with open("classified_data.txt", "r") as f_name:
    print("Vault connection established with failsafe protocols\n")
    print("SECURE EXTRACTION:")
    print(f_name.read())

print()
with open("security_protocols.txt", "w") as vault_file:
    print("SECURE PRESERVATION:")
    data = "[CLASSIFIED] New security protocols archived"
    vault_file.write(data)
    print(data)
    print("Vault automatically sealed upon completion")

print("\nAll vault operations completed with maximum security.")
