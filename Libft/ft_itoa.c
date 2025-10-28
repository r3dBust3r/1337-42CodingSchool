/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/27 17:44:10 by ottalhao          #+#    #+#             */
/*   Updated: 2025/10/28 10:52:04 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	get_len(char *s)
{
	int	i;

	i = 0;
	while (s[i])
		i++;
	return (i);
}

static void	my_strrev(char *s)
{
	int		i;
	char	temp;

	i = 0;
	while (i < get_len(s) / 2)
	{
		temp = s[i];
		s[i] = s[get_len(s) - i - 1];
		s[get_len(s) - i - 1] = temp;
		i++;
	}
}

char	*ft_itoa(int n)
{
	char	*asc_n;
	int		negative;
	int		i;

	asc_n = (char *)malloc(sizeof(char) * 26);
	if (!asc_n)
		return (NULL);
	negative = 0;
	if (n < 0)
	{
		n = -n;
		negative = 1;
	}
	i = 0;
	while (n > 9)
	{
		asc_n[i++] = (n % 10) + '0';
		n /= 10;
	}
	asc_n[i] = n + '0';
	if (negative)
		asc_n[++i] = '-';
	my_strrev(asc_n);
	asc_n[++i] = 0x0;
	return (asc_n);
}
