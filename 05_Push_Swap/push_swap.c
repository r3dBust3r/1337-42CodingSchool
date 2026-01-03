/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/28 16:25:30 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/03 15:08:47 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	main(int ac, char **av)
{
	if (ac == 1)
		return (ft_putstr_fd("Error\n", 2), 1);

	ps_list	*stack_a = NULL;
	ps_list	*node;
	ps_list	*current;

	int		i = 1;
	int		j = 0;
	int		k = 0;
	long	n = 0;
	char	**asc_n;
	
	while (i < ac)
	{
		asc_n = ft_split(av[i], ' ');
		if (is_empty(asc_n))
			return (ft_putstr_fd("Error\n", 2), 1);
		j = 0;
		while (asc_n[j])
		{
			k = 0;
			while (asc_n[j][k])
			{
				if (k == 0 && (asc_n[j][k] == '+' || asc_n[j][k] == '-'))
					k++;
				if (asc_n[j][k] < '0' || asc_n[j][k] > '9')
					return (ft_putstr_fd("Error\n", 2), 1);
				k++;
			}
			n = ft_atol(asc_n[j]);
			if (n < -2147483648 || n > 2147483647)
				return (ft_putstr_fd("Error\n", 2), 1);

			current = stack_a;
			while (current)
			{
				if (n == current->n)
					return (ft_putstr_fd("Error\n", 2), 1);
				current = current->next;
			}
			node = ft_lstnew(n);
			ft_lstadd_back(&stack_a, node);
			j++;
		}
		i++;
	}
	ps_list *stack_b = NULL;
	assign_indexes(&stack_a);
	pswp_sort(&stack_a, &stack_b, count_lst(&stack_a));
	return 0;
}

/**
 * 
 * TODO: Check malloc
 * TODO: Check leaks
 * TODO: Remove forbidden functions [printf, etc...]
 * TODO: Remove forbidden headers
 * TODO: Remove testing functions
 * TODO: Create Makefile
 * TODO: Create Markdown
 * TODO: Replace ps_list with t_list
 * TODO: Replace ps_spaw with s_list
 * TODO: Push
 *
 */
