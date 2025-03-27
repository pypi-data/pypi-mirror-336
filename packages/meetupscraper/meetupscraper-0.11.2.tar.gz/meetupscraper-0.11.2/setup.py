'''A web scraper for meetup.com.

Allows you to access events tied to a specific meetup group in a structured
way.'''

from setuptools import setup

setup(
    name='meetupscraper',
    version='0.11.2',
    description='A web scraper for meetup.com',
    long_description='Allows you to access events tied to a specific meetup group in a structured way',
    url='http://github.com/hakierspejs/meetupscraper',
    author='Hakiespejs Łódź',
    author_email='d33tah@gmail.com',
    license='WTFPL',
    packages=['meetupscraper'],
    install_requires=[
        'requests',
        'lxml',
        'python-dateutil',
        'icalendar',
    ]
)
