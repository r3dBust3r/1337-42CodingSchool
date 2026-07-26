/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parser.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 18:15:09 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/26 22:06:55 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int parser(int c, char **av, t_config *config)
{
	int i;
    int n;

    n = 0;
    i = 1;
	while (i < c - 1)
	{
		n = ft_atol(av[i]);
        if (n == -1)
        {
            print_usage();
            return (clean_config(config));
        }

        if (i == 1) config->number_of_coders = n;
        if (i == 2) config->time_to_burnout = n;
        if (i == 3) config->time_to_compile = n;
        if (i == 4) config->time_to_debug = n;
        if (i == 5) config->time_to_refactor = n;
        if (i == 6) config->number_of_compiles_required = n;
        if (i == 7) config->dongle_cooldown = n;

        i++;
    }

    if (strcmp(av[i], "fifo") != 0 && strcmp(av[i], "edf") != 0)
    {
        fprintf(stderr, "Error: Scheduler is one of (fifo, edf)\n");
        return (clean_config(config));
    }

    config->scheduler = (strcmp(av[i], "fifo") == 0) ? 0 : 1;

	return (0);
}
