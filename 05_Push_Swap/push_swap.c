/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/28 16:25:30 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 12:04:12 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/**************** Testing functions **************/
#include <stdio.h> // REMOVE ME
void print_lst(t_list **lst)
{
	t_list *current = *lst;
	printf("\n---------------------\n");
	while (current)
	{
		printf("  idx: %d\t|\tval: %d", current->index, current->n);
		current = current->next;
		if (current) printf("\n");
	}
	printf("\n---------------------\n");
}
/**************** Testing functions **************/

int	main(int ac, char **av)
{
	if (ac == 1)
		return (1);

	t_list	*stack_a = NULL;
	t_list	*node;
	t_list	*current;

	char	**tab;
	
	int		i = 1;
	int		j = 0;
	int		k = 0;
	long	n = 0;

	while (i < ac)
	{
		tab = ft_split(av[i], ' ');
		if (!tab || is_empty(tab))
			return error_exit(&stack_a, NULL, tab);
		j = 0;
		while (tab[j])
		{
			k = 0;
			while (tab[j][k])
			{
				if (k == 0 && (tab[j][k] == '+' || tab[j][k] == '-'))
					k++;
				if (tab[j][k] < '0' || tab[j][k] > '9')
					return error_exit(&stack_a, NULL, tab);
				k++;
			}
			n = ft_atol(tab[j]);
			if (n < -2147483648 || n > 2147483647)
				return error_exit(&stack_a, NULL, tab);
			current = stack_a;
			while (current)
			{
				if (n == current->n)
					return error_exit(&stack_a, NULL, tab);
				current = current->next;
			}
			node = ft_lstnew(n);
			if (!node)
				return error_exit(&stack_a, NULL, tab);
			ft_lstadd_back(&stack_a, node);
			j++;
		}
		free_tab(tab);
		tab = NULL;
		i++;
	}
	
	t_list *stack_b = NULL;
	assign_indexes(&stack_a);
	pswp_sort(&stack_a, &stack_b, count_lst(&stack_a));

	print_lst(&stack_a); // REMOVE ME LATER
	
	free_stack(&stack_a);
	free_stack(&stack_b);

	return 0;
}

/**
 * 
 * TODO: [+] Check malloc
 * TODO: [+] push_swap to s_list
 * TODO: [+] ps_list to t_list
 * TODO: [+] Putfd -> 2
 * TODO: [+] Doesn't Handle to 24, Fix it
 * TODO: [+] Create Makefile
 * TODO: [+] Activate CFLAGS in Makefile
 * TODO: [+] Check leaks
 * TODO: [+] Remove all comments
 * TODO: [+] Remove forbidden headers
 * TODO: [ ] Norminette
 * TODO: [ ] Remove forbidden functions [printf, etc...]
 * TODO: [ ] Remove testing functions
 * TODO: [ ] Create Markdown
 * TODO: [ ] Push
 * 
 */
 