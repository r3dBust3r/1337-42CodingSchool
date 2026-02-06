# Read()

```c
ssize_t read(int fd, void *buf, size_t count);
```

- Return value
> 0 number of bytes read
> 0 EOF (end of file)
> -1 error


```c

char buffer[100];
ssize_t bytes = read(fd, buffer, 99);
if (bytes == -1)
    perror("read");
else
{
    buffer[bytes] = '\0';
    write(1, buffer, bytes); // print to stdout
}

```