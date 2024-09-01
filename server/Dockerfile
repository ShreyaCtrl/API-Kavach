FROM ghcr.io/zaproxy/zaproxy:stable
COPY ./ /

WORKDIR /

EXPOSE 5000

CMD ["zap-baseline.py", "-t", "http://localhost:80", "-r", "zap_report.html"]
