# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/02/06 11:36:20 by ottalhao          #+#    #+#              #
#    Updated: 2026/02/06 11:57:57 by ottalhao         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

all: pipex

pipex:
	@cc -Wall -Wextra -Werror pipex.c -o pipex
	@echo "Building pipex"

bonus:
	@echo "bonus"
	@echo "Building pipex's bonus"

clean:
	@find . -type f -name "*.o" -print -exec rm -rf {} \;
	@echo "Cleaning object files"

fclean: clean
	@rm -rf pipex
	@echo "Cleaning pipex bin file"

re: fclean all

.PHONY: all bonus clean fclean re
