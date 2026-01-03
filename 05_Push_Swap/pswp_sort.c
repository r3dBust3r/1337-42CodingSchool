/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pswp_sort.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:18:41 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/03 14:19:17 by ottalhao         ###   ########.fr       */
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
			rotate_stack(stack_a, "ra"); // ra()
			distance--;
		}
		push_stack(stack_a, stack_b, "pb"); // pb()
		pswp_sort_3(stack_a, stack_b);
		push_stack(stack_a, stack_b, "pa"); // pa()
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
					rotate_stack(stack_a, "ra"); // ra()
				else
					rev_rotate_stack(stack_a, "rra");
				distance--;
			}
			push_stack(stack_a, stack_b, "pb"); // pb()
			i--;
		}
		pswp_sort_3(stack_a, stack_b);
		push_stack(stack_a, stack_b, "pa"); // pa()
		push_stack(stack_a, stack_b, "pa"); // pa()
	}
	else
	{
		int chunk_size = (count <= 100) ? (count / 7) : (count / 15);
		int pushed = 0;
		while (*stack_a)
		{
			if ((*stack_a)->index <= pushed)
			{
				push_stack(stack_a, stack_b, "pb"); // pb()
				rotate_stack(stack_b, "rb"); // rb()
				pushed++;
			}
			else if ((*stack_a)->index < pushed + chunk_size)
			{
				push_stack(stack_a, stack_b, "pb"); // pb()
				pushed++;
			}
			else
			{
				rotate_stack(stack_a, "ra"); // ra()
			}
		}
		
		// int chunk_size = (count <= 100) ? (count / 3) : (count / 9);
		// int limit = chunk_size;
		// //pushed = 0
		// while (*stack_a)
		// {
		// 	// 1. Find the cheapest node with index < limit
		// 	int hold_first_distance = find_hold_first(*stack_a, limit);
		// 	int hold_last_distance = count_lst(stack_a) - find_hold_last(*stack_a, limit);

		// 	if (hold_first_distance == -1)
		// 	{
		// 		limit += chunk_size;
		// 		continue;
		// 	}

		// 	// 2. Move it to top of A and pb [cite: 245, 278, 279]
		// 	int i = 0;
		// 	if (hold_first_distance <= hold_last_distance)
		// 	{
		// 		while (i < hold_first_distance)
		// 		{
		// 			rotate_stack(stack_a, "ra"); // ra()
		// 			i++;
		// 		}
		// 	}
		// 	else
		// 	{
		// 		while (i < hold_last_distance)
		// 		{
		// 			rev_rotate_stack(stack_a, "rra"); // rra()
		// 			i++;
		// 		}
		// 	}

		// 	// printf("Hold first: %d\nHold last: %d\nChoosing: %d\n\n", hold_first_distance, hold_last_distance, (hold_first_distance <= hold_last_distance) ? hold_first_distance : hold_last_distance);

		// 	push_stack(stack_a, stack_b, "pb"); // pb()

		// 	if ((*stack_b)->index < (limit - (chunk_size / 2)))
		// 	{
		// 		rotate_stack(stack_b, "rb");
		// 	}
		// }

		// print_lst(stack_b);
		// exit(0);
		
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
					rotate_stack(stack_b, "rb"); // rb()
					i++;
				}
			} else {
				// TODO: move with RRB
				int i = 0;
				while (i < count_lst(stack_b) - distance)
				{
					rev_rotate_stack(stack_b, "rrb"); // rrb()
					i++;
				}
			}

			// TODO: push it to A
			push_stack(stack_a, stack_b, "pa"); // pa()
		}

		// print_lst(stack_a);
	}
}
