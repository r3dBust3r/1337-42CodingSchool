/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putstr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/20 18:58:30 by ottalhao          #+#    #+#             */
/*   Updated: 2025/11/20 21:02:13 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libftprintf.h"

void	ft_putstr(char *s, unsigned int *counter)
{
	int i = 0;
	while (s[i])
	{
		ft_putchar(s[i], counter);
		i++;
	}
}
