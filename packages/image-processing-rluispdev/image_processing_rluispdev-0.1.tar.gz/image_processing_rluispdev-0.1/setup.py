from setuptools import setup, find_packages

# Lê o conteúdo do README.md
with open('README.md', 'r', encoding='utf-8') as f:
    page_description = f.read()

# Lê as dependências do requirements.txt
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name="image-processing-rluispdev",
    version="0.1",
    author="rluispdev",
    description="Image Processing Package Using Skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",  # Especifica que o README.md é Markdown
    url="https://github.com/rluispdev/image-processing-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.6',
)