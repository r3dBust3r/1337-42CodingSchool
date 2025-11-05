/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 20:52:15 by ottalhao          #+#    #+#             */
/*   Updated: 2025/11/05 18:05:19 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strtrim(char const *s1, char const *set)
{
	char	*start_p;
	char	*end_p;
	char	*p;
	size_t	alloc_size;

	if (!s1 || !set)
		return (NULL);
	start_p = (char *)s1;
	while (*start_p && ft_strchr(set, *start_p))
		start_p++;
	end_p = (char *)s1 + ft_strlen(s1);
	while (end_p > start_p && ft_strchr(set, *(end_p - 1)))
		end_p--;
	alloc_size = end_p - start_p;
	p = malloc(alloc_size + 1);
	if (!p)
		return (NULL);
	ft_strlcpy(p, start_p, alloc_size + 1);
	return (p);
}
