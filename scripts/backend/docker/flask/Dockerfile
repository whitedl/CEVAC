FROM cevac:base
RUN pip install flask_restful
ADD ./src /root
WORKDIR /root
CMD ["gunicorn", "admin:app", "-b", "0.0.0.0:5000"]
