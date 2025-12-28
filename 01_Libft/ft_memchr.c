/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/22 10:15:30 by ottalhao          #+#    #+#             */
/*   Updated: 2025/10/24 14:11:03 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memchr(const void *s, int c, size_t n)
{
	size_t	i;
	char	*temp_s;

	i = 0;
	temp_s = (char *)s;
	while (i < n)
	{
		if (temp_s[i] == (char)c)
			return ((void *)&temp_s[i]);
		i++;
	}
	return (NULL);
}
