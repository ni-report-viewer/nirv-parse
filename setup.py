from setuptools import setup
import os.path as op
import glob


opts = dict(
    use_scm_version={"root": ".", "relative_to": __file__},
    scripts=[op.join('bin', op.split(f)[-1]) for f in glob.glob('bin/*')])


if __name__ == '__main__':
    setup(**opts)
