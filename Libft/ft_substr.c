/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 18:44:55 by ottalhao          #+#    #+#             */
/*   Updated: 2025/10/24 20:11:11 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	my_strlen(char *str)
{
	int	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	size_t	s_len;
	size_t	alloc_size;
	size_t	i;
	char	*p;

	s_len = my_strlen((char *)s);
	if (s_len - start < len)
		alloc_size = s_len - start;
	else
		alloc_size = len;
	p = (char *)malloc(sizeof(char) * alloc_size);
	if (!p)
		return (NULL);
	i = 0;
	while (i < alloc_size)
		p[i] = s[start + i++];
	return (p);
}
