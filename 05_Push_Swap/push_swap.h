/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/28 16:25:46 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/04 16:09:00 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <unistd.h>
# include <stdlib.h>

typedef struct s_list
{
	int				n;
	int				index;
	struct s_list	*next;
}	t_list;

void		ft_putstr_fd(char *s, int fd);
long long	ft_atol(const char *nptr);
int			is_empty(char **asc_n);
char		**ft_split(const char *s, char c);
int			count_lst(t_list **lst);
void		ft_lstadd_back(t_list **lst, t_list *node);
t_list		*ft_lstnew(int n);

int			str_empty(char *s);
void		rotate_stack(t_list **lst, char *operation);
void		rotate_stack_both(t_list **stack_a, t_list **stack_b);
void		rev_rotate_stack(t_list **lst, char *operation);
void		rrr(t_list **stack_a, t_list **stack_b);
void		swap_stack(t_list **lst, char *operation);
void		swap_stack_both(t_list **stack_a, t_list **stack_b);
void		push_stack(t_list **stack_a, t_list **stack_b, char *operation);

void		assign_indexes(t_list **lst);
int			find_distance(t_list *lst, int n);

void		free_tab(char **tab);
void		free_stack(t_list **lst);
int			error_exit(t_list **a, t_list **b, char **tab);

void		pswp_sort_3(t_list **stack_a);
void		pswp_sort_4(t_list **stack_a, t_list **stack_b);
void		pswp_sort_5(t_list **stack_a, t_list **stack_b);
void		pswp_sort(t_list **stack_a, t_list **stack_b, unsigned int count);

int			non_digits(t_list **stack_a, char **tab, int j);
int			out_of_range(t_list **stack_a, long long *n, char **tab, int *j);
int			node_exists(t_list **stack_a, char **tab, long long n);
int			create_and_store(t_list **stack_a, char **tab, long long n);

#endif
