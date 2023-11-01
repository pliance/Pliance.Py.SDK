FROM python
WORKDIR /work
RUN python3 -m pip install --user --upgrade setuptools wheel
ENV VERSION "2023.11.1"
ADD .pypirc /root/
ADD setup.py .
RUN sed "s/2021.11.1/$VERSION/g" -i setup.py
RUN mkdir pliance_py_sdk
RUN python3 setup.py sdist bdist_wheel
RUN python3 -m pip install --user --upgrade twine
ADD . .
RUN python3 -m twine upload --repository pliance.py.sdk dist/* --verbose

