char *ft_strchr(const char *s, int c)
{
	int i = 0;
	while (s[i])
	{
		if (s[i] == c)
			return (s[i]);
		i++;
	}
	return (0);
}