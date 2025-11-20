/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_put_hex.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/20 20:59:44 by ottalhao          #+#    #+#             */
/*   Updated: 2025/11/20 21:01:07 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libftprintf.h"

void	ft_put_hex(unsigned long n, int is_lower, unsigned int *counter)
{
	char *lower_hex = "0123456789abcdef";
	char *upper_hex = "0123456789ABCDEF";

	if (n < 16)
	{
		if (is_lower)
			ft_putchar(lower_hex[n], counter);
		else
			ft_putchar(upper_hex[n], counter);
		return;
	}

	ft_put_hex(n / 16, is_lower, counter);
	ft_put_hex(n % 16, is_lower, counter);
}
