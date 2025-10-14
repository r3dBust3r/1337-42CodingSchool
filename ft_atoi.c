int ft_atoi(const char *nptr)
{
    int s = 1;
    int r = 0;
    int i = 0;
    while (nptr[i] == '-' || nptr[i] == '+')
    {
        if (nptr[i] == '-')
            s = -s;
        i++;
    }
    while (nptr[i])
        r = r * 10 + (nptr[i++] - '0');
    return (r * s);
}