# Dup() / Dup2()

dup(): dup and dup2 let you duplicate file descriptors. Translation: you make one fd point to the same open file/pipe as another. Same file, same offset, same everything. Two numbers, one underlying thing.

```c
int dup(int oldfd);
```

Now:
    oldfd and newfd write to the same place
    Closing one does NOT close the other

dup2():
```c
int dup2(int oldfd, int newfd);
```

What it does (the important one)
    Forces newfd to become a duplicate of oldfd
    If newfd is open, it gets closed first
    After: newfd points to same thing as oldfd


```c
int fd = open("out.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
if (fd == -1)
    perror("open");

dup2(fd, STDOUT_FILENO); // STDOUT now goes to out.txt
close(fd);              // fd no longer needed

printf("Hello\n");      // goes into out.txt, not terminal
```