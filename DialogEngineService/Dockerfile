FROM rasa/rasa:latest

# To install system dependencies
RUN apt-get update -qq && \
#    apt-get install -y <NAME_OF_REQUIRED_PACKAGE> && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# To install packages from PyPI
# RUN pip install --no-cache-dir <A_REQUIRED_PACKAGE_ON_PYPI>

ENTRYPOINT stack exec duckling-example-exe