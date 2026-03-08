/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/08 06:23:10 by ottalhao          #+#    #+#             */
/*   Updated: 2026/03/08 08:00:25 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "pipex.h"

void	free_array(char **arr)
{
	int	i;

	i = 0;
	while (arr[i])
	{
		free(arr[i]);
		i++;
	}
	free(arr);
}

char	*find_path(char *cmd, char **ep)
{
	char	**paths;
	char	*path;
	char	*part_path;
	int		i;

	i = 0;
	while (ep[i] && ft_strncmp(ep[i], "PATH=", 5) != 0)
		i++;
	if (!ep[i])
		return (NULL);
	paths = ft_split(ep[i] + 5, ':');
	i = 0;
	while (paths[i])
	{
		part_path = ft_strjoin(paths[i], "/");
		path = ft_strjoin(part_path, cmd);
		free(part_path);
		if (access(path, F_OK) == 0)
			return (free_array(paths), path);
		free(path);
		i++;
	}
	return (free_array(paths), NULL);
}

void	execute(char *av, char **ep)
{
	char	**cmd_args;
	char	*path;

	cmd_args = ft_split(av, ' ');
	if (!cmd_args)
		error_exit("split error");
	path = find_path(cmd_args[0], ep);
	if (!path)
	{
		free_array(cmd_args);
		error_exit("command not found");
	}
	if (execve(path, cmd_args, ep) == -1)
	{
		free(path);
		free_array(cmd_args);
		error_exit("execve error");
	}
}
