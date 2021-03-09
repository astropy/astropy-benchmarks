#!/bin/bash -xe

MACHINE=`python -c "from asv.machine import Machine; print(Machine.load('~/.asv-machine.json').machine)"`

echo "asv: "`asv --version`
echo "Machine: "$MACHINE

git clean -fxd
git checkout main
git pull origin main

# We now run all benchmarks since the last one run in this benchmarks repository. This assumes
# you have previously run at least ``asv run HEAD^!`` and added the results to the repository
# otherwise running ``asv run NEW`` will run all benchmarks since the start of the project.
# We add || true to make sure that if no commits are run (because there aren't any) things don't
# fail. But asv should have a way to return a zero status code in that case, so we should fix
# that in future. The timeout command is used to make sure that the command finishes before
# the next cron job - the timeout value is in seconds and can be adjusted.

# On Linux - using taskset -c 0 ensures that the same core is always used when running the benchmarks.
taskset -c 0 asv run NEW || true
timeout 7200 taskset -c 0 asv run ALL --skip-existing-commits || true

# On MacOSX:
# asv run NEW || true
# timeout 7200 asv run ALL --steps 10 --skip-existing-commits || true

git add results/$MACHINE
git commit -m "New results from $MACHINE"

git push origin main
asv gh-pages --no-push
git push -f origin gh-pages

