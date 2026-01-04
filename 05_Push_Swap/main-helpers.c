/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main-helpers.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/04 16:07:38 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 16:07:45 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	non_digits(t_list **stack_a, char **tab, int j)
{
	int	k;

	k = 0;
	while (tab[j][k])
	{
		if (k == 0 && (tab[j][k] == '+' || tab[j][k] == '-'))
			k++;
		if (tab[j][k] < '0' || tab[j][k] > '9')
			return (error_exit(stack_a, NULL, tab));
		k++;
	}
	return (0);
}

int	out_of_range(t_list **stack_a, long long *n, char **tab, int *j)
{
	(*n) = ft_atol(tab[*j]);
	if (*n < -2147483648 || *n > 2147483647)
		return (error_exit(stack_a, NULL, tab));
	return (0);
}

int	node_exists(t_list **stack_a, char **tab, long long n)
{
	t_list	*current;

	current = *stack_a;
	while (current)
	{
		if (n == current->n)
			return (error_exit(stack_a, NULL, tab));
		current = current->next;
	}
	return (0);
}

int	create_and_store(t_list **stack_a, char **tab, long long n)
{
	t_list	*node;

	node = ft_lstnew(n);
	if (!node)
		return (error_exit(stack_a, NULL, tab));
	ft_lstadd_back(stack_a, node);
	return (0);
}
