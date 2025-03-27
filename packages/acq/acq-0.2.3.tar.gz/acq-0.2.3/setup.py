import os
import acq
import setuptools

# setup.cfg is a new-ish standard, so we need to check this for now
if int(setuptools.__version__.split('.', 1)[0]) < 38:
    raise EnvironmentError(
        'Please upgrade setuptools. This package uses setup.cfg, which requires '
        'setuptools version 38 or higher. If you use pip, for instance, you can '
        'upgrade easily with ` pip install -U setuptools `'
    )

README_FILENAME = os.path.join(os.path.dirname(__file__), 'README.md')

with open('README.md', 'r') as readme:
    setuptools.setup(
        description=acq.short_description(),
        long_description=readme.read(),
        long_description_content_type='text/markdown',
        name=acq.name(),
        version=acq.version_string(),
    )
