/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   priority_queue.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/31 18:12:01 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/31 18:12:12 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	pq_push(t_dongle *dongle, t_request *req, int scheduler)
{
	int			swap;
	t_request	*r0;
	t_request	*r1;

	dongle->requests[dongle->queue_size] = req;
	if (dongle->queue_size == 1)
	{
		swap = 0;
		r0 = dongle->requests[0];
		r1 = dongle->requests[1];
		if (scheduler == 0 && r0->creation_time > r1->creation_time)
			swap = 1;
		else if (scheduler != 0 && r0->deadline > r1->deadline)
			swap = 1;
		if (swap)
		{
			dongle->requests[0] = r1;
			dongle->requests[1] = r0;
		}
	}
	dongle->queue_size++;
}

t_request	*pq_pop(t_dongle *dongle)
{
	t_request	*popped;

	if (dongle->queue_size == 0)
		return (NULL);
	popped = dongle->requests[0];
	if (dongle->queue_size == 2)
		dongle->requests[0] = dongle->requests[1];
	dongle->queue_size--;
	return (popped);
}
