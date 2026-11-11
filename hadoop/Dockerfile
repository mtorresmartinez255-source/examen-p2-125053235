FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-17-jdk-headless \
    python3 \
    openssh-server \
    openssh-client \
    curl \
    ca-certificates \
    procps && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV PATH="${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin:${PATH}"

RUN curl -fL \
    https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz \
    -o /tmp/hadoop.tar.gz && \
    tar -xzf /tmp/hadoop.tar.gz -C /opt && \
    mv /opt/hadoop-3.3.6 /opt/hadoop && \
    rm /tmp/hadoop.tar.gz

RUN useradd -m -s /bin/bash hadoop

COPY hadoop/iniciar.sh /usr/local/bin/iniciar-hadoop.sh
COPY hadoop/procesar.sh /usr/local/bin/procesar.sh

RUN chmod +x /usr/local/bin/iniciar-hadoop.sh /usr/local/bin/procesar.sh

CMD ["/usr/local/bin/iniciar-hadoop.sh"]
