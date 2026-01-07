/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pswp_oprs_swp.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:03:57 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/07 10:07:35 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker.h"

int	str_empty(char *s)
{
	if (!s || s[0] == '\0')
		return (1);
	return (0);
}

void	swap_stack(t_list **lst)
{
	t_list	*first;
	t_list	*second;

	if (count_lst(lst) < 2)
		return ;
	first = *lst;
	second = (*lst)->next;
	first->next = second->next;
	second->next = first;
	*lst = second;
}

void	swap_stack_both(t_list **stack_a, t_list **stack_b)
{
	swap_stack(stack_a);
	swap_stack(stack_b);
}
