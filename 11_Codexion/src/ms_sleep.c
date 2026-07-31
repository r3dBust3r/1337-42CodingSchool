/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ms_sleep.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/31 18:10:42 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/31 18:10:56 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	ms_sleep(long long time_in_ms)
{
	long long	start;

	start = get_time();
	while (get_time() - start < time_in_ms)
		usleep(100);
}
