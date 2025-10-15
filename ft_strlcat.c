static int ft_strlen(char *str)
{
	int i = 0;
	while (str[i])
		i++;
	return (i);
}
/*
	It appends src to the end of dst.
	It appends at most (size - strlen(dst) - 1) chars. that means (size) is the total buffer of (dst) 
	It guarantees the result is null-terminated if size > 0.
	It returns the total length it tried to create: strlen(dst) + strlen(src).
*/
int ft_strlcat(char *dst, const char *src, size_t size)
{
	int dst_len = ft_strlen(dst);
	int src_len = ft_strlen(src);
	int i = 0;
	while (i < (size - dst_len - 1))
	{
		dst[dst_len + i] = src[i];
		i++;
	}
	dst[i] = '\0';
	return (src_len + dst_len);
}