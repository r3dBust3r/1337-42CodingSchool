/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 09:04:57 by ottalhao          #+#    #+#             */
/*   Updated: 2025/10/24 14:11:03 by ottalhao         ###   ########.fr       */
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

size_t	ft_strlcat(char *dst, const char *src, size_t size)
{
	size_t	dst_len;
	size_t	src_len;
	size_t	i;

	src_len = my_strlen(src);
	dst_len = my_strlen(dst);
	if (dst_len >= size)
		return (size + src_len);
	i = 0;
	while (src[i] && (dst_len + i + 1) < size)
		dst[dst_len + i] = src[i++];
	dst[dst_len + i] = '\0';
	return (dst_len + src_len);
}
