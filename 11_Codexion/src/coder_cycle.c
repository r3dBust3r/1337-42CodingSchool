/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder_cycle.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/31 18:16:37 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/31 18:16:49 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	check_continue(t_coder *coder)
{
	int	current_compiles;
	int	req_compiles;

	req_compiles = coder->simulator->config->required_compiles;
	pthread_mutex_lock(&coder->mutex);
	current_compiles = coder->compiles_completed;
	pthread_mutex_unlock(&coder->mutex);
	if (req_compiles != -1 && current_compiles >= req_compiles)
		return (0);
	pthread_mutex_lock(&coder->simulator->simulator_mutex);
	if (!coder->simulator->is_running)
	{
		pthread_mutex_unlock(&coder->simulator->simulator_mutex);
		return (0);
	}
	pthread_mutex_unlock(&coder->simulator->simulator_mutex);
	return (1);
}

void	*coder_cycle(void *arg)
{
	t_coder	*coder;

	coder = (t_coder *)arg;
	if (coder->simulator->config->number_of_coders == 1)
	{
		handle_single_coder(coder);
		return (NULL);
	}
	if (coder->id % 2 == 0)
		ms_sleep(10);
	while (check_continue(coder))
	{
		grab_dongles(coder);
		do_compile(coder);
		release_dongles(coder);
		do_debug(coder);
		do_refactor(coder);
		pthread_mutex_lock(&coder->mutex);
		coder->compiles_completed += 1;
		pthread_mutex_unlock(&coder->mutex);
	}
	return (NULL);
}
