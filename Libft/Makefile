# Compiler and flags
COMPILER    = cc
FLAGS       = -Wall -Wextra -Werror

# Library name
LIB_NAME    = libft.a

# Headers
HEADERS     = libft.h

# Source files
MAIN_SRCS   = ft_isalpha.c ft_isdigit.c ft_isalnum.c ft_isascii.c ft_isprint.c \
              ft_strlen.c ft_memset.c ft_bzero.c ft_memcpy.c ft_memmove.c \
              ft_strlcpy.c ft_strlcat.c ft_toupper.c ft_tolower.c ft_strchr.c \
              ft_strrchr.c ft_strncmp.c ft_memchr.c ft_memcmp.c ft_strnstr.c \
              ft_atoi.c ft_calloc.c ft_strdup.c ft_substr.c ft_strjoin.c \
              ft_strtrim.c ft_split.c ft_itoa.c ft_strmapi.c ft_striteri.c \
              ft_putchar_fd.c ft_putstr_fd.c ft_putendl_fd.c ft_putnbr_fd.c

BNS_SRCS    = ft_lstnew_bonus.c ft_lstadd_front_bonus.c ft_lstsize_bonus.c \
              ft_lstlast_bonus.c ft_lstadd_back_bonus.c ft_lstdelone_bonus.c \
              ft_lstclear_bonus.c ft_lstiter_bonus.c ft_lstmap_bonus.c

# Object files
MAIN_OBJS   = $(MAIN_SRCS:.c=.o)
BNS_OBJS    = $(BNS_SRCS:.c=.o)

# Default target
all: $(LIB_NAME)

# Rule to build the library \
[r]	Replace existing or insert new file(s) into the archive \
[c]	Do not warn if the library had to be created \
[s]	Create an archive index (cf. ranlib)
$(LIB_NAME): $(MAIN_OBJS)
	ar rcs $(LIB_NAME) $(MAIN_OBJS)

# Rule for bonus part
bonus: $(MAIN_OBJS) $(BNS_OBJS)
	ar rcs $(LIB_NAME) $(MAIN_OBJS) $(BNS_OBJS)

# Compile .c to .o \
For any file that ends in .o, here’s how to make it: \
it depends on a .c file with the same name, plus the header(s). \
[-c] Tells the compiler: “Compile only — don’t link.” \
That’s how you generate an object file (.o) from a source file. \
[$<] This is an automatic variable meaning: \
“the first prerequisite” \
—in this case, the .c file. \
So for ft_strlen.o, $< = ft_strlen.c. \
[-o $@] This tells the compiler where to put the output. \
$@ means: \
“the target file name” \
—in this case, the .o file being built. \
So for ft_strlen.o, $@ = ft_strlen.o.
%.o:%.c $(HEADERS)
	$(COMPILER) $(FLAGS) -c $< -o $@

# Remove object files
clean:
	rm -f $(MAIN_OBJS) $(BNS_OBJS)

# Remove objects and library
fclean: clean
	rm -f $(LIB_NAME)

# Rebuild everything
re: fclean all

.PHONY: all bonus clean fclean re
