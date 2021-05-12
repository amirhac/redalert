FROM python:3
ADD main.py /
ADD requirements.txt /
ENV TZ=Asia/Jerusalem
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip install -r requirements.txt
CMD [ "python", "./main.py" ]