# 1. Base Image (Python + Linux)
FROM python:3.9-slim

# 2. Install System Tools (Rust & Sound Libraries)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# 3. Install Rust (DeepFilterNet ke liye zaroori hai)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# 4. Working Directory
WORKDIR /app

# 5. Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy Project Files
COPY . .

# 7. Run Server (Using Gunicorn for Production)
CMD ["gunicorn", "-b", "0.0.0.0:10000", "server:app", "--timeout", "120"]