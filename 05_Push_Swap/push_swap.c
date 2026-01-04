/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/28 16:25:30 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 16:11:59 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	handle_params(t_list **stack_a, char **tab, int *j, long long *n)
{
	if (non_digits(stack_a, tab, *j))
		return (1);
	if (out_of_range(stack_a, n, tab, j))
		return (1);
	if (node_exists(stack_a, tab, *n))
		return (1);
	if (create_and_store(stack_a, tab, *n))
		return (1);
	return (0);
}

static int	parse_and_feed(t_list **stack_a, int ac, char **av, char **tab)
{
	int			i;
	int			j;
	long long	n;

	i = 1;
	while (i < ac)
	{
		tab = ft_split(av[i], ' ');
		if (!tab || is_empty(tab))
			return (error_exit(stack_a, NULL, tab));
		j = 0;
		while (tab[j])
		{
			if (handle_params(stack_a, tab, &j, &n))
				return (1);
			j++;
		}
		free_tab(tab);
		tab = NULL;
		i++;
	}
	return (0);
}

int	main(int ac, char **av)
{
	t_list	*stack_a;
	t_list	*stack_b;
	char	**tab;

	if (ac == 1)
		return (1);
	stack_a = NULL;
	stack_b = NULL;
	tab = NULL;
	if (parse_and_feed(&stack_a, ac, av, tab))
		return (1);
	assign_indexes(&stack_a);
	pswp_sort(&stack_a, &stack_b, count_lst(&stack_a));
	free_stack(&stack_a);
	free_stack(&stack_b);
	return (0);
}
