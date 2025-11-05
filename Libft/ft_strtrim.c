/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 20:52:15 by ottalhao          #+#    #+#             */
/*   Updated: 2025/11/04 15:54:36 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	calc_allocsize(char *start, char *end)
{
	int	i;

	i = 0;
	while (start[i])
	{
		if (start + i == end)
			break ;
		i++;
	}
	return (i + 1);
}

static char	*define_start_p(char *s1, char *set, char *start_p)
{
	int	j;
	int	i;

	i = 0;
	while (s1[i])
	{
		j = 0;
		while (set[j])
		{
			if (s1[i] == set[j])
			{
				start_p++;
				break ;
			}
			j++;
		}
		if (set[j] == 0x0)
			break ;
		i++;
	}
	return (start_p);
}

static char	*define_end_p(char *s1, char *set, char *end_p)
{
	int	len;
	int	j;

	len = ft_strlen((char *)s1) - 1;
	while (len)
	{
		j = 0;
		while (set[j])
		{
			if (s1[len] == set[j])
			{
				end_p--;
				break ;
			}
			j++;
		}
		if (set[j] == 0x0)
			break ;
		len--;
	}
	return (end_p);
}

char	*ft_strtrim(char const *s1, char const *set)
{
	char	*start_p;
	char	*end_p;
	char	*p;
	int		i;
	int		alloc_size;

	i = 0;
	start_p = (char *)s1;
	end_p = (char *)s1 + ft_strlen((char *)s1) - 1;
	start_p = define_start_p((char *)s1, (char *)set, start_p);
	end_p = define_end_p((char *)s1, (char *)set, end_p);
	alloc_size = calc_allocsize(start_p, end_p) + 1;
	p = (char *)malloc(sizeof(char) * alloc_size);
	if (!p)
		return (NULL);
	i = 0;
	while (i < alloc_size - 1)
	{
		*(p + i) = *(start_p + i);
		i++;
	}
	p[i] = 0x0;
	return (p);
}
