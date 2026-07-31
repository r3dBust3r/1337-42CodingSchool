/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/31 18:17:19 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/31 18:17:39 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	start_threads(t_simulator *sim)
{
	int	i;

	sim->start_time = get_time();
	i = 0;
	while (i < sim->config->number_of_coders)
	{
		sim->coders[i].last_compile = sim->start_time;
		if (pthread_create(&sim->coders[i].thread_id, NULL,
				coder_cycle, &sim->coders[i]) != 0)
			return (1);
		i++;
	}
	return (0);
}

static int	check_coder_status(t_simulator *sim, t_coder *coder, int *finished)
{
	long long	current;
	int			req;

	req = sim->config->required_compiles;
	pthread_mutex_lock(&coder->mutex);
	current = get_time();
	if ((coder->compiles_completed < req || req == -1)
		&& (current - coder->last_compile >= sim->config->time_to_burnout))
	{
		pthread_mutex_lock(&sim->simulator_mutex);
		sim->is_running = 0;
		pthread_mutex_unlock(&sim->simulator_mutex);
		pthread_mutex_lock(&sim->print_mutex);
		printf("%lld %d burned out\n", current - sim->start_time, coder->id);
		pthread_mutex_unlock(&sim->print_mutex);
		pthread_mutex_unlock(&coder->mutex);
		return (1);
	}
	if (req != -1 && coder->compiles_completed >= req)
		(*finished)++;
	pthread_mutex_unlock(&coder->mutex);
	return (0);
}

static void	monitor_loop(t_simulator *sim)
{
	int	i;
	int	finished;

	while (1)
	{
		i = 0;
		finished = 0;
		while (i < sim->config->number_of_coders)
		{
			if (check_coder_status(sim, &sim->coders[i], &finished))
				return ;
			i++;
		}
		if (sim->config->required_compiles != -1
			&& finished == sim->config->number_of_coders)
		{
			pthread_mutex_lock(&sim->simulator_mutex);
			sim->is_running = 0;
			pthread_mutex_unlock(&sim->simulator_mutex);
			return ;
		}
		usleep(1000);
	}
}

void	run_simulation(t_simulator *sim)
{
	int	i;

	if (start_threads(sim))
		return ;
	monitor_loop(sim);
	i = 0;
	while (i < sim->config->number_of_coders)
	{
		pthread_join(sim->coders[i].thread_id, NULL);
		i++;
	}
}
