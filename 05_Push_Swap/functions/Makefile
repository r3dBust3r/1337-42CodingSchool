# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/01/03 14:50:37 by ottalhao          #+#    #+#              #
#    Updated: 2026/01/03 18:55:19 by ottalhao         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME        = push_swap
CC          = cc
# CFLAGS      = -Wall -Wextra -Werror
SRCS        = assign_indexes.c count_lst.c find_distance.c ft_atol.c ft_lstadd_back.c \
              ft_lstnew.c ft_number.c ft_putstr_fd.c ft_split.c is_empty.c \
              operations.c pswp_sort_3.c pswp_sort.c push_swap.c
OBJS        = $(SRCS:.c=.o)
HEADERS     = push_swap.h

all: $(NAME) clean
	@echo "[*] Push_swap has been compiled"

$(NAME): $(OBJS)
	@$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

%.o: %.c $(HEADERS)
	@$(CC) $(CFLAGS) -c $< -o $@

clean:
	@rm -f $(OBJS)
	@echo "[*] Cleaning..."

fclean: clean
	@rm -f $(NAME)
	@echo "[*] Full Cleaning..."

re: fclean all

.PHONY: all clean fclean re