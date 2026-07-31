NAME        = codexion
HEADER      = $(NAME).h
CC          = cc
CFLAGS      = -Wall -Wextra -Werror -pthread
RM          = rm -f

SRC_DIR     = src
SRC_FILES   = actions.c clean_up.c coder_cycle.c ft_atol.c \
              get_time.c grab_dongle.c help.c initializer.c \
              monitor.c ms_sleep.c parser.c print_action.c \
              priority_queue.c single_coder.c

SRCS        = $(addprefix $(SRC_DIR)/, $(SRC_FILES)) main.c
OBJS        = $(SRCS:.c=.o)

all: $(NAME)

$(NAME): $(OBJS)
	@$(CC) $(CFLAGS) $(OBJS) -o $(NAME)
	@echo "$(NAME) compiled successfully!"

%.o: %.c $(HEADER)
	@$(CC) $(CFLAGS) -I. -c $< -o $@

clean:
	@$(RM) $(OBJS)
	@echo "object files cleaned!"

fclean: clean
	@$(RM) $(NAME)
	@echo "executable cleaned"

re: fclean all

.PHONY: all clean fclean re
