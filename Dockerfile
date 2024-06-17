# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV pg_user_name = postgres.ctxvsrfwmbfxsodwuvxv
ENV pg_password = BRtYThN3ZnIRO676
ENV pg_host = aws-0-ap-southeast-1.pooler.supabase.com
ENV pg_port = 6543
ENV pg_db_name = postgres


ENV user_name = loclh
ENV azure_user_name = peterle
ENV mongodb_connection_string=mongodb+srv://loclh:1@cluster0.rxcryft.mongodb.net/?tlsAllowInvalidCertificates=true
ENV azure_connection_string=mongodb+srv://peterle:EaSport69696969@auragenai.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000&tlsAllowInvalidCertificates=true
# ENV db_name = "aura_1"
ENV db_name=test_vector
ENV collection_name=services

ENV BATCH_SIZE=1000

# Run app.py when the container launches
CMD ["flask", "run"]