/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   check_result_bonus.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 12:40:27 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/07 17:58:15 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker_bonus.h"

static int	lst_sorted(t_list *lst)
{
	while (lst->next)
	{
		if (lst->n > lst->next->n)
			return (0);
		lst = lst->next;
	}
	return (1);
}

void	check_result(t_list *stack_a, t_list *stack_b)
{
	if (lst_sorted(stack_a) && !stack_b)
		ft_putstr_fd("OK\n", 1);
	else
		ft_putstr_fd("KO\n", 1);
}
