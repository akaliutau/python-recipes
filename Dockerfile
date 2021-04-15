FROM rabbitmq:3.8-alpine

MAINTAINER Aliaksei Kaliutau

WORKDIR /usr/local/rabbitmq

# Define environment variables.
ENV RABBITMQ_USER user
ENV RABBITMQ_PASSWORD user
ENV RABBITMQ_PID_FILE /var/lib/rabbitmq/mnesia/rabbitmq

COPY ./rabbitmq-init.sh /usr/local/rabbitmq/rabbitmq-init.sh
RUN chmod +x /usr/local/rabbitmq/rabbitmq-init.sh
EXPOSE 5672
EXPOSE 15672

# Define default command
CMD ["./rabbitmq-init.sh"]