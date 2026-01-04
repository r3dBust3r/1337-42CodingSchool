/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pswp_sort_5.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/04 11:39:47 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 12:00:01 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	pswp_sort_5(t_list **stack_a, t_list **stack_b)
{
	int	i = 2;
	while (i)
	{
		t_list *smallest_node = *stack_a;
		t_list *current = *stack_a;
		while (current)
		{
			if (current->index < smallest_node->index)
				smallest_node = current;
			current = current->next;
		}
		int distance = find_distance(*stack_a, smallest_node->n);
		char *operation = "ra";
		if (distance > 2)
		{
			distance = count_lst(stack_a) - distance;
			operation = "rra";
		}
		while (distance)
		{
			if (operation[0] == 'r' && operation[1] == 'a')
				rotate_stack(stack_a, "ra");
			else
				rev_rotate_stack(stack_a, "rra");
			distance--;
		}
		push_stack(stack_a, stack_b, "pb");
		i--;
	}
	pswp_sort_3(stack_a);
	push_stack(stack_a, stack_b, "pa");
	push_stack(stack_a, stack_b, "pa");
}
