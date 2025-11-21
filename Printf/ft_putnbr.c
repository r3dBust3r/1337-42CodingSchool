/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/20 20:58:47 by ottalhao          #+#    #+#             */
/*   Updated: 2025/11/21 15:29:35 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

void	ft_putnbr(int n, unsigned int *counter)
{
	if (n == -2147483648)
	{
		ft_putstr("-2147483648", counter);
		return ;
	}
	if (n < 0)
	{
		ft_putchar('-', counter);
		n = -n;
	}
	if (n < 10)
	{
		ft_putchar(n + '0', counter);
		return ;
	}
	ft_putnbr(n / 10, counter);
	ft_putnbr(n % 10, counter);
}
