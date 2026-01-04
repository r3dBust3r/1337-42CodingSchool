/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   assign_indexes.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:17:05 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 11:35:01 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void assign_indexes(t_list **lst)
{
	unsigned int count = count_lst(lst);
	unsigned int index = 0;
	unsigned int i = 0;
	while (i < count)
	{
		t_list *smallest_node = NULL;
		t_list *current = *lst;
		while (current)
		{
			if (current->index == -1)
			{
				smallest_node = current;
				break;
			}
			current = current->next;
		}
		current = *lst;
		while (current)
		{
			if (current->index == -1)
			{
				if (current->n < smallest_node->n)
				{
					smallest_node = current;
				}
			}
			current = current->next;
		}
		smallest_node->index = index;
		index++;
		i++;
	}
}