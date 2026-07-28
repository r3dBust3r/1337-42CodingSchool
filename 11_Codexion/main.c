/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 17:46:23 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/28 22:40:23 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"
#include <pthread.h>

static void print_coder(t_coder coder) // FOR DEB
{
	int l_id = -1;
	int r_id = -1;

	if (coder.left_dongle != NULL)
		l_id = coder.left_dongle->id;

	if (coder.right_dongle != NULL)
		r_id = coder.right_dongle->id;

	printf("Coder: %d\n", coder.id);
	printf("  -- thread id: %ld\n", coder.thread_id);
	printf("  -- last compile: %lld\n", coder.last_compile);
	printf("  -- left dongle: %d\n", l_id);
	printf("  -- right dongle: %d\n", r_id);
	printf("  -- compiles completed: %d\n", coder.compiles_completed);
	printf("------------------------\n");
}


static void print_dongle(t_dongle dongle) // FOR BED
{
	printf("Dongle: %d\n", dongle.id);
	printf("  -- is available: %d\n", dongle.is_available);
	printf("  -- available at: %lld\n", dongle.available_at);
	printf("------------------------\n");
}


static void print_simulation(t_simulator *simulator)
{
	printf("Simulator\n");
	printf("  -- start time: %lld\n", simulator->start_time);
	printf("  -- running: %d\n", simulator->is_running);	
}


long long get_time()
{
	struct timeval tv;
	gettimeofday(&tv, NULL);
	return ((tv.tv_sec * 1000LL) + (tv.tv_usec / 1000));
}

void clean_up(t_simulator *simulator)
{
	int i = 0;
	while (i < simulator->config->number_of_coders)
	{
		pthread_mutex_destroy(&simulator->coders[i].mutex);
		pthread_mutex_destroy(&simulator->dongles[i].mutex);
		pthread_cond_destroy(&simulator->dongles[i].cond);
		i++;
	}
	
	pthread_mutex_destroy(&simulator->print_mutex);
	pthread_mutex_destroy(&simulator->simulator_mutex);
	
	free(simulator->coders);
	free(simulator->dongles);
}

void *coder_cycle(void *arg)
{
	t_coder *coder = (t_coder *)arg;
	// CODER LIFE_CYCLE
	return NULL;
}


void run_simulation(t_simulator *simulator)
{
	long long current_time;
	int someone_burned_out = 0;

	// 1. THE MONITOR LOOP
	while (1) // Loop continuously until a break condition is met
	{
		int i = 0;
		int finished_count = 0; // Reset this every single iter

		while (i < simulator->config->number_of_coders)
		{
			t_coder *coder = &simulator->coders[i];

			pthread_mutex_lock(&coder->mutex);
			
			current_time = get_time();
			
			// Check for burnout
			if (current_time - coder->last_compile >= simulator->config->time_to_burnout)
			{
				// Lock simulator_mutex, set is_running = 0
				pthread_mutex_lock(&simulator->simulator_mutex);
				simulator->is_running = 0;
				pthread_mutex_unlock(&simulator->simulator_mutex);
				
				// Print burnout log with relative timestamp
				pthread_mutex_lock(&simulator->print_mutex);
				printf("%lld %d burned out\n", current_time - simulator->start_time, coder->id);
				pthread_mutex_unlock(&simulator->print_mutex);

				someone_burned_out = 1;
				
				// UNLOCK BEFORE BREAKING TO PREVENT DEADLOCK
				pthread_mutex_unlock(&coder->mutex); 
				break;
			}

			// Check if required_compiles is reached for this coder
			// (Assuming required_compiles is not -1, which often denotes "infinite" in these projects)
			if (coder->compiles_completed >= simulator->config->required_compiles)
			{
				finished_count++;
			}

			pthread_mutex_unlock(&coder->mutex);
			i++;
		}
		
		// If someone burned out, break the outer loop
		if (someone_burned_out)
		{
			break;
		}
		
		// If ALL coders have reached the required compiles, end the simulation
		if (finished_count == simulator->config->number_of_coders)
		{
			pthread_mutex_lock(&simulator->simulator_mutex);
			simulator->is_running = 0;
			pthread_mutex_unlock(&simulator->simulator_mutex);
			break;
		}

		usleep(1000); // Tiny sleep so the monitor doesn't consume 100% CPU
	}

	// 2. WAIT FOR THREADS TO EXIT
	int i = 0;
	while (i < simulator->config->number_of_coders)
	{
		pthread_join(simulator->coders[i].thread_id, NULL);
		i++;
	}
}


int initializer(t_config *config, t_simulator *simulator)
{
	t_dongle *dongles = malloc(sizeof(t_dongle) * config->number_of_coders);
	if (!dongles) return (1);

	t_coder *coders = malloc(sizeof(t_coder) * config->number_of_coders);
	if (!coders)
	{
		free(dongles);
		return (1);
	}

	simulator->start_time = get_time();
	simulator->is_running = 1;
	simulator->coders = coders;
	simulator->dongles = dongles;
	simulator->config = config;
	pthread_mutex_init(&simulator->print_mutex, NULL);
	pthread_mutex_init(&simulator->simulator_mutex, NULL);


	int i = 0;
	while (i < config->number_of_coders)
	{
		dongles[i].id = i + 1;
		dongles[i].is_available = 1;
		dongles[i].available_at = simulator->start_time;

		pthread_mutex_init(&dongles[i].mutex, NULL);
		pthread_cond_init(&dongles[i].cond, NULL);
		i++;
	}

	i = 0;
	while (i < config->number_of_coders)
	{
		coders[i].id = i + 1;
		coders[i].last_compile = simulator->start_time;
		coders[i].compiles_completed = 0;
		
		coders[i].left_dongle = &dongles[i];
		coders[i].right_dongle = &dongles[(i + 1) % config->number_of_coders];
		
		coders[i].simulator = simulator;
		pthread_mutex_init(&coders[i].mutex, NULL);
		i++;
	}

	i = 0;
	while (i < config->number_of_coders)
	{
		if (pthread_create(
			&coders[i].thread_id,
			NULL,
			coder_cycle,
			&coders[i]
		) != 0)
		{
			return (1);
		}
		i++;
	}

	return (0);
}


int	main(int c, char **av)
{
	if (c != 9)
		return (print_usage());

	t_config config;

	if (parser(c, av, &config))
		return (1);

	t_simulator simulator;
	initializer(&config, &simulator);
	run_simulation(&simulator);



	// for (int i = 0; i < config.number_of_coders; i++) print_dongle(simulator.dongles[i]);
	// printf("\n\n\033[31m====================================\033[37m\n\n\n");
	// for (int i = 0; i < config.number_of_coders; i++) print_coder(simulator.coders[i]);
	
	clean_up(&simulator);
	return (0);
}
