from setuptools import setup

setup(
    name="Varial",
    version="0.2dev",
    author="Heiner Tholen",
    author_email="heiner.tholen@cern.ch",
    packages=["varial", "varial_example"],
    requires=['pyopenssl', 'cherrypy'],
    license="LICENSE.txt",
    description="Assist and manage an analysis with the CMS experiment.",
    long_description=open('README.rst').read(),
    test_suite="varial.test.test_main.suite"
)
