/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker_helpers_bonus.c                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 10:36:42 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/07 17:58:37 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker_bonus.h"

int	exec_swap(char *line, t_list **a, t_list **b)
{
	if (!ft_strcmp(line, "sa\n"))
		swap_stack(a);
	else if (!ft_strcmp(line, "sb\n"))
		swap_stack(b);
	else if (!ft_strcmp(line, "ss\n"))
		swap_stack_both(a, b);
	else
		return (0);
	return (1);
}

int	exec_push(char *line, t_list **a, t_list **b)
{
	if (!ft_strcmp(line, "pa\n"))
		push_stack(a, b, "pa");
	else if (!ft_strcmp(line, "pb\n"))
		push_stack(a, b, "pb");
	else
		return (0);
	return (1);
}

int	exec_rotate(char *line, t_list **a, t_list **b)
{
	if (!ft_strcmp(line, "ra\n"))
		rotate_stack(a);
	else if (!ft_strcmp(line, "rb\n"))
		rotate_stack(b);
	else if (!ft_strcmp(line, "rr\n"))
		rotate_stack_both(a, b);
	else if (!ft_strcmp(line, "rra\n"))
		rev_rotate_stack(a);
	else if (!ft_strcmp(line, "rrb\n"))
		rev_rotate_stack(b);
	else if (!ft_strcmp(line, "rrr\n"))
		rrr(a, b);
	else
		return (0);
	return (1);
}

int	exec_instruction(char *line, t_list **a, t_list **b)
{
	if (exec_swap(line, a, b))
		return (1);
	if (exec_push(line, a, b))
		return (1);
	if (exec_rotate(line, a, b))
		return (1);
	return (0);
}

int	checker_error_exit(t_list **a, t_list **b, char *line)
{
	if (line)
		free(line);
	ft_putstr_fd("Error\n", 2);
	free_stack(a);
	free_stack(b);
	return (1);
}
