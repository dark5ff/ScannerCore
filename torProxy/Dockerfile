FROM alpine:latest
RUN apk update && apk add tor

COPY torrc /etc/tor/torrc
RUN chown -R tor /etc/tor

RUN mkdir -p /tmp/tor/log/
RUN chmod -R 777 /tmp/tor/log
RUN chown -R tor /tmp/tor/log

USER tor
ENTRYPOINT ["tor"]
CMD ["-f", "/etc/tor/torrc"]

