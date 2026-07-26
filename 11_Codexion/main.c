/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 17:46:23 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/26 22:08:58 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	main(int c, char **av)
{
	if (c != 9)
		return (print_usage());

	t_config *config = malloc(sizeof(t_config));
	if (!config)
		return (1);

	if (parser(c, av, config))
		return (1);

	printf("config->number_of_coders: %d\n", config->number_of_coders);
	printf("config->time_to_burnout: %d\n", config->time_to_burnout);
	printf("config->time_to_compile: %d\n", config->time_to_compile);
	printf("config->time_to_debug: %d\n", config->time_to_debug);
	printf("config->time_to_refactor: %d\n", config->time_to_refactor);
	printf("config->number_of_compiles_required: %d\n", config->number_of_compiles_required);
	printf("config->dongle_cooldown: %d\n", config->dongle_cooldown);
	printf("config->scheduler: %d\n", config->scheduler);

	clean_config(config);
	return (0);
}
