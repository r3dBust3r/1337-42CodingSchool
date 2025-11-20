/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_uns.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/20 20:59:24 by ottalhao          #+#    #+#             */
/*   Updated: 2025/11/20 21:03:03 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libftprintf.h"

void	ft_putnbr_uns(unsigned int n, unsigned int *counter)
{
	if (n < 10)
	{
		ft_putchar(n + '0', counter);
		return ;
	}
	ft_putnbr_uns(n / 10, counter);
	ft_putnbr_uns(n % 10, counter);
}
