A **memory leak** happens when a program allocates memory (like with `malloc`) but never frees it (`free`).

In short:

* You **ask** the system for memory.
* You **forget** to give it back.
* The system just keeps losing chunks of memory until it slows down or crashes.

It’s like borrowing books from a library and never returning them, eventually, nobody else gets to read anything.
