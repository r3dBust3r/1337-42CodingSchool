/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/18 21:43:44 by ottalhao          #+#    #+#             */
/*   Updated: 2025/11/20 21:36:12 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libftprintf.h"

int ft_printf(const char *s, ...)
{
	unsigned int counter = 0;
	char next;

	va_list list;
	va_start(list, s);

	if (!s)
		return (-1);

	int i = 0;
	while (s[i])
	{
		next = s[i + 1];
		if (s[i] == '%')
		{
			if (next == 'c') { ft_putchar(va_arg(list, int), &counter); i++; }
			else if (next == 's') { ft_putstr(va_arg(list, char *), &counter); i++; }
			else if (next == 'd' || next == 'i') { ft_putnbr(va_arg(list, int), &counter); i++; }
			else if (next == 'u') { ft_putnbr_uns(va_arg(list, int), &counter); i++; }
			else if (next == 'x') { ft_put_hex(va_arg(list, unsigned int), 1, &counter); i++; }
			else if (next == 'X') { ft_put_hex(va_arg(list, unsigned int), 0, &counter); i++; }
			else if (next == 'p') { ft_put_addr(va_arg(list, long long), &counter); i++; }
			else if (next == '%') { ft_putchar('%', &counter); i++; }
		}
		else
		{
			ft_putchar(s[i], &counter);
		}
		i++;
	}

	va_end(list);

	return counter;
}
