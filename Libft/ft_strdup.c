/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/22 21:26:50 by ottalhao          #+#    #+#             */
/*   Updated: 2025/10/22 21:44:36 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

static int	ft_strlen(const char *s)
{
	int	i;

	i = 0;
	while (s[i])
		i++;
	return (i);
}

char	*ft_strdup(const char *s)
{
	int		i;
	int		s_len;
	char	*new_s;

	s_len = ft_strlen(s);
	new_s = (char *)malloc(sizeof(char) * (s_len + 1));
	if (!new_s)
		return (NULL);
	i = 0;
	while (i < s_len)
		new_s[i] = s[i++];
	new_s[i] = '\0';
	return (new_s);
}
