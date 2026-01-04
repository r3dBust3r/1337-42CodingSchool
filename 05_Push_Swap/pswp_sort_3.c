/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pswp_sort_3.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:13:51 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 11:55:38 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	pswp_sort_3(t_list **stack_a)
{
	t_list	*nd_1 = *stack_a;
	t_list	*nd_2 = (*stack_a)->next;
	t_list	*nd_3 = (*stack_a)->next->next;

	if (nd_1->n < nd_2->n && nd_2->n < nd_3->n) 
		return;
	if (nd_1->n < nd_2->n && nd_1->n < nd_3->n && nd_2->n > nd_3->n) 
	{
		swap_stack(stack_a, "sa");
		rotate_stack(stack_a, "ra");
	}
	if (nd_1->n > nd_2->n && nd_2->n < nd_3->n && nd_1->n < nd_3->n) 
		swap_stack(stack_a, "sa");
	if (nd_1->n > nd_2->n && nd_1->n > nd_3->n && nd_2->n < nd_3->n) 
		rotate_stack(stack_a, "ra");
	if (nd_1->n < nd_2->n && nd_1->n > nd_3->n && nd_2->n > nd_3->n) 
		rev_rotate_stack(stack_a, "rra");
	if (nd_1->n > nd_2->n && nd_1->n > nd_3->n && nd_2->n > nd_3->n) 
	{
		swap_stack(stack_a, "sa");
		rev_rotate_stack(stack_a, "rra");
	}
}
