/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 17:46:23 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/30 22:40:19 by ottalhao         ###   ########.fr       */
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

void ms_sleep(long long time_in_ms)
{
    long long start = get_time();
    while (get_time() - start < time_in_ms)
        usleep(100);
}

void print_action(t_coder *coder, char *action)
{
    pthread_mutex_lock(&coder->simulator->simulator_mutex);
    if (!coder->simulator->is_running)
    {
        pthread_mutex_unlock(&coder->simulator->simulator_mutex);
        return;
    }
    pthread_mutex_unlock(&coder->simulator->simulator_mutex);

    long long action_time = get_time() - coder->simulator->start_time;
    
    pthread_mutex_lock(&coder->simulator->print_mutex);

	if (coder->simulator->is_running)
        printf("%lld %d %s\n", action_time, coder->id, action);

    pthread_mutex_unlock(&coder->simulator->print_mutex);
}


void pq_push(t_dongle *dongle, t_request *request, int scheduler)
{
    dongle->requests[dongle->queue_size] = request;

    if (dongle->queue_size == 1)
    {
        int swap = 0;

        if (scheduler == 0) // FIFO
        {
            if (dongle->requests[0]->creation_time > dongle->requests[1]->creation_time)
                swap = 1;
        }
        else // EDF
        {
            if (dongle->requests[0]->deadline > dongle->requests[1]->deadline)
                swap = 1;
        }

        if (swap) // SWAP IF THE NEW REQUESTS IS LOWER
        {
            t_request *temp = dongle->requests[0];
            dongle->requests[0] = dongle->requests[1];
            dongle->requests[1] = temp;
        }
    }

    dongle->queue_size++;
}

t_request *pq_pop(t_dongle *dongle)
{
    if (dongle->queue_size == 0)
        return NULL;

    t_request *popped = dongle->requests[0];

    if (dongle->queue_size == 2)
        dongle->requests[0] = dongle->requests[1];

    dongle->queue_size--;
    return popped;
}

void grab_one_dongle(t_coder *coder, t_dongle *dongle)
{
	long long burn_out_time = coder->simulator->config->time_to_burnout;
	int scheduler = coder->simulator->config->scheduler;

	// creating a new request
    t_request req;
    req.coder = coder;
	req.creation_time = get_time();
    req.deadline = coder->last_compile + burn_out_time;

	pthread_mutex_lock(&dongle->mutex);
	pq_push(dongle, &req, scheduler);

	while (
		(!dongle->is_available) ||
		(get_time() < dongle->available_at) ||
		(dongle->requests[0]->coder != coder)
	)
	{
		pthread_cond_wait(&dongle->cond, &dongle->mutex);
	}
	
	pq_pop(dongle);
	dongle->is_available = 0;
	pthread_mutex_unlock(&dongle->mutex);

    print_action(coder, "has taken a dongle");
}

void grab_dongles(t_coder *coder) {
	t_dongle *first_dongle;
	t_dongle *second_dongle;

	// (LOWEST ID FIRST) STRATEGY
	if (coder->left_dongle->id < coder->right_dongle->id)
	{
		first_dongle = coder->left_dongle;
		second_dongle = coder->right_dongle;
	}
	else
	{
		first_dongle = coder->right_dongle;
		second_dongle = coder->left_dongle;
	}

	// (EVEN/ODD) STRATEGY
	// if (coder->id % 2 != 0) // Odd
    // {
    //     first_dongle = coder->left_dongle;
    //     second_dongle = coder->right_dongle;
    // }
    // else // Even
    // {
    //     first_dongle = coder->right_dongle;
    //     second_dongle = coder->left_dongle;
    // }

	grab_one_dongle(coder, first_dongle);
	grab_one_dongle(coder, second_dongle);
}


void do_compile(t_coder *coder) {
    pthread_mutex_lock(&coder->mutex);
    coder->last_compile = get_time();
    pthread_mutex_unlock(&coder->mutex);

    print_action(coder, "is compiling");
    ms_sleep(coder->simulator->config->time_to_compile);
}


void release_dongles(t_coder *coder) {
	int cooldown = coder->simulator->config->dongle_cooldown;
	t_dongle *left_dongle = coder->left_dongle;
	t_dongle *right_dongle = coder->right_dongle;

	pthread_mutex_lock(&left_dongle->mutex);
	left_dongle->is_available = 1;
	left_dongle->available_at = get_time() + cooldown;
	pthread_cond_broadcast(&left_dongle->cond);
	pthread_mutex_unlock(&left_dongle->mutex);

	pthread_mutex_lock(&right_dongle->mutex);
	right_dongle->is_available = 1;
	right_dongle->available_at = get_time() + cooldown;
	pthread_cond_broadcast(&right_dongle->cond);
	pthread_mutex_unlock(&right_dongle->mutex);
}


void do_debug(t_coder *coder) {
    print_action(coder, "is debugging");
    ms_sleep(coder->simulator->config->time_to_debug);
}

void do_refactor(t_coder *coder) {
    print_action(coder, "is refactoring");
    ms_sleep(coder->simulator->config->time_to_refactor);
}

void handle_single_coder(t_coder *coder) {
	if (coder->left_dongle == coder->right_dongle)
	grab_dongles(coder);
}


void *coder_cycle(void *arg)
{
	t_coder *coder = (t_coder *)arg;

	if (coder->simulator->config->number_of_coders == 1)
	{
		handle_single_coder(coder);
		return NULL;
	}

	if (coder->id % 2 == 0)
        ms_sleep(10);

	while (coder->compiles_completed < coder->simulator->config->required_compiles)
	{
		pthread_mutex_lock(&coder->simulator->simulator_mutex);
		if (!coder->simulator->is_running)
		{
			pthread_mutex_unlock(&coder->simulator->simulator_mutex);
			break;
		}
		pthread_mutex_unlock(&coder->simulator->simulator_mutex);

		grab_dongles(coder);
		do_compile(coder);
		release_dongles(coder);
		do_debug(coder);
		do_refactor(coder);

		coder->compiles_completed += 1;
	}

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
			
			// Only check for burnout if the coder hasn't reached the required target
			if ((coder->compiles_completed < simulator->config->required_compiles) && 
				(current_time - coder->last_compile >= simulator->config->time_to_burnout))
			{
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
		dongles[i].requests = malloc(sizeof(t_request *) * 2);

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
