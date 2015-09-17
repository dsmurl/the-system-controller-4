FROM debian:jessie
MAINTAINER Rémy Greinhofer <remy.greinhofer@gmail.com>

# Create the directory containing the code.
RUN mkdir /code
WORKDIR /code

# Set the environment variables.
ENV PYTHONPATH $PYTHONPATH:/code

# Update the package list.
RUN apt-get update \

  # Install packages.
  && DEBIAN_FRONTEND=noninteractive apt-get install -yyq \
    build-essential \
    python \
    python-dev \
    python-pip \
    python-setuptools \
    python-smbus \

  # Clean up.
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy the requirements.txt file.
COPY requirements.txt /code/requirements.txt
COPY test-requirements.txt /code/test-requirements.txt

# Install the pip packages.
RUN pip install -q -r requirements.txt -r test-requirements.txt

# Expose the port.
EXPOSE 8888

# Start the application.
ENTRYPOINT ["python", "wsgi.py"]
