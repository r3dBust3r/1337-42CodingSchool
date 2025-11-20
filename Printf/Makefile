# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/20 21:08:51 by ottalhao          #+#    #+#              #
#    Updated: 2025/11/20 21:43:48 by ottalhao         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

CC       = cc
FLAGS    = -Wall -Wextra -Werror
LIB_NAME = libftprintf.a
HEADER   = libftprintf.h
SRCS     = ft_printf.c \
           ft_putchar.c \
           ft_putnbr.c \
           ft_putstr.c \
           ft_put_addr.c \
           ft_put_hex.c \
           ft_putnbr_uns.c
OBJS     = $(SRCS:.c=.o)

all: $(LIB_NAME)

$(LIB_NAME): $(OBJS)
	@ar rcs $(LIB_NAME) $(OBJS)
	@echo "[  OK  ] $(LIB_NAME) has been created/updated!"

%.o:%.c $(HEADER)
	@$(CC) $(FLAGS) -c $< -o $@

clean:
	@rm -f $(OBJS)
	@echo "[  OK  ] the working space has been cleaned!"

fclean: clean
	@rm -f $(LIB_NAME)

re: fclean all

.PHONY: all clean fclean re
