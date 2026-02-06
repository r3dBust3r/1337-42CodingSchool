# wait() and waitpid()

Without waiting, you get:
- zombie processes
- moulinette yelling
- OS side-eye


## wait()
Waits for any child to finish.

```c
pid_t wait(int *status);

```

---

## waitpid()
Waits for a specific child.
```c
pid_t waitpid(pid_t pid, int *status, int options);
```

Pipex usually uses waitpid.
example:
```c
int status;
waitpid(pid, &status, 0);
```

This means:
- Parent waits until child pid finishes.


Why wait matters in pipex
- To avoid zombies
- To get correct exit status
- To behave like a real shell

Even if pipe still works without it, your program is technically sloppy. Unix remembers.

