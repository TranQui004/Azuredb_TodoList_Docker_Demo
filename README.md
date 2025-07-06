# Tiểu luận: Tìm hiểu và Triển khai Công nghệ Docker

## Giới thiệu

Đây là tiểu luận môn "Ảo hóa và Điện toán đám mây" của nhóm sinh viên Trường Đại học Công Thương TP. HCM, Khoa Công nghệ Thông tin. Tiểu luận tập trung vào việc **tìm hiểu sâu sắc các khái niệm cơ bản, nguyên lý hoạt động và quy trình triển khai của công nghệ Docker**.

Mục tiêu của tiểu luận là cung cấp cái nhìn toàn diện về Docker, từ lịch sử hình thành, các khái niệm cốt lõi (Image, Container, Dockerfile, Docker Hub, Docker Compose, Docker Network, Docker Host), đến cách thức cài đặt và triển khai ứng dụng thực tế sử dụng Docker. Đặc biệt, tiểu luận còn đi sâu vào việc triển khai ứng dụng trên môi trường đám mây (Azure) và đóng gói ứng dụng thành Docker Image để dễ dàng quản lý và triển khai.

## Nội dung chính của Tiểu luận

Tiểu luận được cấu trúc thành 3 chương chính:

### Chương 1: Giới thiệu về Docker
*   Lịch sử hình thành và sự phát triển của Docker.
*   Các khái niệm cơ bản của Docker: Docker Engine (Server, REST API, CLI), Docker Hub, Dockerfile, Images, Container, Docker Compose, Docker Registry, Docker Network, Docker Host.
*   Nguyên lý và quy trình hoạt động của Docker.
*   Cài đặt môi trường Docker trên Windows (bao gồm WSL 2 và Docker Desktop).
*   Giới thiệu các chức năng chính trong Docker Desktop (Containers, Images, Volumes, Builds, Docker Scout, Extensions).
*   Hệ thống lưu trữ của Docker (Union File System, Storage, Volumes, Bind Mounts, Tmpfs Mounts).

### Chương 2: Thực nghiệm
*   **Triển khai trên dịch vụ đám mây:**
    *   Tạo và kết nối đến SQL Server bằng dịch vụ SQL Database của Azure.
    *   Cấu hình Firewall và truy cập Connection String.
*   **Triển khai Web App To-Do List:**
    *   Giới thiệu ứng dụng Web App To-Do List (được xây dựng bằng Python và Flask, kết nối Azure SQL Database).
    *   Cấu trúc thư mục và các thư viện cần thiết.
    *   Tạo Dockerfile để xây dựng Docker Images.
    *   Sử dụng Docker Compose để deploy ứng dụng.
    *   Đẩy Image lên Docker Hub.
    *   Kéo Image về máy và chạy Container.
    *   Triển khai ứng dụng lên nền tảng đám mây (Render).

### Chương 3: Tổng kết
*   Kết quả thực nghiệm đạt được.
*   So sánh Docker và Máy ảo (Virtual Machine) về tài nguyên, hiệu suất và tính di động.
*   Đánh giá ưu và nhược điểm của Docker.
*   Hướng phát triển của Docker trong tương lai.

## Công nghệ và Công cụ sử dụng trong phần Thực nghiệm

*   **Ngôn ngữ lập trình:** Python
*   **Framework:** Flask
*   **Database:** Azure SQL Database
*   **Containerization:** Docker (Dockerfile, Docker Compose)
*   **Nền tảng đám mây:** Microsoft Azure, Render (cho triển khai ứng dụng)
*   **Quản lý Docker Images:** Docker Hub

## Nhóm thực hiện

**Giảng viên hướng dẫn:**
*   ThS. Nguyễn Quốc Sử

**Nhóm:** Ảo ảo ảo

**Trưởng nhóm:**
*   Nguyễn Văn Thành

**Thành viên:**
1.  Bùi Tuấn Kiệt
2.  Lăng Minh Hải
3.  Trần Trọng Quí
4.  Nguyễn Minh Sang
5.  Nguyễn Hoành Thịnh

## Liên hệ

Nếu có bất kỳ câu hỏi hoặc góp ý nào, vui lòng liên hệ với nhóm qua GitHub Issues.

---

**TP. HỒ CHÍ MINH, tháng 09 năm 2024**
