/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/18 21:43:44 by ottalhao          #+#    #+#             */
/*   Updated: 2025/11/21 17:09:46 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H
# include <stdarg.h>
# include <unistd.h>

void	ft_putchar(char c, unsigned int *counter);
void	ft_putstr(char *s, unsigned int *counter);
void	ft_putnbr(int n, unsigned int *counter);
void	ft_putnbr_uns(unsigned int n, unsigned int *counter);
void	ft_put_hex(unsigned long n, int is_lower, unsigned int *counter);
void	ft_put_addr(unsigned long ptr, unsigned int *counter);
int		ft_printf(const char *s, ...);

#endif