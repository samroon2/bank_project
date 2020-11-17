FROM python:3.6-slim

# Create a directory to copy code into.
RUN mkdir /test_location
# Copy code into container.
COPY bank /test_location/bank
COPY tests /test_location/tests
# Change work dir.
WORKDIR /test_location
# pip install pytest.
RUN pip install pytest
# Run tests.
ENTRYPOINT ["pytest"]
CMD ["."]
