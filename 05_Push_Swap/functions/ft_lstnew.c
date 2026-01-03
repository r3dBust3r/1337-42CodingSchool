/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstnew.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:02:54 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/03 14:03:08 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

ps_list	*ft_lstnew(int n)
{
	ps_list	*new_node;

	new_node = malloc(sizeof(ps_list));
	if (!new_node)
		return (NULL);
	new_node->n = n;
	new_node->index = -1;
	new_node->next = NULL;
	return (new_node);
}
