# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='supercaptcha',
    version='0.1.6',
    packages=['supercaptcha'],
    package_data={
        '':['fonts/*.ttf']
    },
    install_requires=[
        'Pillow==5.1.0'
    ],
    author='Viktor Kotseruba',
    author_email='barbuzaster@gmail.com',
    description='captchafield for django newforms',
    license='MIT',
    keywords='forms web django',
)
