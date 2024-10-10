# Use the official Ubuntu base image
FROM ubuntu:16.04

# Set environment variables to prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Update the package list and install dependencies for Python
RUN apt-get update && \
    apt-get install -y \
    wget \
    build-essential \
    libssl-dev \
    libffi-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    tk-dev \
    liblzma-dev \
    libsqlite3-dev \
    lzma \
    ca-certificates \
    curl \
    git

# Download and install Python 2.7.12 from source
RUN wget https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tgz && \
    tar xzf Python-2.7.12.tgz && \
    cd Python-2.7.12 && \
    ./configure --enable-optimizations && \
    make altinstall && \
    cd .. && \
    rm -rf Python-2.7.12 Python-2.7.12.tgz

# Install pip version 19.3.1
RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py && \
    python2.7 get-pip.py pip==19.3.1 && \
    rm get-pip.py

# Install the required Python packages
RUN pip2.7 install \
    inspyred==1.0 \
    matplotlib==1.3.1 \
    networkx==1.8.1 \
    numpy==1.8.0 \
    pytest==4.6.2 \
    scipy==0.13.2 \
    simpy==2.3.1

# Copy the local directory content into the container
COPY ./reproduction ./

# Open the container with a bash shell
CMD ["/bin/bash"]