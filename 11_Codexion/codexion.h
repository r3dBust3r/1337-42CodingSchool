/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 18:00:40 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/30 20:13:45 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <pthread.h>
# include <sys/time.h>
# include <time.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <unistd.h>


typedef struct s_config t_config;
typedef struct s_dongle t_dongle;
typedef struct s_coder t_coder;
typedef struct s_request t_request;
typedef struct s_simulator t_simulator;


typedef struct s_config
{
	int				number_of_coders;
	int				time_to_burnout;
	int				time_to_compile;
	int				time_to_debug;
	int				time_to_refactor;
	int				required_compiles;
	int				dongle_cooldown;
	int				scheduler;
}	t_config;

typedef struct s_dongle
{
	int				id;
	int				is_available;
	long long		available_at;
    int				queue_size;
    t_request		**requests;
	pthread_mutex_t	mutex;
	pthread_cond_t	cond;
}	t_dongle;

typedef struct s_coder
{
	int				id;
	pthread_t		thread_id;
	t_dongle		*left_dongle;
	t_dongle		*right_dongle;
	t_simulator		*simulator;
	long long		last_compile;
	int				compiles_completed;
	pthread_mutex_t	mutex;
	pthread_mutex_t	print_mutex;
}	t_coder;

typedef struct s_request
{
    t_coder			*coder;
    long long		creation_time;
    long long		deadline;
}	t_request;

typedef struct s_simulator
{
	long long		start_time;
	int				is_running;
	t_coder			*coders;
	t_dongle		*dongles;
	t_config		*config;
	pthread_mutex_t	print_mutex;
	pthread_mutex_t	simulator_mutex;
}	t_simulator;

int		print_usage(void);
int		parser(int c, char **av, t_config *config);
long	ft_atol(char *s);

#endif
