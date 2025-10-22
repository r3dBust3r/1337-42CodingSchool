/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcpy.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 18:35:27 by ottalhao          #+#    #+#             */
/*   Updated: 2025/10/21 18:38:59 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

static int	ft_strlen(char *str)
{
	int	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

int	ft_strlcpy(char *dst, const char *src, size_t size)
{
	int	dst_len;
	int	src_len;
	int	i;

	dst_len = ft_strlen(dst);
	src_len = ft_strlen(src);
	i = 0;
	while (i < (size - dst_len) - 1)
		dst[i] = src[i++];
	dst[i] = '\0';
	return (src_len);
}

/*
	strlcpy copies a string (src) into a destination buffer (dst), making sure:
	The destination does not overflow.
	The destination string is always null-terminated (if size > 0).
	It’s safer than strcpy because we specify the maximum size of dst.
	---
	Parameters:
		dst: Destination buffer where the string will be copied.
		src: Source string to copy from.
		size: The total size of the destination buffer, including space for the '\0'.
	Returns:
		The length of src, not the number of characters copied.
 */
