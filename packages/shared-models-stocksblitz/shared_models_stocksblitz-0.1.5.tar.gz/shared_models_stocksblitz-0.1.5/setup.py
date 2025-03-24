from setuptools import setup, find_packages

setup(
    name="shared_models_stocksblitz",
    version="0.1.5",
    packages=find_packages(),  # Automatically finds all submodules like `models`
    install_requires=["sqlalchemy", "psycopg2"],
    include_package_data=True,  # Include non-code files if present
)
