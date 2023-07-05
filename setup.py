import pytest


def run_install():
    retcode = pytest.main(['-v', 'install/test_install.py'])

    if retcode == 0:
        print('Install tests passed')

if __name__ == '__main__':
    run_install()

