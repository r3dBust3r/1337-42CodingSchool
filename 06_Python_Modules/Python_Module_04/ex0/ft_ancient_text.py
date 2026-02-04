print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===")

fname = "ancient_fragment.txt"

print(f"\nAccessing Storage Vault: {fname}")
print("Connection established...")
print("\nRECOVERED DATA:")

f = open(fname, "r")
print(f.read())
f.close()

print("\nData recovery complete. Storage unit disconnected.")
