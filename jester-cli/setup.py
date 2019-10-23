from distutils.core import setup
setup(name='jester-cli',
      version='0.0.1',
      entry_points={
          'console_scripts': [
              'jester = cli:launch',
              ],
          },
)
