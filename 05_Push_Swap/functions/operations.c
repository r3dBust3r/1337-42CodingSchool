/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   operations.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:03:57 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/03 15:32:24 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	swap_stack(ps_list **lst, char *operation)
{
	ps_list	*first;
	ps_list	*second;

	if (count_lst(lst) < 2)
		return ;
	first = *lst;
	second = (*lst)->next;
	first->next = second->next;
	second->next = first;
	*lst = second;
	ft_putstr_fd(operation, 1);
	ft_putstr_fd("\n", 1);
}

void	swap_stack_both(ps_list **stack_a, ps_list **stack_b)
{
	swap_stack(stack_a, "sa");
	swap_stack(stack_b, "sb");
}

void	push_stack(ps_list **stack_a, ps_list **stack_b, char *operation)
{
	ps_list	*node_to_push;

	if (operation == "pa")
	{
		if (count_lst(stack_b) == 0)
			return ;
		node_to_push = *stack_b;
		*stack_b = (*stack_b)->next;
		node_to_push->next = *stack_a;
		*stack_a = node_to_push;
		ft_putstr_fd("pa\n", 1);
	}
	else
	{
		if (count_lst(stack_a) == 0)
			return ;
		node_to_push = *stack_a;
		*stack_a = (*stack_a)->next;
		node_to_push->next = *stack_b;
		*stack_b = node_to_push;
		ft_putstr_fd("pb\n", 1);
	}
}

void	rotate_stack(ps_list **lst, char *operation)
{
	ps_list	*first;
	ps_list	*second;
	ps_list	*last;

	if (count_lst(lst) == 0)
		return ;
	first = *lst;
	second = (*lst)->next;
	last = *lst;
	while (last->next)
		last = last->next;
	last->next = first;
	first->next = NULL;
	*lst = second;
	ft_putstr_fd(operation, 1);
	ft_putstr_fd("\n", 1);
}

void	rotate_stack_both(ps_list **stack_a, ps_list **stack_b)
{
	rotate_stack(stack_a, "ra");
	rotate_stack(stack_b, "rb");
}

void	rev_rotate_stack(ps_list **lst, char *operation)
{
	ps_list	*last;
	ps_list	*second_last;
	int		i;
	int		n_lst;

	n_lst = count_lst(lst);
	if (n_lst < 2)
		return ;
	last = *lst;
	while (last->next)
		last = last->next;
	second_last = *lst;
	i = 0;
	while (i < n_lst - 2)
	{
		second_last = second_last->next;
		i++;
	}
	second_last->next = NULL;
	last->next = *lst;
	*lst = last;
	ft_putstr_fd(operation, 1);
	ft_putstr_fd("\n", 1);
}

void	rrr(ps_list **stack_a, ps_list **stack_b)
{
	rev_rotate_stack(stack_a, "rra");
	rev_rotate_stack(stack_b, "rrb");
}
