/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   assign_indexes.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:17:05 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/03 15:20:42 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	assign_indexes(ps_list **lst)
{
	unsigned int	count;
	unsigned int	index;
	unsigned int	i;
	ps_list			*smallest_node;
	ps_list			*current;

	count = count_lst(lst);
	index = 0;
	i = 0;
	while (i < count)
	{
		smallest_node = NULL;
		current = *lst;
		while (current)
		{
			if (current->index == -1)
			{
				smallest_node = current;
				break ;
			}
			current = current->next;
		}
		current = *lst;
		while (current)
		{
			if (current->index == -1)
			{
				if (current->n < smallest_node->n)
					smallest_node = current;
			}
			current = current->next;
		}
		smallest_node->index = index;
		index++;
		i++;
	}
}
