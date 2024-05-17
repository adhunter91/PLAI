from setuptools import setup, find_packages

setup(
    name='PLAI_webapp',
    version='0.1',
    author='Alexander Hunter',
    author_email='alexander.hunter@berkeley.edu',
    description='Webapp to help kids get kindergarten ready',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/adhunter91/PLAI',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Authlib==1.3.0',
        'Faker==25.0.0',
        'Flask==3.0.2',
        'Django==5.0.3',
        'configparser==6.0.1',
        'openai==1.30.1',
        'pandas==2.2.0',
        'pip==23.2.1',
        'psycopg2-binary==2.9.9',
        'pycparser==2.22',
        'python-dotenv==1.0.1',
        'requests==2.31.0',
        'simpletexting==0.0.1',
        'sqlparse==0.4.4',
        'supabase==2.4.3',
        'urllib3==2.2.0',
        'webflow==1.2.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',  # Development status
        'Programming Language :: Python :: 3.10',  # Python 3.10
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)