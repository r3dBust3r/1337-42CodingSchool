*This project has been created as part of the 42 curriculum by ottalhao*

# push_swap

## Description

### Goal

The goal of **push_swap** is to sort a list of unique integers in ascending order using two stacks (*a* and *b*) and a restricted set of operations, while generating the **minimum possible number of moves**.

### Overview

* Stack **a** is initialized with integers passed as arguments.
* Stack **b** starts empty.
* Only specific operations are allowed (`sa`, `sb`, `ss`, `pa`, `pb`, `ra`, `rb`, `rr`, `rra`, `rrb`, `rrr`).
* The program outputs the operations required to sort stack **a**.
* Efficiency matters. Fewer operations mean a better score.

### Operations
- `sa`: swap the 1st and the 2nd in stack a
- `sb`: swap the 1st and the 2nd in stack b
- `ss`: sa & sb
- `pa`: push the 1st from b to the top of stack a
- `pb`: push the 1st from a to the top of stack b
- `ra`: rotate stack a, the 1st becomes the last
- `rb`: rotate stack b, the 1st becomes the last
- `rr`: ra & rb
- `rra`: reverse rotate stack a, the last becomes the 1st
- `rrb`: reverse rotate stack b, the last becomes the 1st
- `rrr`: rra & rrb

This project emphasizes algorithm design, optimization, and careful memory management in C.

---

## Instructions

### Compilation

Compile the mandatory part:

```bash
make
```

Compile the bonus (`checker`):

```bash
make bonus
```

### Execution

Run `push_swap`:

```bash
./push_swap 3 2 1
```

Validate the result using the checker:

```bash
N=500
NUMS=$(shuf -i 0-10000 -n $N | tr '\n' ' ')
./push_swap $NUMS | ./checker $NUMS
```

Expected output:

* `OK` if stack `a` is sorted and stack `b` is empty
* `KO` otherwise

---

## Bonus

### Checker Program

The bonus part implements a **checker** that:

* Reads a list of integers from arguments
* Reads operations from standard input
* Executes each operation on the stacks
* Verifies whether stack `a` is sorted and stack `b` is empty

Invalid operations result in an `Error` message to the `STDERR`.

Example usage:

```bash
NUMS="89 20 10 0"
./push_swap $NUMS | ./checker $NUMS
```

This ensures correctness independently from the sorting algorithm.

---

## Resources

### Articles

* [push-swap-the-least-amount-of-moves-with-two-stacks](https://medium.com/@jamierobertdawson/push-swap-the-least-amount-of-moves-with-two-stacks-d1e76a71789a)

### Visualizers

* [push_swap_visualizer_1](https://windowdong11.github.io/push_swap_visualizer/)
* [push_swap_visualizer_2](https://codepen.io/ahkoh/full/bGWxmVz)

### Videos

* [Push Swap Explained](https://www.youtube.com/watch?v=mIqpsnKmfzw)

### AI

* ChatGPT
  Used for algorithm discussion & debugging.