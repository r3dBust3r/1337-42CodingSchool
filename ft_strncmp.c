int ft_strncmp(const char *s1, const char *s2, size_t n)
{
	int i = 0;
	if (n == 0)
	{
		return (0);
	}
	while ((s1[i] && s2[i]) || i < n)
	{
		if (s1[i] != s2[i])
			break;
		i++;
	}
	return s1[i] - s2[i];
}
