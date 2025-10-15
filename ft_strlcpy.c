/*
	strlcpy copies a string (src) into a destination buffer (dst), making sure:
	The destination does not overflow.
	The destination string is always null-terminated (if size > 0).
	It’s safer than strcpy because you specify the maximum size of dst.
	---
	Parameters:
		dst: Destination buffer where the string will be copied.
		src: Source string to copy from.
		size: The total size of the destination buffer, including space for the '\0'.
	Returns:
		The length of src, not the number of characters actually copied.
 */

static int ft_strlen(char *str)
{
	int i = 0;
	while (str[i])
		i++;
	return (i);
}

int ft_strlcpy(char *dst, const char *src, size_t size)
{
	int dst_len = ft_strlen(dst);
	int src_len = ft_strlen(src);
	int i = 0;
	while (i < (size - dst_len))
	{
		dst[dst_len + i] = src[i];
		i++;
	}
	dst[i] = '\0';
	return (ft_strlen(src));
}
