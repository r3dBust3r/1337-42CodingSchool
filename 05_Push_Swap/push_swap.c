/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/28 16:25:30 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/01 13:43:00 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

/************ LINKED LIST STRUCTURE ************/
typedef struct push_swap
{
	int n;
	int index;
	struct push_swap *next;
} ps_list;
/************ LINKED LIST STRUCTURE ************/

void	ft_putstr(char *s)
{
	unsigned int	i;

	i = 0;
	while (s[i])
	{
		write(1, &s[i], 1);
		i++;
	}
}

long ft_atol(const char *nptr)
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
	int i = 0;
	while (s[i])
	{
		if (s[i] < '0' || s[i] > '9')
			return (0);
		i++;
	}
	return (1);
}

int is_empty(char **asc_n)
{
    int i = 0;
    while (asc_n[i])
        i++;
    if (i == 0)
		return 1;
	return 0; 
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

/**************** count_lst ****************/
int count_lst(ps_list **lst)
{
    int i = 0;
    ps_list *current = *lst;
    while (current)
    {
        current = current->next;
        i++;
    }
    return i;
}
/**************** count_lst ****************/

/**************** ft_lstadd_back ****************/
void	ft_lstadd_back(ps_list **lst, ps_list *new)
{
	ps_list	*temp;

	if (!lst || !new)
		return ;
	if (!*lst)
	{
		*lst = new;
		return ;
	}
	temp = *lst;
	while (temp->next)
		temp = temp->next;
	temp->next = new;
}
/**************** ft_lstadd_back ****************/

/**************** ft_lstnew ****************/
ps_list	*ft_lstnew(int n, int *index)
{
	ps_list	*new_node;

	new_node = malloc(sizeof(ps_list));
	if (!new_node)
		return (NULL);
	new_node->n = n;
	new_node->index = *index;
	new_node->next = NULL;
	return (new_node);
}
/**************** ft_lstnew ****************/

/**************** operations ****************/
/** sa() & sb() */
void swap_stack(ps_list **lst, char *operation)
{
    if (count_lst(lst) < 2)
        return;
    ps_list *first = *lst;
    ps_list *second = (*lst)->next;
    first->next = second->next;
    second->next = first;
    *lst = second;
	ft_putstr(operation);
	ft_putstr("\n");
}

/** ss() */
void swap_stack_both(ps_list **stack_a, ps_list **stack_b)
{
	swap_stack(stack_a, "sa");
	swap_stack(stack_b, "sb");
}

/** pa() & pb() */
void push_stack(ps_list **stack_a, ps_list **stack_b, char *operation)
{
	if (operation == "pa")
	{
		if (count_lst(stack_b) == 0)
			return;
		ps_list *node_to_push = *stack_b;
		*stack_b = (*stack_b)->next;
		node_to_push->next = *stack_a;
		*stack_a = node_to_push;
		ft_putstr("pa\n");
	}
	else
	{
		if (count_lst(stack_a) == 0)
			return;
		ps_list *node_to_push = *stack_a;
		*stack_a = (*stack_a)->next;
		node_to_push->next = *stack_b;
		*stack_b = node_to_push;
		ft_putstr("pb\n");
	}
}

/** ra() & rb() */
void rotate_stack(ps_list **lst, char* operation)
{
	if (count_lst(lst) == 0)
	    return;
	ps_list *first = *lst;
	ps_list *second = (*lst)->next;
	ps_list *last = *lst;
	while (last->next)
	    last = last->next;
	last->next = first;
	first->next = NULL;
	*lst = second;
    ft_putstr(operation);
    ft_putstr("\n");
}

/** rr() */
void rotate_stack_both(ps_list **stack_a, ps_list **stack_b)
{
	rotate_stack(stack_a, "ra");
	rotate_stack(stack_b, "rb");
}

/** rra() & rrb() */
void rev_rotate_stack(ps_list **lst, char *operation)
{
	int n_lst = count_lst(lst);
	if (n_lst < 2)
		return;
	ps_list *last = *lst;
	while (last->next)
	    last = last->next;
	ps_list *second_last = *lst;
	int i = 0;
	while (i < n_lst - 2)
	{
	    second_last = second_last->next;
	    i++;
	}
	second_last->next = NULL;
	last->next = *lst;
	*lst = last;
	ft_putstr(operation);
	ft_putstr("\n");
}

/** rrr() */
void rrr(ps_list **stack_a, ps_list **stack_b)
{
	rev_rotate_stack(stack_a, "rra");
	rev_rotate_stack(stack_b, "rrb");
}
/**************** operations ****************/

/**************** Testing functions **************/
void print_lst(ps_list **lst)
{
	ps_list *current = *lst;
	printf("\n----------\n");
	while (current)
	{
		printf("  %d", current->n);
		current = current->next;
		if (current) printf("\n");
	}
	printf("\n----------\n");
}
/**************** Testing functions **************/

/****************** Sorting ******************/
void pswp_sort_3(ps_list **stack_a, ps_list **stack_b)
{
	ps_list *nd_1 = *stack_a;
	ps_list *nd_2 = (*stack_a)->next;
	ps_list *nd_3 = (*stack_a)->next->next;

	if (nd_1->n < nd_2->n && nd_2->n < nd_3->n) // 1 2 3
	{
		return;
	}
	if (nd_1->n < nd_2->n && nd_1->n < nd_3->n && nd_2->n > nd_3->n) // 1 3 2
	{
		swap_stack(stack_a, "sa");
		rotate_stack(stack_a, "ra");
	}
	if (nd_1->n > nd_2->n && nd_2->n < nd_3->n && nd_1->n < nd_3->n) // 2 1 3
	{
		swap_stack(stack_a, "sa");
	}
	if (nd_1->n > nd_2->n && nd_1->n > nd_3->n && nd_2->n < nd_3->n) // 3 1 2
	{
		rotate_stack(stack_a, "ra");
	}
	if (nd_1->n < nd_2->n && nd_1->n > nd_3->n && nd_2->n > nd_3->n) // 2 3 1
	{
		rev_rotate_stack(stack_a, "rra");
	}
	if (nd_1->n > nd_2->n && nd_1->n > nd_3->n && nd_2->n > nd_3->n) // 3 2 1
	{
		swap_stack(stack_a, "sa");
		rev_rotate_stack(stack_a, "rra");
	}
}

/********** TEMP FUNCTIONS ***********/
int find_index(ps_list **lst, int n)
{
	int i = 0;
	ps_list *current = *lst;
	while (current)
	{
		if (current->n == n)
			break;
		current = current->next;
		i++;
	}
	return i;
}
/********** TEMP FUNCTIONS ***********/

void pswp_sort(ps_list **stack_a, ps_list **stack_b, unsigned int count)
{
	// swap_stack(stack_a, "sa"); // sa()
	// swap_stack(stack_b, "sb"); // sb()
	// swap_stack_both(stack_a, stack_b); // ss()
	
	// push_stack(stack_a, stack_b, "pa"); // pa()
	// push_stack(stack_a, stack_b, "pb"); // pb()
	
	// rotate_stack(stack_a, "ra"); // ra()
	// rotate_stack(stack_b, "rb"); // rb()
	// rotate_stack_both(stack_a, stack_b); // rr()
	
	// rev_rotate_stack(stack_a, "rra"); // rra()
	// rev_rotate_stack(stack_b, "rrb"); // rrb()
	// rrr(stack_a, stack_b); // rrr()

	if (count == 2)
	{
		
	}
	else if (count == 3)
	{
		// sort 3 nodes
		pswp_sort_3(stack_a, stack_b);
	}
	else if (count == 4) {}
	else if (count == 5) {}
	else
	{
		int chunk_size = (count <= 100) ? (count / 5) : (count / 11); // Strategy from [cite: 201, 286]
		int limit = chunk_size;
		int pushed = 0;

		while (*stack_a)
		{
			// 1. Find the cheapest node with index < limit [cite: 212, 235, 237]
			ps_list *hold_first = *stack_a;
			ps_list *current = *stack_a;
			while (current->index < limit)
			{
				if (current->n < hold_first->n)
				{
					hold_first = current;
				}
				current = current->next;
			}

			// 2. Move it to top of A and pb [cite: 245, 278, 279]
			unsigned int distance = find_index(stack_a, hold_first->n);
			char *operation = "ra";
			if (distance > count / 2)
			{
				distance = count - distance;
			}
			int i = 0;
			while (i < distance)
			{
				if (operation == "ra")
				{
					rotate_stack(stack_a, "ra"); // ra()
				}
				else
				{
					rev_rotate_stack(stack_a, "rra"); // rra()
				}
				i++;
			}
			push_stack(stack_a, stack_b, "pb"); // pb()

			// 3. If you've pushed 'limit' amount of numbers, limit += chunk_size [cite: 280]
			pushed++;
			if (pushed == limit)
			{
				limit += chunk_size;
			}
		}
	}
}
/****************** Sorting ******************/

int main(int ac, char **av)
{
	/** no parameters */
	if (ac == 1)
	{
		printf("Error: No params!\n");
		return 1;
	}

	ps_list	*stack_a = NULL;
	ps_list	*node;
	ps_list	*current;

	char	**asc_n;
	
	int		i = 1; // av index
	int		j = 0; // asc_n index returned by split
	int		k = 0; // asc_n[j] characters index
	int		index = 0; // node index
	long	n = 0; // number

	while (i < ac)
	{
		// split each argument
		asc_n = ft_split(av[i], ' ');

		// TODO: Check if asc_n empty
		if (is_empty(asc_n))
		{
			printf("Error: Found empty str!\n");
			return 1;
		}

		// 1 2 3 "45 67"
		j = 0;
		while (asc_n[j])
		{
			// TODO: Validate if asc_n[j] is a valid number.
			k = 0;
			while (asc_n[j][k])
			{
				if (k == 0 && (asc_n[j][k] == '+' || asc_n[j][k] == '-'))
					k++;
				if (asc_n[j][k] < '0' || asc_n[j][k] > '9')
				{
					printf("Error: Not a valid number!\n");
					return 1;
				}
				k++;
			}

			// TODO: Convert asc_n[j] to a long using ft_atol.
			n = ft_atol(asc_n[j]);

			// printf("%ld\n", n);

			// TODO: Check for Integer Overflow (is it within INT_MIN and INT_MAX?).
			if (n < -2147483648 || n > 2147483647)
			{
				printf("Error: Out of range [-2147483648, 2147483647]\n");
				return 1;
			}

			// TODO: Check for Duplicates (look through your stack to see if the number is already there).
			current = stack_a;
			while (current)
			{
				if (n == current->n)
				{
					printf("Error: Found duplicate!\n");
					return 1;
				}
				current = current->next;
			}

			// TODO: Add to Stack: Create a new node and add it to the bottom of Stack A.
			node = ft_lstnew(n, &index);
			ft_lstadd_back(&stack_a, node);
			index++;

			j++;
		}

		i++;
	}

	ps_list *stack_b = NULL;

	// printf("\nSTACK_A");
	// print_lst(&stack_a);
	// printf("\nSTACK_B");
	// print_lst(&stack_b);

	pswp_sort(&stack_a, &stack_b, count_lst(&stack_a));

	printf("\nSTACK_A");
	print_lst(&stack_a);
	// printf("\nSTACK_B");
	// print_lst(&stack_b);

	return 0;
}

/**
 * 
 * TODO: Check malloc
 * TODO: Check leaks
 * TODO: Remove forbidden functions [printf, etc...]
 * TODO: Remove forbidden headers
 * TODO: Remove testing functions
 * TODO: Create Makefile
 * 
 *	2				Swap if needed
 *	3				Specialized "Case" sorting (max 2 moves) 
 *	4 - 6			Push smallest to B until 3 left in A 
 *	7 - 100			5 Chunks (approx. 20 numbers each) 
 *	101 - 500+		11+ Chunks to minimize rotations
 *
 */