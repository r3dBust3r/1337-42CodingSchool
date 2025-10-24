/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/22 13:21:10 by ottalhao          #+#    #+#             */
/*   Updated: 2025/10/24 14:11:03 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	check_current(const char *big,
							const char *little,
							size_t len,
							int curr_index)
{
	size_t	i;

	i = 0;
	while ((curr_index + i < len) && little[i])
	{
		if (little[i] != big[i + curr_index])
			return (0);
		i++;
	}
	if (little[i] == '\0')
		return (1);
	return (0);
}

char	*ft_strnstr(const char *big, const char *little, size_t len)
{
	size_t	i;

	if (little[0] == '\0')
		return ((char *)big);
	i = 0;
	while (i < len && big[i])
	{
		if (big[i] == little[0])
		{
			if (check_current(big, little, len, i))
				return ((char *)&big[i]);
		}
		i++;
	}
	return (0);
}
