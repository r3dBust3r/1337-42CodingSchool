/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   find_distance.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:16:30 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 11:34:24 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	find_distance(t_list *lst, int n)
{
	int i = 0;
	while (lst)
	{
		if (lst->n == n)
			break;
		lst = lst->next;
		i++;
	}
	return i;
}
