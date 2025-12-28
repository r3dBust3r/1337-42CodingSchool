/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/18 21:43:44 by ottalhao          #+#    #+#             */
/*   Updated: 2025/11/21 17:40:50 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	handle_format(char c, va_list list, unsigned int *counter)
{
	if (c == 'c')
		ft_putchar(va_arg(list, int), counter);
	else if (c == 's')
		ft_putstr(va_arg(list, char *), counter);
	else if (c == 'd' || c == 'i')
		ft_putnbr(va_arg(list, int), counter);
	else if (c == 'u')
		ft_putnbr_uns(va_arg(list, unsigned int), counter);
	else if (c == 'x')
		ft_put_hex(va_arg(list, unsigned int), 1, counter);
	else if (c == 'X')
		ft_put_hex(va_arg(list, unsigned int), 0, counter);
	else if (c == 'p')
		ft_put_addr(va_arg(list, unsigned long), counter);
	else if (c == '%')
		ft_putchar('%', counter);
	else
		return (-1);
	return (0);
}

int	ft_printf(const char *s, ...)
{
	unsigned int	counter;
	va_list			list;
	int				i;

	if (!s)
		return (-1);
	counter = 0;
	va_start(list, s);
	i = 0;
	while (s[i])
	{
		if (s[i] == '%')
		{
			if (!s[i + 1] || handle_format(s[i + 1], list, &counter) == -1)
				return (-1);
			i++;
		}
		else
			ft_putchar(s[i], &counter);
		i++;
	}
	va_end(list);
	return (counter);
}
