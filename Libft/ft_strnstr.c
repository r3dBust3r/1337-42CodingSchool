/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/22 13:21:10 by ottalhao          #+#    #+#             */
/*   Updated: 2025/10/22 13:54:31 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

/*
	Loop through each position i in haystack up to len.
	For each position, check if needle matches character by character.
	Stop checking when you hit end of needle, end of haystack, or reach len.
	If full needle matched, return pointer to start of match.
	Otherwise, return NULL if no match found.
 */

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
