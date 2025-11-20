/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_put_addr.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/20 20:59:57 by ottalhao          #+#    #+#             */
/*   Updated: 2025/11/20 21:01:10 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libftprintf.h"

void	ft_put_addr(unsigned long ptr, unsigned int *counter)
{
	if (!ptr)
	{
		ft_putstr("(nil)", counter);
		return;
	}

	ft_putstr("0x", counter);
	ft_put_hex(ptr, 1, counter);
}
