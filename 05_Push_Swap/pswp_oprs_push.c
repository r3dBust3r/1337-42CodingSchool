/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pswp_oprs_push.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/04 11:32:51 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 11:33:09 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	push_stack(t_list **stack_a, t_list **stack_b, char *operation)
{
	if (operation[0] == 'p' && operation[1] == 'a')
	{
		if (count_lst(stack_b) == 0)
			return;
		t_list *node_to_push = *stack_b;
		*stack_b = (*stack_b)->next;
		node_to_push->next = *stack_a;
		*stack_a = node_to_push;
		ft_putstr_fd("pa\n", 1);
	}
	else
	{
		if (count_lst(stack_a) == 0)
			return;
		t_list *node_to_push = *stack_a;
		*stack_a = (*stack_a)->next;
		node_to_push->next = *stack_b;
		*stack_b = node_to_push;
		ft_putstr_fd("pb\n", 1);
	}
}