"""
Drew Dahlquist,
University of Missouri - Columbia,
College of Engineering,
Dept. of EECS

DMC Lab

2021
"""

import secrets

import subprocess


def main():

    # run command
    process = subprocess.run(
        ['duck', '-u', secrets.user, '--synchronize', secrets.r_dir, secrets.s_dir, ], input=b'upload')


if __name__ == '__main__':
    main()
