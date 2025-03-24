from setuptools import setup, find_packages

setup(
    name='tsp_solver_Tasnim',
    version='0.1.0',
    packages=find_packages(include=["tsp_solver_Tasnim", "tsp_solver_Tasnim.*"]),
    description='A simple TSP solver library with multiple optimization algorithms.',
    author='Masrura Tasnim',
    author_email='your_email@example.com',
    url='https://github.com/mastas09/tsp_solver_Tasnim',
    license='MIT',
    install_requires=[],
    python_requires='>=3.6',
)
