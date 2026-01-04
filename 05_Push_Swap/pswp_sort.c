/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pswp_sort.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:18:41 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 11:56:00 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void pswp_sort(t_list **stack_a, t_list **stack_b, unsigned int count)
{
	if (count == 2)
	{
		if ((*stack_a)->index > (*stack_a)->next->index)
			swap_stack_both(stack_a, stack_b);
	}
	else if (count == 3)
		pswp_sort_3(stack_a);
	else if (count == 4)
		pswp_sort_4(stack_a, stack_b);
	else if (count == 5)
		pswp_sort_5(stack_a, stack_b);
	else
	{
		int chunk_size;
		if (count < 100)
			chunk_size = count;
		else if (count < 300)
			chunk_size = count / 7;
		else
			chunk_size = count / 15;

		int pushed = 0;
		while (*stack_a)
		{
			if ((*stack_a)->index <= pushed)
			{
				push_stack(stack_a, stack_b, "pb");
				rotate_stack(stack_b, "rb");
				pushed++;
			}
			else if ((*stack_a)->index < pushed + chunk_size)
			{
				push_stack(stack_a, stack_b, "pb");
				pushed++;
			}
			else
				rotate_stack(stack_a, "ra");
		}

		while (*stack_b)
		{
			t_list *biggest_node = *stack_b;
			t_list *current = *stack_b;
			while (current) {
				if (current->index > biggest_node->index)
					biggest_node = current;
				current = current->next;
			}
			int distance = find_distance(*stack_b, biggest_node->n);
			if (distance <= count_lst(stack_b) / 2)
			{
				while (distance)	
				{
					rotate_stack(stack_b, "rb");
					distance--;
				}
			} else {
				distance = count_lst(stack_b) - distance;
				while (distance)
				{
					rev_rotate_stack(stack_b, "rrb");
					distance--;
				}
			}
			push_stack(stack_a, stack_b, "pa");
		}
	}
}
