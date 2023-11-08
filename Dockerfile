# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
# COPY requirements.txt /app/
COPY ./requirements.txt .



# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Define environment variable
ENV streamlitEnv=

#expose port
EXPOSE 8501

# Run the command when the container launches
# CMD ["streamlit", "run", "app.py"]
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

