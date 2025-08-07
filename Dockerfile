# Imagen base con Python
FROM python:3.9-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instala Chrome y dependencias
RUN apt-get update && apt-get install -y \
    wget unzip gnupg curl \
    fonts-liberation libappindicator3-1 libasound2 libnspr4 libnss3 libxss1 xdg-utils libu2f-udev libvulkan1 \
    && rm -rf /var/lib/apt/lists/*

# Instala Chrome
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Instala ChromeDriver
RUN pip install --no-cache-dir chromedriver-autoinstaller

# Crea directorio de trabajo
WORKDIR /app
COPY . /app

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Da permisos de ejecución al entrypoint
RUN chmod +x /app/entrypoint.sh

# Usa el script como punto de entrada
ENTRYPOINT ["/app/entrypoint.sh"]

RUN ls -l /app