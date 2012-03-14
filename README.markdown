# Hacking ACIDity

## Environment Setup

1. Checkout the code
1. Install the packages in `pkgs/list` in your distro. The list is for Debian. Ubuntu should work but if it breaks, please fix it and update this file. If you are on a Mac, please figure out how do this and update this file.
1. Setup a virtualenv for you to work in
<pre>
$ virtualenv ~/envs/proto
</pre>
1. Install all the packages you need
<pre>
$ source ~/envs/proto/bin/activate
$ cd ~/src/ACIDity/pkgs
$ pip install --no-deps *.{tar.gz,zip}
</pre>
1. Set `PYTHONPATH` in your env
<pre>
$ export PYTHONPATH=$PYTHONPATH:~/src/ACIDity
</pre>

## Project setup

1. Create and init the DB
<pre>
$ source ~/envs/proto/bin/activate
$ python bin/coredb.py init     # Fix this so it actually works
</pre>
1. Run your shiny testcases with code coverage
</pre>
$ cd tests
$ py.test --cov=..
</pre>

## World domination

1. Implement everything
1. Test everything
1. `$ ack-grep FIXME *`
1. Profit
