/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pswp_sort_5.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/04 11:39:47 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 14:23:28 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	rotate_to_top(t_list **stack, t_list *node)
{
	int		distance;
	char	*operation;

	distance = find_distance(*stack, node->n);
	operation = "ra";
	if (distance > 2)
	{
		distance = count_lst(stack) - distance;
		operation = "rra";
	}
	while (distance)
	{
		if (operation[1] == 'a')
			rotate_stack(stack, "ra");
		else
			rev_rotate_stack(stack, "rra");
		distance--;
	}
}

static void	push_smallest_to_b(t_list **stack_a, t_list **stack_b)
{
	t_list	*smallest;
	t_list	*current;

	smallest = *stack_a;
	current = *stack_a;
	while (current)
	{
		if (current->index < smallest->index)
			smallest = current;
		current = current->next;
	}
	rotate_to_top(stack_a, smallest);
	push_stack(stack_a, stack_b, "pb");
}

void	pswp_sort_5(t_list **stack_a, t_list **stack_b)
{
	push_smallest_to_b(stack_a, stack_b);
	push_smallest_to_b(stack_a, stack_b);
	pswp_sort_3(stack_a);
	push_stack(stack_a, stack_b, "pa");
	push_stack(stack_a, stack_b, "pa");
}
