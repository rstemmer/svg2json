
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

from svg2json.svg2json import VERSION

setuptools.setup(
        name            = "svg2json",
        version         = VERSION,
        author          = "Ralf Stemmer",
        author_email    = "ralf.stemmer@gmx.net",
        description     = "Collects a set of svg vector graphics into a single json file using data URIs",
        long_description= long_description,
        long_description_content_type   = "text/markdown",
        url             = "https://github.com/rstemmer/svg2json",
        project_urls    = {
                "Documentation": "https://github.com/rstemmer/svg2json",
                "Source":  "https://github.com/rstemmer/svg2json",
                "Tracker": "https://github.com/rstemmer/svg2json/issues",
            },
        packages        = setuptools.find_packages(),
        entry_points={
                "console_scripts": [
                    "svg2json=svg2json.svg2json:main",
                    ],
                },
        install_requires= ["scour"],
        python_requires = ">=3.8",
        keywords        = "json svg web-development",
        license         = "Apache Software License",
        classifiers     = [
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: POSIX :: Linux",
            "Environment :: Console",
            "Intended Audience :: End Users/Desktop",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "Topic :: Internet",
            "Topic :: Multimedia :: Graphics :: Graphics Conversion"
            "Topic :: Software Development :: Build Tools",
            "Topic :: Utilities",
            ],
            #"Development Status :: 5 - Production/Stable",
        )

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

