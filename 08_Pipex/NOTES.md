## Functions I need to know
- [+] open: Open a file and get a file descriptor.
- [+] read: Read bytes from a fd into a buffer.
- [+] write: Write bytes from a buffer to a fd.
- [+] close: Close a file descriptor and free OS resources.

- [+] malloc: Allocate heap memory.
- [+] free: Free previously allocated heap memory.

- [+] perror: Print last error message to stderr.
- [ ] strerror: Return error message string from errno.
- [ ] access: Check file existence/permissions.

- [+] dup: Duplicate a fd to a new fd number.
- [+] dup2: Duplicate a fd to a specific fd number.

- [+] execve: Replace current process with a new program.
- [+] exit: Terminate the current process with a status code.

- [+] fork: Create a child process (clone).
- [+] pipe: Create a unidirectional data channel (read/write fds).

- [ ] unlink: Delete a file from the filesystem.

- [+] wait: Wait for any child process to finish.
- [+] waitpid: Wait for a specific child process to finish.

---------

## Common 42 mistakes for this project
- [ ] Forgetting to close() unused fds after dup2
- [ ] Using dup() when you need a specific fd
- [ ] Forgetting that dup2 closes newfd automatically
- [ ] Not checking return values and then crying in moulinette

