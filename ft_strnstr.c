/*
	Loop through each position i in haystack up to len.
	For each position, check if needle matches character by character.
	Stop checking when you hit end of needle, end of haystack, or reach len.
	If full needle matched, return pointer to start of match.
	Otherwise, return NULL if no match found.
 */

// char *strnstr(const char *haystack, const char *needle, size_t len);

static int check_current(char *big, char *little, int curr_index)
{
	int i = 0;
	while (little[i])
	{
		if (little[i] != big[i + curr_index])
			return (0);
		i++;
	}
	return (1);
}

char *strnstr(const char *big, const char *little, size_t len)
{
	if (! little[0])
		return ((char*)big);

	int i = 0;
	while (big[i] && i < len)
	{
		if (big[i] == little[0])
		{
			if (check_current((char*)big, (char*)little, i))
				return ((char*)&big[i]);
		}
		i++;
	}
	return (0);
}