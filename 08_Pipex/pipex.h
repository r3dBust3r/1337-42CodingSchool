/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pipex.h                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/06 11:41:52 by ottalhao          #+#    #+#             */
/*   Updated: 2026/03/09 03:21:11 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PIPEX_H
# define PIPEX_H

# include <unistd.h>
# include <stdio.h>
# include <stdlib.h>
# include <fcntl.h>
# include <sys/wait.h>

char	**ft_split(const char *s, char c);
int		ft_strncmp(const char *s1, const char *s2, size_t n);
char	*ft_strjoin(char const *s1, char const *s2);

void	execute(char *av, char **ep);
void	child_process(char **av, char **ep, int *fd);
void	parent_process(char **av, char **ep, int *fd);
void	error_exit(char *msg);
char	*find_path(char *cmd, char **ep);
void	free_array(char **arr);

#endif
