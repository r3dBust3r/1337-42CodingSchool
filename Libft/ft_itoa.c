/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/27 17:44:10 by ottalhao          #+#    #+#             */
/*   Updated: 2025/11/05 18:59:36 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	calc_len(int n)
{
	int	len;

	len = 0;
	if (n <= 0)
		len++;
	while (n != 0)
	{
		len++;
		n /= 10;
	}
	return (len);
}

char	*ft_itoa(int n)
{
	int		len;
	char	*asc_n;
	long	num;

	len = calc_len(n);
	asc_n = (char *)malloc(sizeof(char) * (len + 1));
	num = n;
	asc_n[len] = '\0';
	if (num < 0)
	{
		asc_n[0] = '-';
		num = -num;
	}
	if (num == 0)
	{
		asc_n[0] = '0';
		return (asc_n);
	}
	while (num > 0)
	{
		asc_n[--len] = (num % 10) + '0';
		num /= 10;
	}
	return (asc_n);
}
