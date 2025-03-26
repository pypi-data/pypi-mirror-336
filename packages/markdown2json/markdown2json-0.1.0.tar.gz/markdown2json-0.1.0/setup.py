from setuptools import setup, find_packages

setup(
    name="markdown2json",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Markdown==3.7",
        "beautifulsoup4==4.12.3",
        "anthropic==0.43.0",
        "openai==1.59.7",
        "ollama==0.4.7",
        "python-dotenv==1.0.1",
        "markdown-katex==202406.1035",
        "markdown-it-py==3.0.0",
    ],
    author="Vaghawan Ojha, Sadikshya Gyawali, Manish Dahal, Manish Awale, Ashwini Mandal",
    author_email="vaghawan.ojha@ekbana.net, sadikshya.gyawali@ekbana.info, manish.dahal@ekbana.info, manish.awale@ekbana.info, ashwini.mandal@ekbana.info",
    description="A Python package to convert markdown content to structured JSON",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ekbanasolutions/markdown2json",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
