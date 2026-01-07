/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split_bonus.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 14:00:09 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/07 17:58:59 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker_bonus.h"

static int	count_elms(const char *s, char c)
{
	int	i;
	int	elms;

	elms = 0;
	i = 0;
	if (!s)
		return (0);
	while (s[i])
	{
		while (s[i] == c)
			i++;
		if (s[i])
			elms++;
		while (s[i] && s[i] != c)
			i++;
	}
	return (elms);
}

static void	free_all(char **arr, int filled)
{
	int	i;

	i = 0;
	while (i < filled)
	{
		free(arr[i]);
		i++;
	}
	free(arr);
}

static char	*alloc_word(const char *s, int start, int end)
{
	int		len;
	int		j;
	char	*word;

	len = end - start;
	word = malloc(sizeof(char) * (len + 1));
	if (!word)
		return (NULL);
	j = 0;
	while (j < len)
	{
		word[j] = s[start + j];
		j++;
	}
	word[len] = '\0';
	return (word);
}

static int	fill_parent_array(const char *s, char c, char **arr, int i)
{
	int		start;
	int		index;
	char	*word;

	index = 0;
	while (s[i])
	{
		while (s[i] == c)
			i++;
		if (!s[i])
			break ;
		start = i;
		while (s[i] && s[i] != c)
			i++;
		word = alloc_word(s, start, i);
		if (!word)
		{
			free_all(arr, index);
			return (-1);
		}
		arr[index++] = word;
	}
	arr[index] = NULL;
	return (0);
}

char	**ft_split(const char *s, char c)
{
	char	**arr;
	int		count;
	int		i;

	i = 0;
	if (!s)
		return (NULL);
	count = count_elms(s, c);
	arr = malloc(sizeof(char *) * (count + 1));
	if (!arr)
		return (NULL);
	if (fill_parent_array(s, c, arr, i) == -1)
		return (NULL);
	return (arr);
}
