/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pswp_sort_4.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/04 11:38:53 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 11:59:42 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void pswp_sort_4(t_list **stack_a, t_list **stack_b)
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
	while (distance)
	{
		rotate_stack(stack_a, "ra");
		distance--;
	}
	push_stack(stack_a, stack_b, "pb");
	pswp_sort_3(stack_a);
	push_stack(stack_a, stack_b, "pa");
}
