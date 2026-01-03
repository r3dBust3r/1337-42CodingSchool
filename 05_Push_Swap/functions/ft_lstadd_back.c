/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstadd_back.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:02:14 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/03 19:26:50 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	ft_lstadd_back(ps_list **lst, ps_list *node)
{
	ps_list	*temp;

	if (!lst || !node)
		return ;
	if (!*lst)
	{
		*lst = node;
		return ;
	}
	temp = *lst;
	while (temp->next)
		temp = temp->next;
	temp->next = node;
}
