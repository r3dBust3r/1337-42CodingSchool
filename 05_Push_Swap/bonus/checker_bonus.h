/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker_bonus.h                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/06 23:20:41 by ottalhao          #+#    #+#             */
/*   Updated: 2026/01/07 17:57:56 by ottalhao         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CHECKER_BONUS_H
# define CHECKER_BONUS_H

# include <unistd.h>
# include <stdlib.h>

typedef struct s_list
{
	int				n;
	struct s_list	*next;
}	t_list;

# ifndef BUFFER_SIZE
#  define BUFFER_SIZE 42
# endif

# if BUFFER_SIZE < 0
#  undef BUFFER_SIZE
#  define BUFFER_SIZE 0
# endif

char		*get_next_line(int fd);
size_t		ft_strlen(const char *s);
char		*ft_strchr(const char *s, int c);
char		*ft_strdup(const char *s);
char		*ft_strjoin(char const *s1, char const *s2);

int			str_empty(char *s);
void		push_stack(t_list **stack_a, t_list **stack_b, char *op);
void		rotate_stack(t_list **lst);
void		rotate_stack_both(t_list **stack_a, t_list **stack_b);
void		rev_rotate_stack(t_list **lst);
void		rrr(t_list **stack_a, t_list **stack_b);
void		swap_stack(t_list **lst);
void		swap_stack_both(t_list **stack_a, t_list **stack_b);
char		**ft_split(const char *s, char c);
int			is_empty(char **asc_n);
void		free_tab(char **tab);
void		free_stack(t_list **lst);
int			error_exit(t_list **a, t_list **b, char **tab);
int			non_digits(t_list **stack_a, char **tab, int j);
int			out_of_range(t_list **stack_a, long long *n, char **tab, int *j);
int			node_exists(t_list **stack_a, char **tab, long long n);
int			create_and_store(t_list **stack_a, char **tab, long long n);
void		ft_putstr_fd(char *s, int fd);
long long	ft_atol(const char *nptr);
t_list		*ft_lstnew(int n);
void		ft_lstadd_back(t_list **lst, t_list *node);
int			count_lst(t_list **lst);

int			ft_strcmp(const char *s1, const char *s2);
int			exec_swap(char *line, t_list **a, t_list **b);
int			exec_push(char *line, t_list **a, t_list **b);
int			exec_rotate(char *line, t_list **a, t_list **b);
int			exec_instruction(char *line, t_list **a, t_list **b);
int			checker_error_exit(t_list **a, t_list **b, char *line);
void		check_result(t_list *stack_a, t_list *stack_b);

#endif
