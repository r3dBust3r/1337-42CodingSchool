/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   help.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 21:28:50 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/31 18:57:28 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	p_err(char *s)
{
	fprintf(stderr, s);
}

int	print_usage(void)
{
	p_err("Error: something is wrong with your input\n\n");
	p_err("Usage: ./codexion <coders> <burnout> <compile> ");
	p_err("<debug> <refactor> <compiles_req> <cooldown> <scheduler>\n\n");
	p_err("Arguments:\n");
	p_err(" <coders>       : Strictly positive integer (Number of coders)\n");
	p_err(" <burnout>      : Positive integer (Time to burnout in ms)\n");
	p_err(" <compile>      : Positive integer (Time to compile in ms)\n");
	p_err(" <debug>        : Positive integer (Time to debug in ms)\n");
	p_err(" <refactor>     : Positive integer (Time to refactor in ms)\n");
	p_err(" <compiles_req> : Positive integer (Number of compiles required)\n");
	p_err(" <cooldown>     : Positive integer (Dongle cooldown in ms)\n");
	p_err(" <scheduler>    : 'fifo' or 'edf'  (Scheduling algorithm)\n");
	return (1);
}
