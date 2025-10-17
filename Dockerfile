FROM openjdk:17-slim

# Install Python, pip, and curl
RUN apt-get update && apt-get install -y python3 python3-pip curl && rm -rf /var/lib/apt/lists/*

# Set the working directory inside container
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Download and install Nextflow executable
RUN curl -s https://get.nextflow.io | bash

# Add the Nextflow executable to the system's PATH
ENV PATH="/app:${PATH}"

# Copy all project files (Python scripts, main.nf, etc.) into the container
COPY . .

# Make Python scripts executable
RUN chmod +x bin/*.py

# Set the main command that will always run
ENTRYPOINT ["nextflow", "run", "main.nf"]

CMD ["--input", "data", "--output", "results"]
