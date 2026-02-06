# Write()

```c
ssize_t write(int fd, const void *buf, size_t count);
```

```c
char *msg = "Hello Pipex\n";
if (write(1, msg, 12) == -1) // 1 = stdout
    perror("write");
```
| FD | Meaning |
| -- | ------- |
| 0  | stdin   |
| 1  | stdout  |
| 2  | stderr  |


`write(1, "OK\n", 3);`  # prints to terminal
`write(2, "ERR\n", 4);` # prints to error output

