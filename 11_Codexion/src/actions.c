/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   actions.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/31 18:15:35 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/31 18:15:50 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	do_compile(t_coder *coder)
{
	pthread_mutex_lock(&coder->mutex);
	coder->last_compile = get_time();
	pthread_mutex_unlock(&coder->mutex);
	print_action(coder, "is compiling");
	ms_sleep(coder->simulator->config->time_to_compile);
}

void	release_dongles(t_coder *coder)
{
	int			cooldown;
	t_dongle	*left_dongle;
	t_dongle	*right_dongle;

	cooldown = coder->simulator->config->dongle_cooldown;
	left_dongle = coder->left_dongle;
	right_dongle = coder->right_dongle;
	pthread_mutex_lock(&left_dongle->mutex);
	left_dongle->is_available = 1;
	left_dongle->available_at = get_time() + cooldown;
	pthread_cond_broadcast(&left_dongle->cond);
	pthread_mutex_unlock(&left_dongle->mutex);
	pthread_mutex_lock(&right_dongle->mutex);
	right_dongle->is_available = 1;
	right_dongle->available_at = get_time() + cooldown;
	pthread_cond_broadcast(&right_dongle->cond);
	pthread_mutex_unlock(&right_dongle->mutex);
}

void	do_debug(t_coder *coder)
{
	print_action(coder, "is debugging");
	ms_sleep(coder->simulator->config->time_to_debug);
}

void	do_refactor(t_coder *coder)
{
	print_action(coder, "is refactoring");
	ms_sleep(coder->simulator->config->time_to_refactor);
}
