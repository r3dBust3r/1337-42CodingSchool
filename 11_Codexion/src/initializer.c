/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   initializer.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/31 18:17:49 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/31 18:18:04 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	init_dongles(t_config *config, t_simulator *sim)
{
	int	i;

	i = 0;
	while (i < config->number_of_coders)
	{
		sim->dongles[i].id = i + 1;
		sim->dongles[i].is_available = 1;
		sim->dongles[i].available_at = get_time();
		sim->dongles[i].queue_size = 0;
		sim->dongles[i].requests = malloc(sizeof(t_request *) * 2);
		pthread_mutex_init(&sim->dongles[i].mutex, NULL);
		pthread_cond_init(&sim->dongles[i].cond, NULL);
		i++;
	}
}

static void	init_coders(t_config *config, t_simulator *sim)
{
	int	i;

	i = 0;
	while (i < config->number_of_coders)
	{
		sim->coders[i].id = i + 1;
		sim->coders[i].compiles_completed = 0;
		sim->coders[i].left_dongle = &sim->dongles[i];
		sim->coders[i].right_dongle = &sim->dongles[(i + 1)
			% config->number_of_coders];
		sim->coders[i].simulator = sim;
		pthread_mutex_init(&sim->coders[i].mutex, NULL);
		i++;
	}
}

int	initializer(t_config *config, t_simulator *sim)
{
	sim->dongles = malloc(sizeof(t_dongle) * config->number_of_coders);
	if (!sim->dongles)
		return (1);
	sim->coders = malloc(sizeof(t_coder) * config->number_of_coders);
	if (!sim->coders)
	{
		free(sim->dongles);
		return (1);
	}
	sim->is_running = 1;
	sim->config = config;
	pthread_mutex_init(&sim->print_mutex, NULL);
	pthread_mutex_init(&sim->simulator_mutex, NULL);
	init_dongles(config, sim);
	init_coders(config, sim);
	return (0);
}
