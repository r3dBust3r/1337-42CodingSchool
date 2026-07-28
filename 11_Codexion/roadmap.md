# Codexion — Roadmap & Checklist

## 0. Translate the subject into "Dining Philosophers" language

| Codexion | Classic Dining Philosophers |
|---|---|
| Coder | Philosopher |
| Dongle | Fork |
| Compiling | Eating |
| Debugging + Refactoring | Thinking |
| Burnout | Starving to death |
| Quantum Compiler (center) | The table |

If you already understand the classic problem, 70% of the mental model transfers directly. But **don't relax** — Codexion bolts on four things the classic problem doesn't have, and each one is a real design decision:

1. **Dongle cooldown** — a released dongle isn't immediately available again.
2. **A pluggable scheduler** (`fifo` or `edf`) — arbitration isn't "whoever grabs it first," it's a policy you must enforce and prove.
3. **A mandatory hand-rolled priority queue (heap)** — you can't fake this with a sorted array and call it done; it has to be a real heap, and it has to serve both scheduling modes.
4. **10ms burnout-detection precision** — a monitor thread with a real deadline, not "check occasionally."

Everything below is built around those four additions, since the core eat/think loop is the part you likely already know how to reason about from the philosophers problem.

---

## Phase 1 — Design on paper (before you open an editor)

