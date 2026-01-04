/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pswp_sort.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:18:41 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 14:40:43 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	sort_small_stack(t_list **stack_a, t_list **stack_b, int count)
{
	if (count == 2 && (*stack_a)->index > (*stack_a)->next->index)
		swap_stack_both(stack_a, stack_b);
	else if (count == 3)
		pswp_sort_3(stack_a);
	else if (count == 4)
		pswp_sort_4(stack_a, stack_b);
	else if (count == 5)
		pswp_sort_5(stack_a, stack_b);
}

static void	sort_by_chunks(
	t_list **stack_a,
	t_list **stack_b,
	int count,
	int *pushed)
{
	int	chunk_size;

	if (count < 100)
		chunk_size = count;
	else if (count < 300)
		chunk_size = count / 7;
	else
		chunk_size = count / 15;
	while (*stack_a)
	{
		if ((*stack_a)->index <= (*pushed))
		{
			push_stack(stack_a, stack_b, "pb");
			rotate_stack(stack_b, "rb");
			(*pushed)++;
		}
		else if ((*stack_a)->index < (*pushed) + chunk_size)
		{
			push_stack(stack_a, stack_b, "pb");
			(*pushed)++;
		}
		else
			rotate_stack(stack_a, "ra");
	}
}

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

static void	push_biggest_to_a(t_list **stack_a, t_list **stack_b)
{
	t_list	*biggest;
	t_list	*current;

	biggest = *stack_b;
	current = *stack_b;
	while (current)
	{
		if (current->index > biggest->index)
			biggest = current;
		current = current->next;
	}
	rotate_to_top(stack_b, biggest);
	push_stack(stack_a, stack_b, "pa");
}

void	pswp_sort(t_list **stack_a, t_list **stack_b, unsigned int count)
{
	int	pushed;

	pushed = 0;
	if (count <= 5)
		sort_small_stack(stack_a, stack_b, count);
	else
	{
		sort_by_chunks(stack_a, stack_b, count, &pushed);
		while (*stack_b)
			push_biggest_to_a(stack_a, stack_b);
	}
}
