/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parser.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 18:15:09 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/31 19:02:06 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	set_config_value(t_config *config, int i, int n)
{
	if (i == 1)
		config->number_of_coders = n;
	else if (i == 2)
		config->time_to_burnout = n;
	else if (i == 3)
		config->time_to_compile = n;
	else if (i == 4)
		config->time_to_debug = n;
	else if (i == 5)
		config->time_to_refactor = n;
	else if (i == 6)
		config->required_compiles = n;
	else if (i == 7)
		config->dongle_cooldown = n;
}

int	parser(int c, char **av, t_config *config)
{
	int	i;
	int	n;

	i = 1;
	while (i < c - 1)
	{
		n = ft_atol(av[i]);
		if (n == -1)
			return (print_usage());
		if (i == 1 && n <= 0)
			return (print_usage());
		set_config_value(config, i, n);
		i++;
	}
	if (strcmp(av[i], "fifo") != 0 && strcmp(av[i], "edf") != 0)
		return (print_usage());
	if (strcmp(av[i], "fifo") == 0)
		config->scheduler = 0;
	else
		config->scheduler = 1;
	return (0);
}
