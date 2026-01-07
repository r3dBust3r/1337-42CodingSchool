/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pswp_oprs_rot.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:03:57 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/07 10:07:32 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker.h"

void	rotate_stack(t_list **lst)
{
	t_list	*first;
	t_list	*second;
	t_list	*last;

	if (!lst || !*lst || !(*lst)->next)
		return ;
	first = *lst;
	second = (*lst)->next;
	last = *lst;
	while (last->next)
		last = last->next;
	last->next = first;
	first->next = NULL;
	*lst = second;
}

void	rotate_stack_both(t_list **stack_a, t_list **stack_b)
{
	rotate_stack(stack_a);
	rotate_stack(stack_b);
}

void	rev_rotate_stack(t_list **lst)
{
	t_list	*last;
	t_list	*second_last;

	if (!lst || !*lst || !(*lst)->next)
		return ;
	second_last = *lst;
	last = (*lst)->next;
	while (last->next)
	{
		second_last = last;
		last = last->next;
	}
	second_last->next = NULL;
	last->next = *lst;
	*lst = last;
}

void	rrr(t_list **stack_a, t_list **stack_b)
{
	rev_rotate_stack(stack_a);
	rev_rotate_stack(stack_b);
}
