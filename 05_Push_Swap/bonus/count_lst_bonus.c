/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   count_lst_bonus.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:01:19 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/07 17:58:44 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker_bonus.h"

int	count_lst(t_list **lst)
{
	t_list	*current;
	int		i;

	i = 0;
	current = *lst;
	while (current)
	{
		current = current->next;
		i++;
	}
	return (i);
}
