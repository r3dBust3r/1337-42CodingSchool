### File Descriptors

When a program starts, **every process automatically gets 3 open file descriptors**
all connected to the console:

| FD  | Name       | Purpose                       | Default         |
| --- | ---------- | ----------------------------- | --------------- |
| `0` | **stdin**  | Standard Input (for reading)  | Keyboard        |
| `1` | **stdout** | Standard Output (for writing) | Screen/Terminal |
| `2` | **stderr** | Standard Error (for errors)   | Screen/Terminal |

```
          ┌─────────────────────────────────────┐
          │             Your Program            │
          └─────────────────────────────────────┘
                    │         │           │
                    │         │           │
                ┌───┴───┐ ┌───┴────┐ ┌────┴───┐
                │   0   │ │   1    │ │    2   │
                │ stdin │ │ stdout │ │ stderr │
                └───┬───┘ └───┬────┘ └────┬───┘
                    │         │          │
                    ▼         ▼          ▼
                 Keyboard   Screen     Screen
```

##### Examples
###### **stdin (FD = 0)**

Used for **input** (usually from the keyboard).

```c
char name[20];
read(0, name, sizeof(name));   // reads from stdin (keyboard)
```

You type something → it’s read from **FD 0**.

###### **stdout (FD = 1)**

Used for **normal program output** (goes to the screen).

```c
write(1, "Hello!\n", 7);       // writes to stdout (screen)
```

Displays “Hello!” on the console via **FD 1**.

###### **stderr (FD = 2)**

Used for **error messages**, separate from normal output.

```c
write(2, "Error: file not found\n", 22);
```

Prints an error message on the screen using **FD 2**,
even if stdout is redirected elsewhere (like to a file).

##### Then When You Open a File

```c
int fd = open("data.txt", O_RDONLY);
```

* Suppose `fd = 3` (next available number after 0, 1, 2).
* You can now `read(fd, ...)` or `write(fd, ...)`.

##### Summary

```
0 → stdin  → input  (keyboard)
1 → stdout → output (screen)
2 → stderr → errors (screen)
```

When you open new files, the OS assigns higher file descriptors:
**3, 4, 5, ..., 100, ...**

So, reading from a file and printing to the screen is like:

```
File (FD 3) → [buffer in memory] → Stdout (FD 1)
```

##### File Descriptors & Shell Redirection

| Symbol                | Meaning                         |
| --------------------- | ------------------------------- |
| `>`                   | Redirect stdout to a file       |
Example: `./prgm > out.txt` FD 1 (stdout) goes to `out.txt`

| Symbol                | Meaning                         |
| --------------------- | ------------------------------- |
| `<`                   | Redirect stdin from a file      |
Example: `./prgm < input.txt` FD 0 (stdin) reads from `input.txt`

| Symbol                | Meaning                         |
| --------------------- | ------------------------------- |
| `2>`                  | Redirect stderr to a file       |
Example: `./prgm 2> error.txt` FD 2 (stderr) goes to `error.txt`

| Symbol                | Meaning                         |
| --------------------- | ------------------------------- |
| `&>` or `> file 2>&1` | Redirect both stdout and stderr |
Example: `./prgm &> all.txt` or `./prgm > all.txt 2>&1` FD 1 and FD 2 both go to the same file |

##### Diagram for `./prgm > out.txt 2> error.txt`

```
      ┌───────────────────────┐
      │      Your Program     │
      └───────────────────────┘
              │         │
            FD [1]    FD [2]
              │         │
              ▼         ▼
         ┌─────────┐ ┌──────────┐
         │ out.txt │ │ error.txt│
         └─────────┘ └──────────┘
```

* Normally, FD 1 and FD 2 go to the screen.
* With redirection, FD 1 writes to `out.txt` and FD 2 writes to `error.txt`.

##### Diagram for `./prgm < input.txt > out.txt`

```
         input.txt
             │
       FD [0] (stdin)
             │
             ▼
   ┌───────────────────────┐
   │      Your Program     │
   └───────────────────────┘
             │
             │
       FD 1 (stdout)
             │
             ▼
           out.txt
```

* Now **stdin** comes from `input.txt` (FD 0) instead of the keyboard.
* **stdout** goes to `out.txt` (FD 1) instead of the terminal.


##### File Descriptor Table (FDT)
a **per-process table maintained by the operating system** that keeps track of all the **open files, sockets, pipes, or devices** for that process.

##### Structure (Simplified)

```
File Descriptor Table (per process)
+-----+---------------------+
| FD  | Pointer to File     |
+-----+---------------------+
| 0   | stdin (keyboard)    |
| 1   | stdout (screen)     |
| 2   | stderr (screen)     |
| 3   | data.txt (file)     |
| 4   | log.txt (file)      |
| ... | ...                 |
+-----+---------------------+
```

* **FD** = the number your program sees.
* **Pointer to File** = points to the **Open File Description** in the kernel, which has:
  * File position (current offset)
  * Mode (read/write)
  * Reference to inode or socket

##### Example

1. When you call `open("data.txt", O_RDONLY)`, the kernel:
   * Finds the next available FD (ex: 3).
   * Adds an entry in the **process’s FDT** pointing to the **kernel’s file description**.

2. When you `read(3, buffer, 100)`, the kernel:
   * Looks up FD 3 in the FDT.
   * Uses the file description to get the data and current offset.

3. When you `close(3)`, the kernel:
   * Removes the entry from the FDT.
   * If no other FD points to the same file description, it frees resources.


```
Process A
+--------------------------------------------------+
|               File Descriptor Table              |
+-----+--------------------------------------------+
| 0   | stdin pointer                              |
| 1   | stdout pointer                             |
| 2   | stderr pointer                             |
| 3   | pointer → Open File Description (data.txt) |
+-----+--------------------------------------------+

Kernel (Open File Description)
+-------------------+
| inode: data.txt   |
| mode: read-only   |
| offset: 0         |
+-------------------+
```

##### Creating our own file descriptor
`ls /proc/$$/fd` // list file descriptors in the sys
`exec 7>&1` // creating our custom fd
`exec 7>output-file.txt` // creating a symbolic link to our fd
`echo "hello" >&7` // redirecting the stdout to our custom fd
`cat output-file.txt` // doesn't need an explanation lol
