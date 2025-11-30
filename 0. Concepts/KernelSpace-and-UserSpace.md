### User Space vs Kernel Space

**Kernel Space**

* The part of memory where the operating system kernel runs.
* Has full control over the system (CPU, memory, devices).
* Runs in privileged mode (kernel mode).
* Contains device drivers, file system, process scheduler, etc.
* A crash here can bring down the entire system.

**User Space**

* The area of memory where user applications (e.g., browsers, editors) run.
* Runs in unprivileged mode (user mode).
* Programs cannot directly access hardware or kernel memory.
* Crashes only affect the application, not the OS.

**Interaction**

* Programs in user space request OS services through system calls (e.g., `read()`, `write()`, `open()`).
* The kernel performs the requested operation in kernel space and returns the result to user space.

**Summary Table**

```
| Aspect                        | User Space         | Kernel Space            |
| ----------------------------- | ------------------ | ----------------------- |
| What runs here                | User programs      | Operating system core   |
| Access level                  | Restricted         | Full (privileged)       |
| Can access hardware directly? | No                 | Yes                     |
| If it crashes...              | Only the app fails | Entire system may crash |
| Mode                          | User mode          | Kernel mode             |
```

a C/Python/PHP program runs entirely in user space, when it needs to perform I/O (like reading a file),
it requests the kernel to do it via a system call.
