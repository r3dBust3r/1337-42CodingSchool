/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   assign_indexes.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:17:05 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 12:28:59 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_list	*get_first_unindexed(t_list *lst)
{
	while (lst)
	{
		if (lst->index == -1)
			return (lst);
		lst = lst->next;
	}
	return (NULL);
}

t_list	*get_smallest_unindexed(t_list *lst)
{
	t_list	*smallest;

	smallest = get_first_unindexed(lst);
	while (lst)
	{
		if (lst->index == -1 && lst->n < smallest->n)
			smallest = lst;
		lst = lst->next;
	}
	return (smallest);
}

void	assign_indexes(t_list **lst)
{
	unsigned int	count;
	unsigned int	index;
	t_list			*smallest;

	count = count_lst(lst);
	index = 0;
	while (index < count)
	{
		smallest = get_smallest_unindexed(*lst);
		smallest->index = index;
		index++;
	}
}
