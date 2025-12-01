# 1. Python Image
FROM python:3.9-slim

# 2. System Tools (Git & Sound Libraries added)
# 'git' add kar diya hai taaki AI crash na ho
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    curl \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# 3. Install Rust (AI Compiler)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# 4. Setup Work Folder
WORKDIR /app

# 5. Install Python Libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy App Files
COPY . .

# 7. Start Server
CMD ["gunicorn", "-b", "0.0.0.0:10000", "server:app", "--timeout", "300"]