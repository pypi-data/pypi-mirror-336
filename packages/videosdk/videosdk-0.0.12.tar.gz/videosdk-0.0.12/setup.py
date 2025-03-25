import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="videosdk",
    version="0.0.12",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="videosdk",
    author_email="sdk@videosdk.live",
    license="MIT",
    packages=setuptools.find_packages(
        include=["videosdk*", "videosdk.worker.proto_gen*"], exclude=["example"]
    ),
    include_package_data=True,
)
