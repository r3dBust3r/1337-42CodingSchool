/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putstr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/20 18:58:30 by ottalhao          #+#    #+#             */
/*   Updated: 2025/11/21 17:10:51 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

void	ft_putstr(char *s, unsigned int *counter)
{
	int	i;

	i = 0;
	if (!s)
	{
		ft_putstr("(null)", counter);
		return ;
	}
	while (s[i])
	{
		ft_putchar(s[i], counter);
		i++;
	}
}
