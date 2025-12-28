/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/27 17:44:10 by ottalhao          #+#    #+#             */
/*   Updated: 2025/11/10 10:35:51 by ottalhao         ###   ########.fr       */
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

static void	fill_digits(char *s, long num, int len)
{
	s[len] = '\0';
	if (num == 0)
	{
		s[0] = '0';
		return ;
	}
	while (num > 0)
	{
		s[--len] = (num % 10) + '0';
		num /= 10;
	}
}

char	*ft_itoa(int n)
{
	char	*s;
	long	num;
	int		len;

	len = calc_len(n);
	s = (char *)malloc(sizeof(char) * (len + 1));
	if (!s)
		return (NULL);
	num = n;
	if (num < 0)
	{
		s[0] = '-';
		num = -num;
	}
	fill_digits(s, num, len);
	return (s);
}
