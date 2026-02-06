# Open()

- open
```c
int open(const char *pathname, int flags, mode_t mode);
```
Modes:
- `O_RDONLY` read only
- `O_WRONLY` write only
- `O_RDWR` read + write
- `O_CREAT` create if not exists
- `O_TRUNC` truncate (empty) file
- `O_APPEND` append to end


---


- close
```c
int close(int fd);
```
close a file descriptor
```c
int fd = 1;
close(fd);

```
