1. **Preprocessing** (`cpp`)

   * The compiler first expands macros (`#define`), includes header files (`#include`), and removes comments.
   * It’s like a janitor sweeping up your messy code before the real work begins.
   * Command example:

     ```bash
     gcc -E file.c -o file.i
     ```

     Output: a human-readable but bloated file full of expanded macros and includes.

2. **Compilation** (`cc1`)

   * The preprocessed code is then translated into **assembly** — actual low-level instructions for your CPU architecture.
   * Syntax errors? They’re caught here. This is where your typos go to die.
   * Command example:

     ```bash
     gcc -S file.i -o file.s
     ```

     Output: `file.s` (assembly code).

3. **Assembly** (`as`)

   * The assembly file is converted into **object code** (machine code, but not yet executable).
   * It’s basically raw binary gibberish the CPU loves, but it can’t run alone.
   * Command example:

     ```bash
     gcc -c file.s -o file.o
     ```

     Output: `file.o` (object file).

4. **Linking** (`ld`)

   * All object files (`.o`) and libraries are stitched together into one **executable**.
   * This is where external functions like `printf()` get connected to their actual code in the standard library.
   * Command example:

     ```bash
     gcc file.o -o file
     ```

     Output: an executable named `file`.

So the full magical pipeline is:

```
Preprocessing → Compilation → Assembly → Linking
```

Or, for short:

```
.c → .i → .s → .o → (executable)
```

- ASCII Presentation

```
   +--------------------+
   | file.c (source)    |
   +--------------------+
              | gcc -E file.c -o file.i
              v
   +--------------------+
   | Preprocessor (.i)  |
   | expands #include   |
   | and #define        |
   +--------------------+
              | gcc -S file.i -o file.s
              v
   +--------------------+
   | Compiler (.s)      |
   | turns code into    |
   | assembly language  |
   +--------------------+
              | gcc -c file.s -o file.o
              v
   +--------------------+
   | Assembler (.o)     |
   | converts assembly  |
   | to machine code    |
   +--------------------+
              | gcc file.s -o program
              v
   +--------------------+
   | Linker (executable)|
   | joins .o + libs    |
   +--------------------+
              |
              v
   +--------------------+
   | a.out / program    |
   +--------------------+

             ↓
       ./program runs
             ↓
     Segmentation fault :)
```
