/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/28 16:25:30 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 11:15:07 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */



#include "stdio.h" // REMOVE ME 


#include <unistd.h>
#include <stdlib.h>

typedef struct	s_list
{
	int				n;
	int				index;
	struct s_list	*next;
} t_list;

void	ft_putstr_fd(char *s, int fd)
{
	unsigned int	i;

	i = 0;
	while (s[i])
	{
		write(fd, &s[i], 1);
		i++;
	}
}

long	ft_atol(const char *nptr)
{
	long	r;
	int		s;
	int		i;

	s = 1;
	r = 0;
	i = 0;
	while (nptr[i] == 32 || (nptr[i] >= 9 && nptr[i] <= 13))
		i++;
	if (nptr[i] == '+' || nptr[i] == '-')
	{
		if (nptr[i] == '-')
			s = -1;
		i++;
	}
	while (nptr[i] && nptr[i] >= '0' && nptr[i] <= '9')
		r = r * 10 + (nptr[i++] - '0');
	return (r * s);
}

int	ft_number(char *s)
{
	int	i;

	i = 0;
	while (s[i])
	{
		if (s[i] < '0' || s[i] > '9')
			return (0);
		i++;
	}
	return (1);
}

int	is_empty(char **asc_n)
{
	int	i;

	i = 0;
	while (asc_n[i])
		i++;
	if (i == 0)
		return (1);
	return (0);
}

/******************* split *******************/
static int	count_elms(const char *s, char c)
{
	int	i;
	int	elms;

	elms = 0;
	i = 0;
	if (!s)
		return (0);
	while (s[i])
	{
		while (s[i] == c)
			i++;
		if (s[i])
			elms++;
		while (s[i] && s[i] != c)
			i++;
	}
	return (elms);
}

static void	free_all(char **arr, int filled)
{
	int	i;

	i = 0;
	while (i < filled)
	{
		free(arr[i]);
		i++;
	}
	free(arr);
}

static char	*alloc_word(const char *s, int start, int end)
{
	int		len;
	int		j;
	char	*word;

	len = end - start;
	word = malloc(sizeof(char) * (len + 1));
	if (!word)
		return (NULL);
	j = 0;
	while (j < len)
	{
		word[j] = s[start + j];
		j++;
	}
	word[len] = '\0';
	return (word);
}

static int	fill_parent_array(const char *s, char c, char **arr, int i)
{
	int		start;
	int		index;
	char	*word;

	index = 0;
	while (s[i])
	{
		while (s[i] == c)
			i++;
		if (!s[i])
			break ;
		start = i;
		while (s[i] && s[i] != c)
			i++;
		word = alloc_word(s, start, i);
		if (!word)
		{
			free_all(arr, index);
			return (-1);
		}
		arr[index++] = word;
	}
	arr[index] = NULL;
	return (0);
}

char	**ft_split(const char *s, char c)
{
	char	**arr;
	int		count;
	int		i;

	i = 0;
	if (!s)
		return (NULL);
	count = count_elms(s, c);
	arr = malloc(sizeof(char *) * (count + 1));
	if (!arr)
		return (NULL);
	if (fill_parent_array(s, c, arr, i) == -1)
		return (NULL);
	return (arr);
}
/******************* split *******************/

int	count_lst(t_list **lst)
{
	t_list	*current;
	int		i;

	i = 0;
	current = *lst;
	while (current)
	{
		current = current->next;
		i++;
	}
	return (i);
}

void	ft_lstadd_back(t_list **lst, t_list *node)
{
	t_list	*temp;

	if (!lst || !node)
		return ;
	if (!*lst)
	{
		*lst = node;
		return ;
	}
	temp = *lst;
	while (temp->next)
		temp = temp->next;
	temp->next = node;
}

t_list	*ft_lstnew(int n)
{
	t_list	*new_node;

	new_node = malloc(sizeof(t_list));
	if (!new_node)
		return (NULL);
	new_node->n = n;
	new_node->index = -1;
	new_node->next = NULL;
	return (new_node);
}
int str_empty(char *s)
{
	if (!s || s[0] == '\0')
		return 1;
	return 0;
}

