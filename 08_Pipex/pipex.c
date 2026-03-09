/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pipex.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/06 11:37:00 by ottalhao          #+#    #+#             */
/*   Updated: 2026/03/09 15:24:07 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "pipex.h"

void	error_exit(char *msg)
{
	perror(msg);
	exit(1);
}

void	child1_process(char **av, char **ep, int *fd)
{
	int	infile;

	infile = open(av[1], O_RDONLY);
	if (infile == -1)
	{
		unlink(av[4]);
		error_exit("infile error");
	}
	dup2(infile, STDIN_FILENO);
	dup2(fd[1], STDOUT_FILENO);
	close(fd[0]);
	close(fd[1]);
	close(infile);
	execute(av[2], ep);
}

void	child2_process(char **av, char **ep, int *fd)
{
	int	outfile;

	outfile = open(av[4], O_WRONLY | O_CREAT | O_TRUNC, 0644);
	if (outfile == -1)
		error_exit("outfile error");
	dup2(fd[0], STDIN_FILENO);
	dup2(outfile, STDOUT_FILENO);
	close(fd[1]);
	close(fd[0]);
	close(outfile);
	execute(av[3], ep);
}

void	run_pipe(char **av, char **ep)
{
	int		fd[2];
	pid_t	pid1;
	pid_t	pid2;

	if (pipe(fd) == -1)
		error_exit("pipe error");
	pid1 = fork();
	if (pid1 == -1)
		error_exit("fork error");
	if (pid1 == 0)
		child1_process(av, ep, fd);
	pid2 = fork();
	if (pid2 == -1)
		error_exit("fork error");
	if (pid2 == 0)
		child2_process(av, ep, fd);
	close(fd[0]);
	close(fd[1]);
	waitpid(pid1, NULL, 0);
	waitpid(pid2, NULL, 0);
}

int	main(int ac, char **av, char **ep)
{
	if (ac == 5)
		run_pipe(av, ep);
	else
		write(2, "Usage: ./pipex file1 cmd1 cmd2 file2\n", 37);
	return (0);
}
