/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pipex.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/06 11:37:00 by ottalhao          #+#    #+#             */
/*   Updated: 2026/02/06 18:21:42 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "pipex.h"

int main(int ac, char **av)
{
    if (ac != 5)
    {
        printf("exactly 4 arguments needed!\n\n");
        return (1);
    }

    int fd[2];
    pipe(fd);

    // fd[0] -> pipe read
    // fd[1] -> pipe write

    char *file1 = av[1];
    char *cmd1 = av[2];
    char *cmd2 = av[3];
    char *file2 = av[4];

    pid_t pid = fork();
    if (pid == 0)
    {
        // Child: ls
        // Child has to write to pipe
        dup2(fd[1], STDOUT_FILENO);
        close(fd[0]);
        close(fd[1]);
        execlp(cmd1, cmd1, NULL);
    } else {
        // Parent: wc
        // Parent has to read from pipe
        dup2(fd[0], STDIN_FILENO);
        close(fd[0]);
        close(fd[1]);
        execlp(cmd2, cmd2, NULL);
    }



    // printf("hello world!\n");

    // char *file1 = av[1];
    // char *cmd1 = av[2];
    // char *cmd2 = av[3];
    // char *file2 = av[4];

    // int fd1 = open(file1, O_RDONLY);
    // dup2(fd1, 0);
    // close(fd1);
    
    // char buffer[100];
    // read(0, buffer, 100);

    // read(0, cmd, 4);
    
    // int fd2 = open(file2, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    // dup2(fd1, 0);

    // char *cmd = malloc(sizeof(char) * 4);

    // printf("%s", cmd);


// ssize_t read(int fd, void *buf, size_t count);


    // write(fd2, )

    // dup2(fd2, 1);
    // // close(fd2);

    // write(1, "aljsdkfhas23084729374q2983c923", 33);

    // if (fd1 == -1)
    // {
    //     perror("Open");
    //     return 1;
    // }

    // printf(">> %s opened successfuly!\n", file1);

    // int bffr_size = 500;

    // char *file1_content = malloc(sizeof(char) * bffr_size + 1);
    // read(fd1, file1_content, bffr_size);
    // printf("\n%s\n", file1_content);
    // file1_content[bffr_size] = '\0';

    // read(int fd, void *buf, size_t count)

    // TODO: ALL THE LOGIC!
    // printf("$> < %s %s | %s > %s\n\n", file1, cmd1, cmd2, file2);
    // $> < file1 cmd1 | cmd2 > file2

    // if (close(fd1) == -1)
    //     perror("Close");

    // if (close(fd2) == -1)
    //     perror("Close");

    return (0);
}


/**

    STDIN  -> 0 -> READ()  -> WRITE()
    STDOUT -> 1 -> WRITE() -> READ()

    PIPE READ():  fd[1]
    PIPE WRITE(): fd[0]

    === Pipex Algo ===

    command1 | command2
    child_pr | parent_pr

    - get command1
    - get command2
    - create a pipe
    - fork the process
    - child process do -> pid == 0:
        - dup STDOUT to pipe: fd[1] <-> STDOUT
        - Close both pipe ends
        - execve(command1)

    - parent process do -> pid != 0:
        - dup STDIN to pipe:  fd[0] <-> STDIN
        - Close both pipe ends
        - execve(command2)
        - waitpid(pid): Wait the child process

*/
