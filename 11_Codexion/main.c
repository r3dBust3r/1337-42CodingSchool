/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 17:46:23 by ottalhao          #+#    #+#             */
/*   Updated: 2026/07/31 17:13:02 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int print_usage(void)
{
    fprintf(stderr, "Error: something is wrong with your input\n\n");
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

long ft_atol(char *s)
{
	long r;
	int i;

	r = 0;
	i = 0;
	while (s[i])
	{
		if (s[i] < '0' || s[i] > '9')
			return (-1);
		r = r * 10 + s[i] - '0';
		if (r > 2147483647)
			return (-1);
		i++;
	}
	return (r);
}

int parser(int c, char **av, t_config *config)
{
	int i;
	int n;

	n = 0;
	i = 1;
	while (i < c - 1)
	{
		n = ft_atol(av[i]);
		if (n == -1)
			return print_usage();

		if (i == 1) config->number_of_coders = n;
		if (i == 2) config->time_to_burnout = n;
		if (i == 3) config->time_to_compile = n;
		if (i == 4) config->time_to_debug = n;
		if (i == 5) config->time_to_refactor = n;
		if (i == 6) config->required_compiles = n;
		if (i == 7) config->dongle_cooldown = n;

		i++;
	}

	if (strcmp(av[i], "fifo") != 0 && strcmp(av[i], "edf") != 0)
		return print_usage();

	config->scheduler = (strcmp(av[i], "fifo") == 0) ? 0 : 1;

	return (0);
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
		free(simulator->dongles[i].requests); 
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

	// Double-check is_running to prevent the Helgrind data race 
	// when comparing the state against the monitor thread
	pthread_mutex_lock(&coder->simulator->simulator_mutex);
	int safe_to_print = coder->simulator->is_running;
	pthread_mutex_unlock(&coder->simulator->simulator_mutex);

	if (safe_to_print)
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
			// Currently: If the new request (1) is OLDER than the current root (0), swap them.
			if (dongle->requests[0]->creation_time > dongle->requests[1]->creation_time)
				swap = 1;

			if (dongle->requests[0]->creation_time > dongle->requests[1]->creation_time)
				swap = 1;
		}
		else // EDF
		{
			if (dongle->requests[0]->deadline > dongle->requests[1]->deadline)
				swap = 1;
		}

		if (swap) 
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

	t_request req;
	req.coder = coder;
	req.creation_time = get_time();
		
	pthread_mutex_lock(&coder->mutex);
	req.deadline = coder->last_compile + burn_out_time;
	pthread_mutex_unlock(&coder->mutex);

	pthread_mutex_lock(&dongle->mutex);
	pq_push(dongle, &req, scheduler);

	while ((!dongle->is_available) || (dongle->requests[0]->coder != coder))
	{
		pthread_cond_wait(&dongle->cond, &dongle->mutex);
	}
		
	pq_pop(dongle);
	dongle->is_available = 0;
	pthread_mutex_unlock(&dongle->mutex);

	long long current = get_time();
	if (current < dongle->available_at)
		ms_sleep(dongle->available_at - current);

	print_action(coder, "has taken a dongle");
}

void grab_dongles(t_coder *coder) {
	t_dongle *first_dongle;
	t_dongle *second_dongle;

	if (coder->id % 2 != 0)
	{
		first_dongle = coder->left_dongle;
		second_dongle = coder->right_dongle;
	}
	else
	{
		first_dongle = coder->right_dongle;
		second_dongle = coder->left_dongle;
	}



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
	pthread_mutex_lock(&coder->left_dongle->mutex);
	print_action(coder, "has taken a dongle");
	pthread_mutex_unlock(&coder->left_dongle->mutex);
	ms_sleep(coder->simulator->config->time_to_burnout + 10); 
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

	while (1)
	{
		// Safe check for completion status to prevent data races with the monitor
		pthread_mutex_lock(&coder->mutex);
		int current_compiles = coder->compiles_completed;
		pthread_mutex_unlock(&coder->mutex);

		if (coder->simulator->config->required_compiles != -1 && current_compiles >= coder->simulator->config->required_compiles)
			break;

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

		// Safe increment to prevent data races with the monitor
		pthread_mutex_lock(&coder->mutex);
		coder->compiles_completed += 1;
		pthread_mutex_unlock(&coder->mutex);
	}

	return NULL;
}

void run_simulation(t_simulator *simulator)
{
	simulator->start_time = get_time();
	int i = 0;
	while (i < simulator->config->number_of_coders)
	{
		simulator->coders[i].last_compile = simulator->start_time;
		if (pthread_create(&simulator->coders[i].thread_id, NULL, coder_cycle, &simulator->coders[i]) != 0)
			return;
		i++;
	}

	long long current_time;
	int someone_burned_out = 0;

	while (1)
	{
		i = 0;
		int finished_count = 0;

		while (i < simulator->config->number_of_coders)
		{
			t_coder *coder = &simulator->coders[i];

			pthread_mutex_lock(&coder->mutex);
			current_time = get_time();
			
			if ((coder->compiles_completed < simulator->config->required_compiles || simulator->config->required_compiles == -1) && 
				(current_time - coder->last_compile >= simulator->config->time_to_burnout))
			{
				pthread_mutex_lock(&simulator->simulator_mutex);
				simulator->is_running = 0;
				pthread_mutex_unlock(&simulator->simulator_mutex);
				
				pthread_mutex_lock(&simulator->print_mutex);
				printf("%lld %d burned out\n", current_time - simulator->start_time, coder->id);
				pthread_mutex_unlock(&simulator->print_mutex);
				
				someone_burned_out = 1;
				pthread_mutex_unlock(&coder->mutex); 
				break;
			}

			if (simulator->config->required_compiles != -1 && coder->compiles_completed >= simulator->config->required_compiles)
			{
				finished_count++;
			}

			pthread_mutex_unlock(&coder->mutex);
			i++;
		}
		
		if (someone_burned_out || (simulator->config->required_compiles != -1 && finished_count == simulator->config->number_of_coders))
		{
			if (!someone_burned_out)
			{
				pthread_mutex_lock(&simulator->simulator_mutex);
				simulator->is_running = 0;
				pthread_mutex_unlock(&simulator->simulator_mutex);
			}
			break;
		}

		usleep(1000); 
	}

	i = 0;
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
		dongles[i].available_at = get_time();
		dongles[i].queue_size = 0;
		dongles[i].requests = malloc(sizeof(t_request *) * 2);

		pthread_mutex_init(&dongles[i].mutex, NULL);
		pthread_cond_init(&dongles[i].cond, NULL);
		i++;
	}

	i = 0;
	while (i < config->number_of_coders)
	{
		coders[i].id = i + 1;
		coders[i].compiles_completed = 0;
		
		coders[i].left_dongle = &dongles[i];
		coders[i].right_dongle = &dongles[(i + 1) % config->number_of_coders];
		
		coders[i].simulator = simulator;
		pthread_mutex_init(&coders[i].mutex, NULL);
		i++;
	}

	return (0);
}

int main(int c, char **av)
{
	if (c != 9)
		return (print_usage());

	t_config config;

	if (parser(c, av, &config))
		return (1);

	t_simulator simulator;
	if (initializer(&config, &simulator))
		return (1);
		
	run_simulation(&simulator);
	clean_up(&simulator);

	return (0);
}
