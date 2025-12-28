/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/30 18:04:02 by ottalhao          #+#    #+#             */
/*   Updated: 2025/12/06 22:20:19 by ottalhao         ###   ########.fr       */
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
}
/*
	Testing for memory leaks with:
		$ cc -Wall -Wextra -Werror -g main.c ../get_next_line.c ../get_next_line_utils.c -o gnl
		$ valgrind --leak-check=full --show-leak-kinds=all ./gnl
*/
