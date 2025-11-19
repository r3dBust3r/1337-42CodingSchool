/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/18 21:43:44 by ottalhao          #+#    #+#             */
/*   Updated: 2025/11/18 22:26:41 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdarg.h>
#include "libft.h"

int ft_printf(const char *s, ...)
{
	va_list list;
	va_start(list, s);

	int i = 0;
	while (s[i])
	{
		if (s[i] == '%')
		{
			if (s[i + 1] == '%')
			{
				ft_putchar_fd('%', 1);
				i++;
			}
			if (s[i + 1] == 'c')
			{
				ft_putchar_fd(va_arg(list, int), 1);
				i++;
			}
			if (s[i + 1] == 's')
			{
				ft_putstr_fd(va_arg(list, char *), 1);
				i++;
			}
			if (s[i + 1] == 'p')
			{
				/** print mem address */
			}
			if (s[i + 1] == 'd' || s[i + 1] == 'i')
			{
				ft_putnbr_fd(va_arg(list, int), 1);
				i++;
			}
			if (s[i + 1] == 'u')
			{
				/** print digit */
			}
			if (s[i + 1] == 'x')
			{
				/** print hex lower */
			}
			if (s[i + 1] == 'X')
			{
				/** print hex upper */
			}
		}
		else
		{
			write(1, &s[i], 1);
		}
		i++;
	}

	va_end(list);
}
