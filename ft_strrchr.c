static int ft_strlen(char *str)
{
    int i = 0;
    while (str[i])
        i++;
    return (i);
}

char *ft_strrchr(const char *s, int c)
{
	int i = 0;
	char *ptr = NULL;

	while (s[i])
	{
		if (s[i] == c)
			ptr = (char*)&s[i];
		i++;
	}
	return (ptr);
}