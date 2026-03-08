# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/02/06 11:36:20 by ottalhao          #+#    #+#              #
#    Updated: 2026/03/08 07:41:13 by ottalhao         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME     = pipex
CC       = cc
CFLAGS   = -Wall -Wextra -Werror
SRCS     = pipex.c utils.c ft_split.c ft_strncmp.c ft_strjoin.c
OBJS     = $(SRCS:.c=.o)

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
