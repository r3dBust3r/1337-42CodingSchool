**Static library (.a / .lib):**

* Code is **copied into your program** at compile time.
* The executable becomes bigger but doesn’t need the library later.
* Changing the library means you must **recompile** your program.

**Dynamic library (.so / .dll):**

* Code is **loaded at runtime** (linked dynamically).
* The executable is smaller and can share the library with other programs.
* Updating the library doesn’t need recompiling — just replace the `.so` or `.dll`.
