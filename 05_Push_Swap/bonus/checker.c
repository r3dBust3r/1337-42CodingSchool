/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/06 23:18:27 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/07 13:30:04 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker.h"

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

int	ft_strcmp(const char *s1, const char *s2)
{
	size_t	i;

	i = 0;
	while (s1[i] && s2[i])
	{
		if (s1[i] != s2[i])
			break ;
		i++;
	}
	return ((unsigned char)s1[i] - (unsigned char)s2[i]);
}

int	main(int ac, char **av)
{
	t_list	*stack_a;
	t_list	*stack_b;
	char	*line;

	if (ac == 1)
		return (1);
	stack_a = NULL;
	stack_b = NULL;
	if (parse_and_feed(&stack_a, ac, av, NULL))
		return (1);
	line = get_next_line(0);
	while (line)
	{
		if (!exec_instruction(line, &stack_a, &stack_b))
			return (checker_error_exit(&stack_a, &stack_b, line));
		free(line);
		line = get_next_line(0);
	}
	if (line)
		free(line);
	check_result(stack_a, stack_b);
	free_stack(&stack_a);
	free_stack(&stack_b);
	return (0);
}
