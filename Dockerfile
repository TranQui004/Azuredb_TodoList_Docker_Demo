# Sử dụng Python image chính thức
FROM python:3.9-slim

# Cài đặt các thư viện cần thiết
#Cài đặt msodbcsql17 để hỗ trợ kết nối Microsoft SQL Server.
RUN apt-get update && apt-get install -y curl gnupg
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Tạo và thay đổi thư mục làm việc thành /app
WORKDIR /app

# Copy các file vào container
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Thiết lập lệnh chạy ứng dụng Flask
CMD ["python", "app.py"]
