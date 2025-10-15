void *ft_memcpy(void *dest, const void *src, size_t n)
{
	size_t i = 0;
	unsigned char *d = (unsigned char *)dest;
	const unsigned char *s = (const unsigned char *)src;
	while (i < n)
		d[i] = s[i++];
	return (dest);
}
