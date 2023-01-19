# Specify the base image for the environment
FROM ubuntu:20.04

# Specify the authors of the image
LABEL authors="lnuernberg@bwh.harvard.edu,dbontempi@bwh.harvard.edu"

# Remove any third-party apt sources to avoid issues with expiring keys.
RUN rm -f /etc/apt/sources.list.d/*.list

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Amsterdam
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install some basic system utilities
RUN apt update && apt install -y --no-install-recommends \  
  wget \
  sudo \
  git \
  python3 \
  python3-pip \
  plastimatch \
&& rm -rf /var/lib/apt/lists/*

# Create a working directory
RUN mkdir /app
WORKDIR /app

# Install general utilities (specify version if necessary)
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir \
  albumentations \
  h5py \
  nibabel \ 
  numpy \
  opencv-python \
  pandas \ 
  Pillow \
  pydicom \
  PyYAML \
  pyplastimatch \
  scikit-image \
  scikit-learn \
  scipy \
  SimpleITK

# FIXME: make sure the execution of the next commands is not cached
# (while what comes before can be cached)
ARG CACHEBUST=6

# Clone git repositories
ENV aimi_branch="thresholder"
RUN git config --global http.sslVerify false 
RUN git clone -b $aimi_branch https://github.com/AIM-Harvard/aimi_alpha.git /app/

# Create useful aliases
RUN echo 'alias ll="ls -alF"' >> ~/.bashrc

# Create directories that will be used as mounting points
RUN mkdir /app/data /app/data/input_data /app/data/output_data 

# Set PYTHONPATH to the /app folder
ENV PYTHONPATH="/app"

# FIXME: separate this in base image + specific image
RUN apt update && apt install -y ffmpeg libsm6 libxext6 xvfb

# FIXME: set this environment variable as a shortcut to avoid nnunet crashing everything
ENV SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True

# Install nnunet and platipy
RUN pip3 install --no-cache-dir TotalSegmentator 

# FIXME: pass it as a command to the container in Slicer
CMD ["python3", "/app/aimi/totalsegmentator/scripts/slicer_run.py"]