void	swap_stack(t_list **lst, char *operation)
{
	if (count_lst(lst) < 2)
		return;
	t_list *first = *lst;
	t_list *second = (*lst)->next;
	first->next = second->next;
	second->next = first;
	*lst = second;
	if (!str_empty(operation))
	{
		ft_putstr_fd(operation, 1);
		ft_putstr_fd("\n", 1);
	}
}

void	swap_stack_both(t_list **stack_a, t_list **stack_b)
{
	swap_stack(stack_a, "");
	swap_stack(stack_b, "");
	ft_putstr_fd("ss\n", 1);
}

void	push_stack(t_list **stack_a, t_list **stack_b, char *operation)
{
	if (operation[0] == 'p' && operation[1] == 'a')
	{
		if (count_lst(stack_b) == 0)
			return;
		t_list *node_to_push = *stack_b;
		*stack_b = (*stack_b)->next;
		node_to_push->next = *stack_a;
		*stack_a = node_to_push;
		ft_putstr_fd("pa\n", 1);
	}
	else
	{
		if (count_lst(stack_a) == 0)
			return;
		t_list *node_to_push = *stack_a;
		*stack_a = (*stack_a)->next;
		node_to_push->next = *stack_b;
		*stack_b = node_to_push;
		ft_putstr_fd("pb\n", 1);
	}
}

void	rotate_stack(t_list **lst, char* operation)
{
	if (count_lst(lst) < 2)
		return;
	t_list *first = *lst;
	t_list *second = (*lst)->next;
	t_list *last = *lst;
	while (last->next)
		last = last->next;
	last->next = first;
	first->next = NULL;
	*lst = second;
	if (!str_empty(operation))
	{		
		ft_putstr_fd(operation, 1);
		ft_putstr_fd("\n", 1);
	}
}
	
void	rotate_stack_both(t_list **stack_a, t_list **stack_b)
{
	rotate_stack(stack_a, "");
	rotate_stack(stack_b, "");
	ft_putstr_fd("rr\n", 1);
}

void	rev_rotate_stack(t_list **lst, char *operation)
{
	int n_lst = count_lst(lst);
	if (n_lst < 2)
		return;
	t_list *last = *lst;
	while (last->next)
	    last = last->next;
	t_list *second_last = *lst;
	int i = 0;
	while (i < n_lst - 2)
	{
		second_last = second_last->next;
		i++;
	}
	second_last->next = NULL;
	last->next = *lst;
	*lst = last;
	if (!str_empty(operation))
	{	
		ft_putstr_fd(operation, 1);
		ft_putstr_fd("\n", 1);
	}
}

void	rrr(t_list **stack_a, t_list **stack_b)
{
	rev_rotate_stack(stack_a, "");
	rev_rotate_stack(stack_b, "");
	ft_putstr_fd("rrr\n", 1);
}

int	find_distance(t_list *lst, int n)
{
	int i = 0;
	while (lst)
	{
		if (lst->n == n)
			break;
		lst = lst->next;
		i++;
	}
	return i;
}

void assign_indexes(t_list **lst)
{
	unsigned int count = count_lst(lst);
	unsigned int index = 0;
	unsigned int i = 0;
	while (i < count)
	{
		t_list *smallest_node = NULL;
		t_list *current = *lst;
		while (current)
		{
			if (current->index == -1)
			{
				smallest_node = current;
				break;
			}
			current = current->next;
		}
		current = *lst;
		while (current)
		{
			if (current->index == -1)
			{
				if (current->n < smallest_node->n)
				{
					smallest_node = current;
				}
			}
			current = current->next;
		}
		smallest_node->index = index;
		index++;
		i++;
	}
}

