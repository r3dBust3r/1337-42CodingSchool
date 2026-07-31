/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 18:00:40 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/31 18:19:52 by ottalhao         ###   ########.fr       */
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

typedef struct s_config		t_config;
typedef struct s_dongle		t_dongle;
typedef struct s_coder		t_coder;
typedef struct s_request	t_request;
typedef struct s_simulator	t_simulator;

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

long long	get_time(void);
t_request	*pq_pop(t_dongle *dongle);
long		ft_atol(char *s);
void		*coder_cycle(void *arg);
void		clean_up(t_simulator *simulator);
void		do_compile(t_coder *coder);
void		do_debug(t_coder *coder);
void		do_refactor(t_coder *coder);
void		grab_dongles(t_coder *coder);
void		handle_single_coder(t_coder *coder);
void		ms_sleep(long long time_in_ms);
void		pq_push(t_dongle *dongle, t_request *req, int scheduler);
void		print_action(t_coder *coder, char *action);
void		release_dongles(t_coder *coder);
void		run_simulation(t_simulator *sim);
int			initializer(t_config *config, t_simulator *sim);
int			main(int c, char **av);
int			parser(int c, char **av, t_config *config);
int			print_usage(void);

#endif
