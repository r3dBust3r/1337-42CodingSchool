/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   single_coder.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/31 18:16:17 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/31 18:16:27 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	handle_single_coder(t_coder *coder)
{
	pthread_mutex_lock(&coder->left_dongle->mutex);
	print_action(coder, "has taken a dongle");
	pthread_mutex_unlock(&coder->left_dongle->mutex);
	ms_sleep(coder->simulator->config->time_to_burnout + 10);
}
