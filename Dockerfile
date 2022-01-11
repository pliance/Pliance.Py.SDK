FROM python
WORKDIR /work
RUN python3 -m pip install --user --upgrade setuptools wheel
ADD .pypirc /root/
ADD setup.py .
RUN mkdir pliance_py_sdk
RUN python3 setup.py sdist bdist_wheel
RUN python3 -m pip install --user --upgrade twine
ADD . .
RUN sed 's/2021.11.1/2022.1.2/g' -i setup.py
RUN python3 -m twine upload --repository pliance.py.sdk dist/*

