### Endianness
Humans naturally write numbers in **big endian** format. `n = 512`
The most significant digit is **5**, which represents **500**, so we read it from **big to little**:

```
500 + 10 + 2
```

If humans used **little endian**, we would write the same number as **215**, interpreting it from **little to big**:

```
2 + 10 + 500
```

##### Example with a Hex Number
```
n = 0x32F643C0
0x32F643C0 (hex) = 855000000 (decimal)
```

How this number is stored in memory depends on the system’s endianness:

**Big Endian**
```
+----+----+----+----+
| 32 | F6 | 43 | C0 |
+----+----+----+----+
```

**Little Endian**
```
+----+----+----+----+
| C0 | 43 | F6 | 32 |
+----+----+----+----+
```

It’s important to know the endianness so you can interpret memory values correctly. For example:

```
+----+----+
| aa | bb |
+----+----+
```

* In **big endian**, this represents `0xAABB`.
* In **little endian**, it represents `0xBBAA`.

##### Network Standards
According to the Internet standard (RFC 793), **all fields in network headers** must use **big endian** byte order.
If a computer uses **little endian** internally, it must **convert** network data to little endian before interpreting it.

##### NOTES
1. **Endianness** refers to **byte order**, not bit order.
2. It only applies to **multi-byte data types**.
   * For example, the string `"james"` is not reversed because each character is a single byte.

Examples:

```
INVALID: "james"    -> "semaj"
INVALID: 0x89       -> 0x98
VALID:   0x11223344 -> 0x44332211
```

##### Checking Endianness on Linux
We can check our system’s byte order with:

```bash
lscpu | grep "Byte Order"
```

##### Example Program

Let’s take a look at a simple example:
```bash
echo "int n = 0x10203040;" > var.c
gcc -c var.c
readelf -x .data var.o
```

The output will show how the number `0x10203040` is actually stored in memory, revealing our system’s endianness.