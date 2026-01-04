/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pswp_oprs_rot.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:03:57 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 12:45:15 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	rotate_stack(t_list **lst, char *operation)
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
	if (!str_empty(operation))
	{		
		ft_putstr_fd(operation, 1);
		ft_putstr_fd("\n", 1);
	}
}

void	rotate_stack_both(t_list **stack_a, t_list **stack_b)
{
	rotate_stack(stack_a, "");
	rotate_stack(stack_b, "");
	ft_putstr_fd("rr\n", 1);
}

void	rev_rotate_stack(t_list **lst, char *operation)
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
	if (!str_empty(operation))
	{
		ft_putstr_fd(operation, 1);
		ft_putstr_fd("\n", 1);
	}
}

void	rrr(t_list **stack_a, t_list **stack_b)
{
	rev_rotate_stack(stack_a, "");
	rev_rotate_stack(stack_b, "");
	ft_putstr_fd("rrr\n", 1);
}