void	pswp_sort_3(t_list **stack_a, t_list **stack_b)
{
	t_list	*nd_1 = *stack_a;
	t_list	*nd_2 = (*stack_a)->next;
	t_list	*nd_3 = (*stack_a)->next->next;

	if (nd_1->n < nd_2->n && nd_2->n < nd_3->n) 
		return;
	if (nd_1->n < nd_2->n && nd_1->n < nd_3->n && nd_2->n > nd_3->n) 
	{
		swap_stack(stack_a, "sa");
		rotate_stack(stack_a, "ra");
	}
	if (nd_1->n > nd_2->n && nd_2->n < nd_3->n && nd_1->n < nd_3->n) 
		swap_stack(stack_a, "sa");
	if (nd_1->n > nd_2->n && nd_1->n > nd_3->n && nd_2->n < nd_3->n) 
		rotate_stack(stack_a, "ra");
	if (nd_1->n < nd_2->n && nd_1->n > nd_3->n && nd_2->n > nd_3->n) 
		rev_rotate_stack(stack_a, "rra");
	if (nd_1->n > nd_2->n && nd_1->n > nd_3->n && nd_2->n > nd_3->n) 
	{
		swap_stack(stack_a, "sa");
		rev_rotate_stack(stack_a, "rra");
	}
}

void pswp_sort_4(t_list **stack_a, t_list **stack_b)
{
	t_list *smallest_node = *stack_a;
	t_list *current = *stack_a;
	while (current)
	{
		if (current->index < smallest_node->index)
			smallest_node = current;
		current = current->next;
	}
	int distance = find_distance(*stack_a, smallest_node->n);
	while (distance)
	{
		rotate_stack(stack_a, "ra");
		distance--;
	}
	push_stack(stack_a, stack_b, "pb");
	pswp_sort_3(stack_a, stack_b);
	push_stack(stack_a, stack_b, "pa");
}

void	pswp_sort_5(t_list **stack_a, t_list **stack_b)
{
	int	i = 2;
	while (i)
	{
		t_list *smallest_node = *stack_a;
		t_list *current = *stack_a;
		while (current)
		{
			if (current->index < smallest_node->index)
				smallest_node = current;
			current = current->next;
		}
		int distance = find_distance(*stack_a, smallest_node->n);
		char *operation = "ra";
		if (distance > 2)
		{
			distance = count_lst(stack_a) - distance;
			operation = "rra";
		}
		while (distance)
		{
			if (operation[0] == 'r' && operation[1] == 'a')
				rotate_stack(stack_a, "ra");
			else
				rev_rotate_stack(stack_a, "rra");
			distance--;
		}
		push_stack(stack_a, stack_b, "pb");
		i--;
	}
	pswp_sort_3(stack_a, stack_b);
	push_stack(stack_a, stack_b, "pa");
	push_stack(stack_a, stack_b, "pa");
}

void pswp_sort(t_list **stack_a, t_list **stack_b, unsigned int count)
{
	if (count == 2)
	{
		if ((*stack_a)->index > (*stack_a)->next->index)
			swap_stack_both(stack_a, stack_b);
	}
	else if (count == 3)
		pswp_sort_3(stack_a, stack_b);
	else if (count == 4)
		pswp_sort_4(stack_a, stack_b);
	else if (count == 5)
		pswp_sort_5(stack_a, stack_b);
	else
	{
		int chunk_size;
		if (count < 100)
			chunk_size = count;
		else if (count < 300)
			chunk_size = count / 7;
		else
			chunk_size = count / 15;

		int pushed = 0;
		while (*stack_a)
		{
			if ((*stack_a)->index <= pushed)
			{
				push_stack(stack_a, stack_b, "pb");
				rotate_stack(stack_b, "rb");
				pushed++;
			}
			else if ((*stack_a)->index < pushed + chunk_size)
			{
				push_stack(stack_a, stack_b, "pb");
				pushed++;
			}
			else
				rotate_stack(stack_a, "ra");
		}

		while (*stack_b)
		{
			t_list *biggest_node = *stack_b;
			t_list *current = *stack_b;
			while (current) {
				if (current->index > biggest_node->index)
					biggest_node = current;
				current = current->next;
			}
			int distance = find_distance(*stack_b, biggest_node->n);
			if (distance <= count_lst(stack_b) / 2)
			{
				while (distance)	
				{
					rotate_stack(stack_b, "rb");
					distance--;
				}
			} else {
				distance = count_lst(stack_b) - distance;
				while (distance)
				{
					rev_rotate_stack(stack_b, "rrb");
					distance--;
				}
			}
			push_stack(stack_a, stack_b, "pa");
		}
	}
}


