/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   grab_dongle.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/31 18:15:01 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/31 18:20:03 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	grab_one_dongle(t_coder *coder, t_dongle *dongle)
{
	long long	burn_out_time;
	int			scheduler;
	long long	current;
	t_request	req;

	scheduler = coder->simulator->config->scheduler;
	burn_out_time = coder->simulator->config->time_to_burnout;
	req.coder = coder;
	req.creation_time = get_time();
	pthread_mutex_lock(&coder->mutex);
	req.deadline = coder->last_compile + burn_out_time;
	pthread_mutex_unlock(&coder->mutex);
	pthread_mutex_lock(&dongle->mutex);
	pq_push(dongle, &req, scheduler);
	while ((!dongle->is_available) || (dongle->requests[0]->coder != coder))
		pthread_cond_wait(&dongle->cond, &dongle->mutex);
	pq_pop(dongle);
	dongle->is_available = 0;
	pthread_mutex_unlock(&dongle->mutex);
	current = get_time();
	if (current < dongle->available_at)
		ms_sleep(dongle->available_at - current);
	print_action(coder, "has taken a dongle");
}

void	grab_dongles(t_coder *coder)
{
	t_dongle	*first_dongle;
	t_dongle	*second_dongle;

	if (coder->id % 2 != 0)
	{
		first_dongle = coder->left_dongle;
		second_dongle = coder->right_dongle;
	}
	else
	{
		first_dongle = coder->right_dongle;
		second_dongle = coder->left_dongle;
	}
	grab_one_dongle(coder, first_dongle);
	grab_one_dongle(coder, second_dongle);
}
