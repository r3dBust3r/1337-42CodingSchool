/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pswp_sort.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:18:41 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/03 19:14:32 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void pswp_sort(ps_list **stack_a, ps_list **stack_b, unsigned int count)
{
	if (count == 2)
	{
		if ((*stack_a)->index > (*stack_a)->next->index)
			swap_stack_both(stack_a, stack_b);
	}
	else if (count == 3)
	{
		pswp_sort_3(stack_a, stack_b);
	}
	else if (count == 4)
	{
		ps_list *smallest_node = *stack_a;
		ps_list *current = *stack_a;
		while (current)
		{
			if (current->index < smallest_node->index)
			{
				smallest_node = current;
			}
			current = current->next;
		}
		int distance = find_distance(*stack_a, smallest_node->n);
		while (distance)
		{
			rotate_stack(stack_a, "ra");
			distance--;
		}
		push_stack(stack_a, stack_b, "pb");
		pswp_sort_3(stack_a, stack_b);
		push_stack(stack_a, stack_b, "pa");
	}
	else if (count == 5)
	{
		int i = 2;
		while (i)
		{
			ps_list *smallest_node = *stack_a;
			ps_list *current = *stack_a;
			while (current)
			{
				if (current->index < smallest_node->index)
				{
					smallest_node = current;
				}
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
				if (operation == "ra")
					rotate_stack(stack_a, "ra");
				else
					rev_rotate_stack(stack_a, "rra");
				distance--;
			}
			push_stack(stack_a, stack_b, "pb");
			i--;
		}
		pswp_sort_3(stack_a, stack_b);
		push_stack(stack_a, stack_b, "pa");
		push_stack(stack_a, stack_b, "pa");
	}
	else
	{
		int chunk_size = (count <= 100) ? (count / 7) : (count / 15);
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
			{
				rotate_stack(stack_a, "ra");
			}
		}
		
		while (*stack_b)
		{
			// TODO: find the biggest node
			ps_list *biggest_node = *stack_b;
			ps_list *current = *stack_b;
			while (current) {
				if (current->index > biggest_node->index)
					biggest_node = current;
				current = current->next;
			}

			// TODO: Find its distance
			int distance = find_distance(*stack_b, biggest_node->n);
			
			// TODO: move it to the top of B
			if (distance <= count_lst(stack_b) / 2) {
				// TODO: move with RB
				int i = 0;
				while (i < distance)	
				{
					rotate_stack(stack_b, "rb");
					i++;
				}
			} else {
				// TODO: move with RRB
				int i = 0;
				while (i < count_lst(stack_b) - distance)
				{
					rev_rotate_stack(stack_b, "rrb");
					i++;
				}
			}

			// TODO: push it to A
			push_stack(stack_a, stack_b, "pa");
		}

		// print_lst(stack_a);
	}
}