void	free_tab(char **tab)
{
	int i = 0;

	if (!tab)
		return;
	while (tab[i])
	{
		free(tab[i]);
		i++;
	}
	free(tab);
}


void	free_stack(t_list **lst)
{
	t_list	*tmp;

	while (*lst)
	{
		tmp = (*lst)->next;
		free(*lst);
		*lst = tmp;
	}
}


int	error_exit(t_list **a, t_list **b, char **tab)
{
	if (a)
		free_stack(a);
	if (b)
		free_stack(b);
	if (tab)
		free_tab(tab);
	ft_putstr_fd("Error\n", 2);
	return (1);
}


/**************** Testing functions **************/
#include <stdio.h> // REMOVE ME
void print_lst(t_list **lst)
{
	t_list *current = *lst;
	printf("\n---------------------\n");
	while (current)
	{
		printf("  idx: %d\t|\tval: %d", current->index, current->n);
		current = current->next;
		if (current) printf("\n");
	}
	printf("\n---------------------\n");
}
/**************** Testing functions **************/

int	main(int ac, char **av)
{
	if (ac == 1)
		return (1);

	t_list	*stack_a = NULL;
	t_list	*node;
	t_list	*current;

	char	**tab;
	
	int		i = 1;
	int		j = 0;
	int		k = 0;
	long	n = 0;

	while (i < ac)
	{
		tab = ft_split(av[i], ' ');
		if (!tab || is_empty(tab))
			return error_exit(&stack_a, NULL, tab);
		j = 0;
		while (tab[j])
		{
			k = 0;
			while (tab[j][k])
			{
				if (k == 0 && (tab[j][k] == '+' || tab[j][k] == '-'))
					k++;
				if (tab[j][k] < '0' || tab[j][k] > '9')
					return error_exit(&stack_a, NULL, tab);
				k++;
			}
			n = ft_atol(tab[j]);
			if (n < -2147483648 || n > 2147483647)
				return error_exit(&stack_a, NULL, tab);
			current = stack_a;
			while (current)
			{
				if (n == current->n)
					return error_exit(&stack_a, NULL, tab);
				current = current->next;
			}
			node = ft_lstnew(n);
			if (!node)
				return error_exit(&stack_a, NULL, tab);
			ft_lstadd_back(&stack_a, node);
			j++;
		}
		free_tab(tab);
		tab = NULL;
		i++;
	}
	
	t_list *stack_b = NULL;
	assign_indexes(&stack_a);
	pswp_sort(&stack_a, &stack_b, count_lst(&stack_a));

	print_lst(&stack_a); // REMOVE ME LATER
	
	free_stack(&stack_a);
	free_stack(&stack_b);

	return 0;
}

/**
 * 
 * TODO: [+] Check malloc
 * TODO: [+] push_swap to s_list
 * TODO: [+] ps_list to t_list
 * TODO: [+] Putfd -> 2
 * TODO: [ ] Check leaks
 * TODO: [ ] Doesn't Handle to 24, Fix it
 * TODO: [ ] Create Makefile
 * TODO: [ ] Remove testing functions
 * TODO: [ ] Remove forbidden functions [printf, etc...]
 * TODO: [ ] Remove forbidden headers
 * TODO: [ ] Remove all comments
 * TODO: [ ] Norminette
 * TODO: [ ] Create Markdown
 * TODO: [ ] Push
 * 
 */