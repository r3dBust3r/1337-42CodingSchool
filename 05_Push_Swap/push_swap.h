/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/28 16:25:46 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/03 15:03:59 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <unistd.h>
# include <stdlib.h>

typedef struct push_swap
{
	int					n;
	int					index;
	struct push_swap	*next;
}	ps_list;

void	ft_putstr_fd(char *s, int fd);
long	ft_atol(const char *nptr);
int		ft_number(char *s);
int		is_empty(char **asc_n);
char	**ft_split(const char *s, char c);
int		count_lst(ps_list **lst);
void	ft_lstadd_back(ps_list **lst, ps_list *new);
ps_list	*ft_lstnew(int n);
void	swap_stack(ps_list **lst, char *operation);
void	swap_stack_both(ps_list **stack_a, ps_list **stack_b);
void	push_stack(ps_list **stack_a, ps_list **stack_b, char *operation);
void	rotate_stack(ps_list **lst, char *operation);
void	rotate_stack_both(ps_list **stack_a, ps_list **stack_b);
void	rev_rotate_stack(ps_list **lst, char *operation);
void	rrr(ps_list **stack_a, ps_list **stack_b);
void	pswp_sort_3(ps_list **stack_a, ps_list **stack_b);
int		find_distance(ps_list *lst, int n);
void	assign_indexes(ps_list **lst);
void	pswp_sort(ps_list **stack_a, ps_list **stack_b, unsigned int count);

#endif
