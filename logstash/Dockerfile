FROM docker.elastic.co/logstash/logstash:7.8.1
COPY logstash.yml /usr/share/logstash/config/logstash.yml
RUN rm -r /usr/share/logstash/pipeline/* 
COPY pipes.conf /usr/share/logstash/pipeline/pipes.conf
