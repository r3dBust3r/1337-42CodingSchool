/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/30 18:04:02 by ottalhao          #+#    #+#             */
/*   Updated: 2025/11/30 18:04:26 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../get_next_line.h"
#include <stdio.h>
#include <fcntl.h>

int	main(void)
{
	int i = 1;
	int fd = open("file_to_read.txt", O_RDONLY);
	char *line;
	while ((line = get_next_line(fd)))
	{
		printf("line #%d: %s", i++, line);
		free(line);
	}
	return 0;
	/*
		testing for memory leak with:
			1. cc -Wall -Wextra -Werror -g main.c ../get_next_line.c ../get_next_line_utils.c -o gnl
			2. valgrind --leak-check=full --show-leak-kinds=all ./gnl
	*/
}
