ARG OS
FROM cangjians/pycangjie:${OS}
MAINTAINER Cangjians (https://cangjians.github.io)

# basic environment for building
WORKDIR /usr/local/src/ibus-cangjie

# copy source files to build
COPY "." "./"

# build the library
RUN ./autogen.sh --prefix=/usr && \
  make && make install
