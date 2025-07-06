-- Bảng danh mục công việc
CREATE TABLE Categories (
    CategoryID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(50) NOT NULL
);

-- Bảng người dùng
CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(50) UNIQUE NOT NULL,
    Password NVARCHAR(255) NOT NULL -- Nên mã hóa mật khẩu trong thực tế
);

-- Bảng công việc (đã cập nhật)
CREATE TABLE Tasks (
    TaskID INT IDENTITY(1,1) PRIMARY KEY,
    Description NVARCHAR(255) NOT NULL,
    IsCompleted BIT NOT NULL DEFAULT 0,
    DueDate DATE NULL, -- Thay đổi kiểu dữ liệu thành DATE
    CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
    CategoryID INT NULL,
    UserID INT NULL,  -- Thêm cột UserID
    Details NVARCHAR(MAX) NULL, -- Thêm cột Details
    CONSTRAINT FK_Tasks_Categories FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID),
    CONSTRAINT FK_Tasks_Users FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Thêm user mẫu (username: user, password: 123)
INSERT INTO Users (Username, Password) VALUES ('user', '123'); -- Không mã hóa, chỉ dùng cho demo

-- Chèn dữ liệu mẫu cho bảng Categories
INSERT INTO Categories (Name) VALUES 
(N'Công việc cá nhân'),
(N'Công việc văn phòng'),
(N'Dự án lớn');

-- Chèn dữ liệu mẫu cho bảng Tasks (đã cập nhật với UserID và Details)
-- Giả sử UserID = 1 tương ứng với username 'user'
INSERT INTO Tasks (Description, IsCompleted, DueDate, CategoryID, UserID, Details) VALUES
(N'Viết báo cáo', 0, '2024-11-15', 2, 1, N'Hoàn thành báo cáo cuối năm'),
(N'Học Docker', 0, '2024-11-20', 1, 1, N'Tìm hiểu về Docker và containerization'),
(N'Triển khai dự án web', 1, NULL, 3, 1, N'Deploy dự án lên server');


-- Thêm danh mục mặc định
IF NOT EXISTS (SELECT 1 FROM Categories WHERE Name = N'Không có danh mục')
BEGIN
    INSERT INTO Categories (Name) VALUES (N'Không có danh mục');
END;