
import invoke

# Based on https://github.com/pyca/cryptography/blob/master/tasks.py


@invoke.task
def release(version):
    invoke.run("git tag -a pythonz-{0} -m \"pythonz {0} release\"".format(version))
    invoke.run("git push --tags")

