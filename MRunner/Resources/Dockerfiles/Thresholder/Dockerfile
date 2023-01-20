# Specify the base image for the environment
FROM ubuntu:20.04

# Specify the authors of the image
LABEL authors="lnuernberg@bwh.harvard.edu,dbontempi@bwh.harvard.edu"

# Remove any third-party apt sources to avoid issues with expiring keys.
RUN rm -f /etc/apt/sources.list.d/*.list

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Amsterdam
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install basic system utilities and useful packages 
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

# Clone git repositories
RUN git config --global http.sslVerify false 
RUN git clone https://github.com/AIM-Harvard/mhub.git /app/
RUN git clone https://github.com/pieper/dicomsort.git /app/dicomsort

# Make dicomsort callable
RUN printf "python3 /app/dicomsort/dicomsort.py \"$@\"\n" > /usr/bin/dicomsort
RUN sudo chmod +x /usr/bin/dicomsort

# Install DCMQI
ENV DCMQI_RELEASE_URL="https://github.com/QIICR/dcmqi/releases/download/v1.2.4/dcmqi-1.2.4-linux.tar.gz"
ENV DCMQI_DOWNLOAD_PATH="/app/dcmqi-1.2.4-linux.tar.gz"
ENV DCMQI_PATH="/app/dcmqi-1.2.4-linux"

RUN wget -O $DCMQI_DOWNLOAD_PATH $DCMQI_RELEASE_URL --no-check-certificate \
 && tar -xvf $DCMQI_DOWNLOAD_PATH \
 && sudo mv ${DCMQI_PATH}/bin/* /bin \
 && rm $DCMQI_DOWNLOAD_PATH  \
 && rm -r $DCMQI_PATH

# Create directories that will be used as mounting points
RUN mkdir /app/data /app/data/input_data /app/data/output_data 

# Set PYTHONPATH to the /app folder
ENV PYTHONPATH="/app"

# FIXME: pass it as a command to the container in Slicer
CMD ["python3", "/app/mhub/thresholder/scripts/run.py"]