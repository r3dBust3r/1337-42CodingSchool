# execve()

```c
int execve(char *path, char *argv[], char *envp[]);
```

What it really does

It replaces the current process image with a new program.

Not starts a new one.
Not returns on success.
It nukes your code and becomes the command.

If execve works, your code after it is gone.

```c
char *args[] = {"ls", "-l", NULL};

execve("/bin/ls", args, envp);
perror("execve"); // only runs if execve fails

```
After this:
- your program is now ls
- same PID
- same fds (after dup2 redirections)
- That’s why pipex works.

How this fits with pipe + fork + dup2

Child process:                  pid == 0
- dup2 to set stdin/stdout
- execve(cmd1)

Parent (or second child):       pid != 0
- dup2 to set stdin/stdout
- execve(cmd2)

Your code disappears. Only the commands remain. Like a real shell.

