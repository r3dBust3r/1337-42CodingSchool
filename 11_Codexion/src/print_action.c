/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_action.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/31 18:11:16 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/31 18:11:28 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	print_action(t_coder *coder, char *action)
{
	long long	action_time;
	int			safe_to_print;

	pthread_mutex_lock(&coder->simulator->simulator_mutex);
	if (!coder->simulator->is_running)
	{
		pthread_mutex_unlock(&coder->simulator->simulator_mutex);
		return ;
	}
	pthread_mutex_unlock(&coder->simulator->simulator_mutex);
	action_time = get_time() - coder->simulator->start_time;
	pthread_mutex_lock(&coder->simulator->print_mutex);
	pthread_mutex_lock(&coder->simulator->simulator_mutex);
	safe_to_print = coder->simulator->is_running;
	pthread_mutex_unlock(&coder->simulator->simulator_mutex);
	if (safe_to_print)
		printf("%lld %d %s\n", action_time, coder->id, action);
	pthread_mutex_unlock(&coder->simulator->print_mutex);
}