- [ ] Draw the ring for `n = 1`, `n = 2`, and `n = 5` coders by hand. Label which dongle is "left" and "right" for each coder number.
- [ ] Write the per-coder state diagram: `waiting for dongles → compiling → debugging → refactoring → (back to waiting)`.
- [ ] Decide **who decides who gets a dongle**. This is the one architectural fork-in-the-road (pun intended) of the whole project. Two honest options:
  - **Per-dongle queues**: each dongle has its own waiting list; a coder tries to reserve left, then right (or vice versa) — this is the *classic* approach, and it's exactly what causes deadlock in the original problem (everyone holds their left fork, waits forever for the right).
  - **Central broker**: one thread-safe component owns all dongle state, and a coder makes a single request for "the pair I need." The broker only ever grants *both* dongles together or *neither*. This sidesteps hold-and-wait entirely (one of Coffman's four deadlock conditions), so you don't need the usual trick of "always pick up the lower-numbered fork first."
  
  Given that you also need one *global* scheduling policy (fifo/edf) across potentially-competing requests, the broker model is usually far easier to reason about and to prove correct — but it's your call, and you should be able to defend whichever you pick in your defense. **Which one are you leaning toward, and why?**
- [ ] Sketch your structs on paper: `t_coder`, `t_dongle`, `t_request` (or whatever you call the "I want to compile" ticket), `t_heap`, and one `t_sim` context struct that holds everything and gets passed as `void *arg` to every thread (remember: **no global variables**).
- [ ] Decide how you'll compute a coder's deadline: `deadline = last_compile_start + time_to_burnout`. Decide what "last_compile_start" means at t=0, before anyone has compiled yet.
- [ ] Decide your EDF tie-breaker (the subject explicitly requires one, even though it'll rarely trigger). Simplest options: arrival sequence number, or coder ID.

---

## Phase 2 — Skeleton, parsing, Makefile

- [ ] Parse and validate all 8 arguments: `number_of_coders time_to_burnout time_to_compile time_to_debug time_to_refactor required_compiles dongle_cooldown scheduler`.
- [ ] Reject: negative numbers, non-integer strings, `number_of_coders == 0`, and any `scheduler` value that isn't exactly `fifo` or `edf`.
- [ ] Write the Makefile: `NAME`, `all`, `clean`, `fclean`, `re`, flags `-Wall -Wextra -Werror -pthread`, no unnecessary relinking.
- [ ] Build your `t_sim` context struct and confirm you can allocate/free it cleanly with zero coders touched yet.

---

## Phase 3 — Threads with no dongle logic yet

- [ ] Spawn `number_of_coders` threads. Each thread just logs a fake lifecycle (sleep a bit, print "would compile") — no real synchronization yet. This proves your thread plumbing, argument-passing, and join logic work before concurrency bugs get layered on top.
- [ ] Spawn the monitor thread and wire up a shared "stop simulation" flag (mutex-protected) that all coder threads check and that causes clean `pthread_join` on exit.
- [ ] Confirm `pthread_join` on all threads happens exactly once, no leaked thread handles.

---

## Phase 4 — The hand-rolled heap (build and test in isolation)

- [ ] Implement a generic min-heap: `push`, `pop`, `peek`, with a comparator function pointer so the *same* heap code can order by arrival time (fifo) or by deadline (edf).
- [ ] Write a tiny standalone test (separate `main`, not wired into the simulation yet) that pushes a batch of fake requests and confirms `pop` returns them in the right order for both comparators, including your tie-breaker case.
- [ ] Only move on once this passes on its own — debugging heap-ordering bugs *while* also debugging thread races is miserable.

---

## Phase 5 — Dongle acquisition / arbitration

- [ ] Implement the mutex + condition-variable logic for however you resolved Phase 1's design question: a coder posts a request, waits on a cond var, and is only woken once granted.
- [ ] Handle the pair-acquisition atomically — no state where a coder holds exactly one dongle.
- [ ] Handle cooldown: after release, a dongle isn't eligible for granting until `dongle_cooldown` ms pass. You'll likely need `pthread_cond_timedwait` so the broker can wake itself up when a cooldown expires, even with no new requests arriving.
- [ ] **Test with `n = 2` first.** It's the smallest case where two coders genuinely compete for the same dongle, and it's small enough to reason about by hand.
- [ ] Then test `n = 5`, `n = 10` before going bigger.

---

## Phase 6 — Full state machine + compile counting

- [ ] Wire compiling → debugging → refactoring → immediately re-request dongles.
- [ ] Track `num_compiles` per coder; stop the simulation once *every* coder has reached `required_compiles`.
- [ ] Confirm the two stop conditions (burnout vs. compiles-required) don't race each other — e.g. don't let a burnout log and a "simulation complete, clean exit" both try to fire.

---

## Phase 7 — Monitor thread precision (the 10ms requirement)

- [ ] Compute exact deadlines per coder and have the monitor check them at a granularity tight enough to guarantee detection within 10ms (a short, repeated sleep-and-check loop is the simplest correct approach here — don't overthink it into something exotic).
- [ ] Deliberately test with a very small `time_to_burnout` and a coder that will never get dongles (e.g. `n = 1`) to force a burnout, and time how long after the real deadline your log line appears.
- [ ] Confirm burnout stops *all* threads promptly and cleanly (no orphaned threads, no use-after-free on shared state).

---

## Phase 8 — Logging

- [ ] One `log_action()` function, one mutex, exact format: `timestamp_in_ms X <action>`.
- [ ] Confirm two coders logging at "the same time" never interleave mid-line.
- [ ] Confirm `X has taken a dongle` is logged **twice** before `X is compiling` (once per dongle), matching the example in the subject.

---

## Phase 9 — Edge cases & stress tests

- [ ] `n = 1`: only one dongle exists, compiling needs two — this coder can *never* compile and should burn out cleanly and predictably. Make sure your program doesn't hang or crash here; it's an intentional edge case they will test.
- [ ] Very large `n` (stress test for races) — run repeatedly, not just once; race conditions are probabilistic.
- [ ] `valgrind --leak-check=full` — zero leaks (this is a local dev tool, not something you submit).
- [ ] Norm check on every file, mandatory and bonus.
- [ ] Confirm `edf` mode never starves anyone over a long run with feasible parameters (this is the "guarantee liveness" requirement).
- [ ] Confirm `fifo` mode grants strictly in arrival order under contention.
- [ ] Feed it garbage args (negative numbers, `abc`, `xyz` as scheduler) and confirm clean rejection, not a crash.

---

## Phase 10 — README.md

- [ ] First line, italicized: `*This project has been created as part of the 42 curriculum by <login>.*`
- [ ] `Description` section.
- [ ] `Instructions` section (build/run).
- [ ] `Resources` section — references you used **and** an honest account of where/how you used AI (per the subject's AI Instructions chapter — be specific about which tasks, not a blanket statement).
- [ ] `Blocking cases handled` section — deadlock prevention (name which Coffman condition your design breaks and how), starvation prevention, cooldown handling, precise burnout detection, log serialization.
- [ ] `Thread synchronization mechanisms` section — which mutexes/cond vars protect what, with a concrete example of a race you prevented.
- [ ] Written in English.

---

## Phase 11 — Defense prep

- [ ] Be able to explain, out loud, why your design can't deadlock — in terms of Coffman's four conditions, not just "it works."
- [ ] Prepare test cases you can run live, including the `n = 1` burnout and a fifo-vs-edf ordering demo.
- [ ] Be ready for a "recode" request: a small live modification (e.g., add a field to a log line, change a data structure) — know your own code well enough to do this in a few minutes without re-reading everything.

---

**Where to start today:** Phase 1's design question — per-dongle queues vs. central broker — is the decision that shapes every phase after it. Want to think through the tradeoffs together before you write any structs?
