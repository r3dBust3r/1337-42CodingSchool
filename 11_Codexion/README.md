*This project has been created as part of the 42 curriculum by ottalhao.*

# Codexion

Codexion is a multithreaded concurrency simulation inspired by the classic dining philosophers problem. In this project, each coder cycles through compile, debug, and refactor phases while competing for two shared dongles. A monitor thread observes the system and stops the simulation when a coder burns out or when every coder has completed the required number of compiles.

The project supports two scheduling strategies for dongle requests:

- FIFO: requests are served in the order they were created.
- EDF: requests are prioritized by the earliest deadline, based on each coder's burnout window.

## Instructions

### Build

```bash
make
```

The project builds with `cc` and `pthread` using the following flags:

```
-Wall -Wextra -Werror -pthread
```

### Clean

```bash
make clean
make fclean
make re
```

### Run

```bash
./codexion <coders> <burnout> <compile> <debug> <refactor> <compiles_req> <cooldown> <scheduler>
```

Example:

```bash
./codexion 5 800 200 200 200 3 50 fifo
```

Argument details:

| Argument | Meaning |
| --- | --- |
| `coders` | Number of coder threads and dongles |
| `burnout` | Maximum time in ms before a coder burns out if it does not compile again |
| `compile` | Time spent compiling in ms |
| `debug` | Time spent debugging in ms |
| `refactor` | Time spent refactoring in ms |
| `compiles_req` | Number of compiles each coder must complete before the simulation can end |
| `cooldown` | Time in ms a dongle remains unavailable after being released |
| `scheduler` | `fifo` or `edf` |

The parser accepts only positive decimal integers for the numeric parameters. The scheduler must be exactly `fifo` or `edf`.

## Description

Each coder owns two adjacent dongles in a circular topology. To compile, a coder must acquire two dongles, perform the compile phase, release them, then continue with debug and refactor. Even-numbered coders briefly delay their first attempt to reduce contention at startup.

The monitor thread keeps track of the simulation clock, each coder's last compile timestamp, and each coder's completed compile count. If a coder exceeds the burnout threshold before compiling again, the simulation stops immediately and the burnout event is printed once. If every coder reaches the required compile count, the monitor stops the simulation cleanly.

## Blocking Cases Handled

- Deadlock prevention is addressed by alternating the first dongle pickup order between odd and even coders.
- Starvation is reduced with a per-dongle request queue and a selectable scheduler policy.
- FIFO mode serves requests by creation time, while EDF mode serves the request with the earliest deadline.
- Dongle cooldown is enforced after release through an `available_at` timestamp, so a released dongle cannot be reused too early.
- Burnout detection is based on the most recent compile timestamp, not on the coder's current activity.
- Log output is serialized so that status lines do not interleave across threads.
- The single-coder case is handled explicitly so the simulation still behaves predictably when no second dongle is available.

## Thread Synchronization Mechanisms

Codexion uses standard POSIX threading primitives to coordinate shared state safely:

- `pthread_mutex_t` on each coder protects `last_compile` and `compiles_completed`.
- `pthread_mutex_t` on each dongle protects the availability flag, cooldown timestamp, and request queue.
- `pthread_cond_t` on each dongle wakes waiting coders when the dongle is released or its queue position changes.
- A global simulator mutex protects the `is_running` flag so the monitor and workers agree on when the simulation has ended.
- A dedicated print mutex serializes log messages and prevents mixed output from different threads.

The request flow is straightforward: a coder creates a request, pushes it into the dongle queue, and waits on the dongle condition variable until it is both available and at the head of the queue. When a coder releases a dongle, it marks the dongle as available, updates the cooldown deadline, and broadcasts to waiting threads so the next eligible coder can proceed.

This design prevents common race conditions around shared queues, status flags, and logging while still allowing the monitor to react quickly to burnout or completion.

## Resources

Classic references used for this project:

- [https://www.youtube.com/watch?v=d9s_d28yJq0&list=PLfqABt5AS4FmuQf70psXrsMLEDQXNkLq2](https://www.youtube.com/watch?v=d9s_d28yJq0&list=PLfqABt5AS4FmuQf70psXrsMLEDQXNkLq2)
- [https://www.youtube.com/watch?v=VSkvwzqo-Pk](https://www.youtube.com/watch?v=VSkvwzqo-Pk)
- [https://www.youtube.com/watch?v=XjlFoND00oY](https://www.youtube.com/watch?v=XjlFoND00oY)
- `man pthread_create`, `man pthread_join`, `man pthread_mutex_lock`, `man pthread_cond_wait`
- `man gettimeofday`
- The dining philosophers problem and standard deadlock-prevention patterns
- POSIX threads documentation and mutex/condition-variable usage guides

AI usage:

- GPT-5.4 mini was used to analyze the source tree, infer the runtime behavior, and draft this README.
- The code was inspected directly to verify the command-line interface, scheduler modes, synchronization model, and edge-case handling before the documentation was written.
