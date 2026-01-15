print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===\n")

archive_name = "new_discovery.txt"
print(f"Initializing new storage unit: {archive_name}")
archive_file = open(archive_name, "w")
print("Storage unit created successfully...\n")

print("Inscribing preservation data...")
source_name = "ancient_fragment.txt"
source_file = open(source_name, "r")
source_content = source_file.read()
print(source_content)

archive_file.write(source_content)

archive_file.close()
source_file.close()

print("\nData inscription complete. Storage unit sealed.")
print(f"Archive '{archive_name}' ready for long-term preservation.")
