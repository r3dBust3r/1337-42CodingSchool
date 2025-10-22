static int ft_strlen(char *str)
{
	int i = 0;
	while (str[i])
		i++;
	return (i);
}

void *ft_memmove(void *dest, const void *src, size_t n)
{
	size_t i = 0;
	unsigned char *d = (unsigned char *)dest;
	const unsigned char *s = (const unsigned char *)src;

	if (n == 0)
		return (dest);

	if ((const unsigned int *)src + n >= (unsigned int *)dest)
	{
		while (i < n)
			d[i] = s[i++];
	}
	else
	{
		while (i < n)
		{
			d[i] = s[ft_strlen(s) - 1 - i];
			i++;
		}
	}

	return (dest);
}
