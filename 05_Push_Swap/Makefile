# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/01/03 14:50:37 by ottalhao          #+#    #+#              #
#    Updated: 2026/01/04 16:09:21 by ottalhao         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME        = push_swap
CC          = cc
CFLAGS      = -Wall -Wextra -Werror
SRCS        = ft_lstnew.c ft_lstadd_back.c count_lst.c assign_indexes.c find_distance.c \
              ft_putstr_fd.c ft_split.c ft_atol.c is_empty.c free_mem.c pswp_oprs_swp.c \
			  pswp_oprs_push.c pswp_oprs_rot.c pswp_sort_3.c pswp_sort_4.c pswp_sort_5.c \
			  pswp_sort.c push_swap.c main-helpers.c
OBJS        = $(SRCS:.c=.o)
HEADERS     = push_swap.h

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re