clapps - Command Line App Skeleton [WIP]
========================================

Hallo Luki!

Python CLI scripts have been extremely useful to me in the past, both at home
and for work. However, whether a one-off helper script or a periodically
running job on a server, rarely did my Python scripts receive the appreciation
they would have deserved.
CLI scripts usually handle mundane, repetitive tasks. Dull a matters, as long
as the code does what is expected, anyway.

Python's standard library comes with a vast set of tools to write proper
command line applications. Most are quite fun to use and offer neat, painless
interfaces. Still, depending on the size of the business logic, a well-written
CLI app might very well be three quarters boilerplate and a measely 25% core
logic.

I have long lost count of the times I have opened a new file and begun writing:

```{.py}
#!/usr/bin/env python3

from argparse import ArgumentParser, parse_args

def run():
    parser = ArgumentParser()
    parser.add_argument(*args, **kwargs)  # repeat n-times
    args = parse_args()

    # some logic here

if __name__ = "__main__":
    run()
```

Once one's done the above a couple of times, it can be done hacked together
fairly quickly, but the approach is (a) error prone and (b) anything but DRY.

If the main function grows, the following step would be moving the adding of
arguments into its own enclosing function. Thereafter? Depends.
Is it worth it to add logging or just `print` some information
to whereever and be done with it? Maybe.
Does the script need to handle writing to an out- or logfile? Or is it the
caller's responsibility to employ shell helpers the likes of [`tee`][tee] to
capture output? Likely the latter.
Unit-testing the boilerplate? Please.
Packaging an app, rather than invoking the script with the interpreter?
Come on now.

`clapps` is an attempt at reducing the boilerplate I need for a quality command
line app / making the boilerplate re-usable.

[tee]: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/tee.html
