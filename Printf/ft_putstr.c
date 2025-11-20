/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putstr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/20 18:58:30 by ottalhao          #+#    #+#             */
/*   Updated: 2025/11/21 00:14:48 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libftprintf.h"

void	ft_putstr(char *s, unsigned int *counter)
{
	int i = 0;
	if (!s)
	{
		ft_putstr("(null)", counter);
		return;
	}

	while (s[i])
	{
		ft_putchar(s[i], counter);
		i++;
	}
}
