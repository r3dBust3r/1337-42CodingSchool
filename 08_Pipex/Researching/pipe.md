# Pipe()

pipe() is where you stop thinking in files and start thinking in plumbing. Literally.

A pipe is just a kernel buffer with two ends:
one end you write to
one end you read from

```c
int pipe(int fd[2]);
```

it gives us after:
```c
int fd[2];
pipe(fd);
```

| fd index | Meaning   |
| -------- | --------- |
| fd[0]    | READ end  |
| fd[1]    | WRITE end |

So:
`write(fd[1], ...)` → goes into pipe
`read(fd[0], ...)`  → comes out

We write to fd[1], then we read from fd[0]
`write(fd[1], bffr, bffr_size);`
`read(fd[0], bffr, bffr_size);`

```c
int fd[2];
char buf[100];

pipe(fd);

write(fd[1], "Hello\n", 6); // we write to the pipe bffr 
close(fd[1]);               // we close the fd, important

read(fd[0], buf, 100);      // we read from the pipe bffr
write(1, buf, 6);           // we write to stdout bffr

close(fd[0]);               // we close the fd
```
