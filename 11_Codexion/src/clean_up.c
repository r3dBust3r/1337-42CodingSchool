/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   clean_up.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/31 18:10:18 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/31 18:10:25 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	clean_up(t_simulator *simulator)
{
	int	i;

	i = 0;
	while (i < simulator->config->number_of_coders)
	{
		pthread_mutex_destroy(&simulator->coders[i].mutex);
		pthread_mutex_destroy(&simulator->dongles[i].mutex);
		pthread_cond_destroy(&simulator->dongles[i].cond);
		free(simulator->dongles[i].requests);
		i++;
	}
	pthread_mutex_destroy(&simulator->print_mutex);
	pthread_mutex_destroy(&simulator->simulator_mutex);
	free(simulator->coders);
	free(simulator->dongles);
}
