/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 18:44:55 by ottalhao          #+#    #+#             */
/*   Updated: 2025/11/04 15:57:14 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	size_t	s_len;
	size_t	alloc_size;
	size_t	i;
	char	*p;

	s_len = ft_strlen((char *)s);
	if (s_len - start < len)
		alloc_size = s_len - start;
	else
		alloc_size = len;
	p = (char *)malloc(sizeof(char) * (alloc_size + 1));
	if (!p)
		return (NULL);
	i = 0;
	while (i < alloc_size)
	{
		p[i] = s[start + i];
		i++;
	}
	p[i] = '\0';
	return (p);
}
