# Fork()

`pid_t fork(void);`

fork() clones your process.
After fork, you have:
Process A (child)  -> cmd1 (writer)
Process B (parent) -> cmd2 (reader)

Now:
    cmd1 can write
    cmd2 can read
at the same time

How shells really think

The shell does NOT do:
    runs cmd1 then cmd2

It does:
    runs cmd1 AND cmd2 together, connected by a pipe


```c
pid_t pid = fork();

if (pid == 0)
{
    // CHILD Process
}
else
{
    // PARENT Process
}
```

| Where you are  | fork() returns | Meaning                |
| -------------- | -------------- | ---------------------- |
| Child process  | `0`            | “I am the child”       |
| Parent process | `> 0`          | “I created a child”    |
| Error          | `-1`           | “No child, OS unhappy” |
