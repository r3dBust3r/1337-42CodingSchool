from sys import stdin, stdout, stderr

stdout.write("=== CYBER ARCHIVES - COMMUNICATION SYSTEM ===\n\n")

stdout.write("Input Stream active. Enter archivist ID: ")
stdout.flush()
archivist_id = stdin.readline().strip()

stdout.write("Input Stream active. Enter status report: ")
stdout.flush()
report_status = stdin.readline().strip()

stdout.write(
    f"\n[STANDARD] Archive status from {archivist_id}: {report_status}\n"
)
stderr.write("[ALERT] System diagnostic: Communication channels verified\n")
stdout.write("[STANDARD] Data transmission complete\n\n")

stdout.write("Three-channel communication test successful.\n")
