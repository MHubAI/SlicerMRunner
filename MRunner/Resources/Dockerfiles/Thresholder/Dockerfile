# Specify the base image for the environment
FROM ubuntu:18.04

# Specify the maintainer of the image
LABEL maintainer="lnuernberg@bwh.harvard.edu"

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
&& rm -rf /var/lib/apt/lists/*

# Create a working directory
RUN mkdir /app
WORKDIR /app

# Create a non-root user "user" and switch to it
# We can rename "user" after AIMI in the future
ARG USER_ID
ARG GROUP_ID

RUN groupadd -g $GROUP_ID user \
 && adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID --shell /bin/bash user \
 && chown -R user:user /app
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user
USER user

# Set up a user directory for "user"
ENV HOME=/home/user
RUN mkdir $HOME/.cache $HOME/.config \
 && chmod -R 777 $HOME

# Install task specific system packages 
RUN sudo apt-get update && sudo apt-get install -y plastimatch

# Copy the YAML environment file in the container
COPY ./environment.yaml /app/environment.yaml

# Set up Conda and install a very minimal base environment
ENV CONDA_AUTO_UPDATE_CONDA=false \
    PATH=$HOME/miniconda/bin:$PATH

ENV CONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"

RUN wget -O ~/miniconda.sh $CONDA_URL --no-check-certificate \
 && chmod +x ~/miniconda.sh \
 && bash ~/miniconda.sh -b -p ~/miniconda \
 && rm ~/miniconda.sh \
 && conda env update -n base -f /app/environment.yaml \
 && sudo rm /app/environment.yaml \
 && conda clean -ya

RUN conda update -n base -c defaults conda
RUN echo "conda activate base" > ~/.bashrc

# Install general utilities (specify version if necessary)
RUN pip3 install --upgrade pip \
 && pip3 install --no-cache-dir \
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

# Clone git repositories  # aimi_beta
ARG CACHEBUST=3
ENV aimi_branch="thresholder"
RUN git config --global http.sslVerify false 
RUN git clone -b $aimi_branch https://github.com/AIM-Harvard/aimi_alpha.git /app/
RUN git clone https://github.com/pieper/dicomsort.git /app/dicomsort

# Make dicomsort callable
COPY dicomsort.sh $HOME/miniconda/bin/dicomsort 
RUN sudo chmod +x $HOME/miniconda/bin/dicomsort 

# Create useful aliases
RUN echo 'alias ll="ls -alF"' >> ~/.bashrc

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

################################################################################

CMD ["python", "/app/aimi/thresholder/scripts/run.py"]

# Build on Mac
# cd ~/Projects/SlicerMHubIntegration/thresholder/docker
# docker build --build-arg USER_ID=1001 --build-arg GROUP_ID=1001 --platform=linux/amd64 -t=leo/thresholder .

# Run
# cd ~/Projects/SlicerMHubIntegration/thresholder
# docker run -it --volume $(pwd)/sample_data_nrrd:/app/data/input_data --volume $(pwd)/sample_output:/app/data/output_data leo/thresholder
