/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pswp_oprs_rot.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:03:57 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 11:28:22 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	rotate_stack(t_list **lst, char* operation)
{
	if (count_lst(lst) < 2)
		return;
	t_list *first = *lst;
	t_list *second = (*lst)->next;
	t_list *last = *lst;
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
	int n_lst = count_lst(lst);
	if (n_lst < 2)
		return;
	t_list *last = *lst;
	while (last->next)
	    last = last->next;
	t_list *second_last = *lst;
	int i = 0;
	while (i < n_lst - 2)
	{
		second_last = second_last->next;
		i++;
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
