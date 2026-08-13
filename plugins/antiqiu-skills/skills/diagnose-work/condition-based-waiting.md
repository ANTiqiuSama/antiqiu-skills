# Condition-based waiting

Use this reference when a test or asynchronous workflow sleeps for a guessed duration before checking observable state. Prefer a framework-native event, promise, callback, or waiter; poll only when no direct signal is available.

## Replace the guess with the condition

```text
before: trigger work -> sleep N ms -> assert state
after:  trigger work -> wait until required state or timeout -> assert state
```

A useful waiter must:

- read fresh state on every check;
- name the condition in its timeout error;
- have a finite timeout based on the operation's real budget;
- use a polling interval appropriate to the system rather than a universal magic number;
- return the matched value when possible so the caller does not race by reading again.

Example pseudocode:

```text
deadline = now + timeout
loop:
  value = observe()
  if predicate(value): return value
  if now >= deadline: fail with condition and last observed value
  wait for the next event or a bounded polling interval
```

Keep a fixed delay when elapsed time is itself the behavior under test, such as debounce, backoff, or lease expiry. In that case derive the delay from the documented timing contract and explain the tolerance.

Verify the replacement by running the focused test repeatedly or under the concurrency condition that exposed the flake. Do not claim the flake is fixed from one passing run when recurrence evidence is cheap to obtain.
