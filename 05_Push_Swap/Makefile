# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/01/03 14:50:37 by ottalhao          #+#    #+#              #
#    Updated: 2026/01/07 12:46:37 by ottalhao         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME        = push_swap
CC          = cc
CFLAGS      = -Wall -Wextra -Werror
SRCS        = ft_lstnew.c ft_lstadd_back.c count_lst.c assign_indexes.c find_distance.c \
              ft_putstr_fd.c ft_split.c ft_atol.c is_empty.c free_mem.c pswp_oprs_swp.c \
              pswp_oprs_push.c pswp_oprs_rot.c pswp_sort_3.c pswp_sort_4.c pswp_sort_5.c \
              pswp_sort.c push_swap.c main_helpers.c
OBJS        = $(SRCS:.c=.o)
HEADERS     = push_swap.h
BONUS       = bonus/checker.c bonus/checker_helpers.c bonus/main_helpers.c bonus/count_lst.c bonus/free_mem.c \
              bonus/ft_atol.c bonus/ft_lstadd_back.c bonus/ft_lstnew.c bonus/ft_putstr_fd.c bonus/ft_split.c \
              bonus/get_next_line.c bonus/check_result.c bonus/get_next_line_utils.c bonus/is_empty.c \
              bonus/pswp_oprs_swp.c bonus/pswp_oprs_push.c bonus/pswp_oprs_rot.c
BNS_OBJS    = $(BONUS:.c=.o)
BNS_NAME    = checker
BNS_HEADERS = checker.h

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

bonus: $(BNS_NAME)

$(BNS_NAME): $(BNS_OBJS)
	$(CC) $(CFLAGS) $(BNS_OBJS) -o $(BNS_NAME)

%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(BNS_OBJS)

fclean: clean
	rm -f $(NAME) $(BNS_NAME)

re: fclean all

.PHONY: all clean fclean re