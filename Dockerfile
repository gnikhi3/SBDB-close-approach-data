FROM python:3

WORKDIR /usr/src/app
COPY pip_packages.txt ./
RUN pip install --no-cache-dir -r pip_packages.txt
COPY . .
RUN ["chmod", "+x", "/usr/src/app/start.sh"]
ENTRYPOINT ["/usr/src/app/start.sh"]
EXPOSE 7000