NAME        = codexion
HEADER      = $(NAME).h
CC          = cc
CFLAGS      = -Wall -Wextra -Werror
RM          = rm -f

SRCS        = parser.c ft_atol.c print_usage.c clean.c main.c
OBJS        = $(SRCS:.c=.o)

all: $(NAME)

$(NAME): $(OBJS)
	@$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

%.o: %.c $(HEADER)
	@$(CC) $(CFLAGS) -I. -c $< -o $@

clean:
	@$(RM) $(OBJS)

fclean: clean
	@$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re
