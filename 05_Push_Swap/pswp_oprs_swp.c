/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pswp_oprs_swp.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:03:57 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 11:31:27 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"


int str_empty(char *s)
{
	if (!s || s[0] == '\0')
		return 1;
	return 0;
}

void	swap_stack(t_list **lst, char *operation)
{
	if (count_lst(lst) < 2)
		return;
	t_list *first = *lst;
	t_list *second = (*lst)->next;
	first->next = second->next;
	second->next = first;
	*lst = second;
	if (!str_empty(operation))
	{
		ft_putstr_fd(operation, 1);
		ft_putstr_fd("\n", 1);
	}
}

void	swap_stack_both(t_list **stack_a, t_list **stack_b)
{
	swap_stack(stack_a, "");
	swap_stack(stack_b, "");
	ft_putstr_fd("ss\n", 1);
}