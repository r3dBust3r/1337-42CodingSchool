/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_usage.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 21:28:50 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/26 22:11:24 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	print_usage(void)
{
	fprintf(stderr, "Usage: ./codexion <coders> <burnout> <compile> <debug> <refactor> <compiles_req> <cooldown> <scheduler>\n\n");
	fprintf(stderr, "Arguments:\n");
	fprintf(stderr, "  <coders>       : Positive integer (Number of coders)\n");
	fprintf(stderr, "  <burnout>      : Positive integer (Time to burnout in ms)\n");
	fprintf(stderr, "  <compile>      : Positive integer (Time to compile in ms)\n");
	fprintf(stderr, "  <debug>        : Positive integer (Time to debug in ms)\n");
	fprintf(stderr, "  <refactor>     : Positive integer (Time to refactor in ms)\n");
	fprintf(stderr, "  <compiles_req> : Positive integer (Number of compiles required)\n");
	fprintf(stderr, "  <cooldown>     : Positive integer (Dongle cooldown in ms)\n");
	fprintf(stderr, "  <scheduler>    : 'fifo' or 'edf'  (Scheduling algorithm)\n");
	return (1);
}
