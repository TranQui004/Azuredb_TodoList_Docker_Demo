from flask import Flask, render_template, request, redirect, url_for, flash,get_flashed_messages
import pyodbc
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'f7389d10a2e3f47b6c5d12ab8f4c9a6e'


# Cấu hình kết nối
server = 'baron.database.windows.net'
database = 'db_todo'
username = 'baron'
password = 'Van1404@Thanh'
driver = '{ODBC Driver 17 for SQL Server}'

# Hàm kết nối đến Azure SQL Database
def connect_to_db():
    return pyodbc.connect(
        f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    )

# Cấu hình Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect đến trang login nếu chưa đăng nhập



# User model cho Flask-Login
class User(UserMixin):
    def __init__(self, userid, username, password):
        self.id = userid
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(userid):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE UserID = ?", (userid,))
        user_data = cursor.fetchone()
        if user_data:
            return User(user_data.UserID, user_data.Username, user_data.Password)
        return None
    except Exception as e:
        print(f"Lỗi khi load user: {e}") # In ra console để debug
        return None
    finally:
        if 'connection' in locals():
            connection.close()


# Route đăng nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            connection = connect_to_db()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?", (username, password))
            user = cursor.fetchone()
            if user:
                user_obj = User(user.UserID, user.Username, user.Password)
                login_user(user_obj)
                flash('Đăng nhập thành công!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'danger')
        except Exception as e:
            flash(f'Lỗi: {e}', 'danger') # Hiển thị lỗi cho người dùng
        finally:
            if 'connection' in locals():
                connection.close()
    return render_template('login.html')

# Route đăng ký
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            connection = connect_to_db()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)", (username, password))
            connection.commit()
            flash('Đăng ký thành công!', 'success')
            return redirect(url_for('login'))
        except pyodbc.IntegrityError: # Xử lý lỗi trùng lặp username
            flash('Tên đăng nhập đã tồn tại!', 'danger')
        except Exception as e:
            flash(f'Lỗi: {e}', 'danger')
        finally:
            if 'connection' in locals():
                connection.close()
    return render_template('register.html')

# Route đăng xuất
@app.route('/logout')
@login_required
def logout():
    logout_user()
    get_flashed_messages() # Xóa tất cả flash messages
    return redirect(url_for('index'))

# Trang chủ - Hiển thị danh sách công việc của người dùng hiện tại
@app.route('/')
@login_required  # Yêu cầu đăng nhập để xem trang này
def index():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT t.TaskID, t.Description, t.IsCompleted, t.DueDate, t.CreatedDate, c.Name AS Category
            FROM Tasks t
            LEFT JOIN Categories c ON t.CategoryID = c.CategoryID
            WHERE t.UserID = ?
            ORDER BY t.TaskID ASC
        """, (current_user.id,)) # Lấy task của user hiện tại
        tasks = cursor.fetchall()

        cursor.execute("SELECT * FROM Categories")
        categories = cursor.fetchall()

        return render_template('index.html', tasks=tasks, categories=categories, filters={}, username=current_user.username) # Truyền username vào template
    except Exception as e:
        flash(f"Lỗi: {e}", 'danger')
        return redirect(url_for('index')) # Redirect về index để tránh lỗi
    finally:
        if 'connection' in locals():
            connection.close()

# Thêm công việc mới
@app.route('/add', methods=['POST'])
@login_required
def add_task():
    description = request.form['description']
    due_date = request.form['due_date'] or None
    details = request.form.get('details', None)  # Lấy nội dung chi tiết
    category_id = request.form.get('category_id', None)
    is_completed = 1 if 'is_completed' in request.form else 0  # Lấy trạng thái từ form

    # Nếu không chọn danh mục, gán vào danh mục mặc định
    if not category_id:
        try:
            connection = connect_to_db()
            cursor = connection.cursor()
            cursor.execute("SELECT CategoryID FROM Categories WHERE Name = N'Không có danh mục'")
            category_id = cursor.fetchone().CategoryID
        finally:
            if 'connection' in locals():
                connection.close()

    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO Tasks (Description, DueDate, Details, CategoryID, IsCompleted, UserID) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (description, due_date, details, category_id, is_completed, current_user.id))
        connection.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Lỗi khi thêm dữ liệu: {e}"
    finally:
        if 'connection' in locals():
            connection.close()

#Chi tiết công việc
@app.route('/details/<int:task_id>')
@login_required
def task_details(task_id):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT t.TaskID, t.Description, t.Details, t.IsCompleted, t.DueDate, t.CreatedDate, c.Name AS Category
            FROM Tasks t
            LEFT JOIN Categories c ON t.CategoryID = c.CategoryID
            WHERE t.TaskID = ? AND t.UserID = ? -- Thêm điều kiện kiểm tra UserID
        """, (task_id, current_user.id))
        task = cursor.fetchone()

        if not task:
            flash("Công việc không tồn tại hoặc bạn không có quyền truy cập!", 'danger')
            return redirect(url_for('index'))

        return render_template('details.html', task=task)
    except Exception as e:
        return f"Lỗi khi truy vấn dữ liệu: {e}"
    finally:
        if 'connection' in locals():
            connection.close()


# Cập nhật trạng thái công việc
@app.route('/complete/<int:task_id>')
@login_required
def complete_task(task_id):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("UPDATE Tasks SET IsCompleted = 1 WHERE TaskID = ? AND UserID = ?", (task_id, current_user.id))
        connection.commit()
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"Lỗi khi cập nhật dữ liệu: {e}", 'danger')
        return redirect(url_for('index'))
    finally:
        if 'connection' in locals():
            connection.close()

# Xóa công việc
@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Tasks WHERE TaskID = ? AND UserID = ?", (task_id, current_user.id))
        connection.commit()
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"Lỗi khi xóa dữ liệu: {e}", 'danger')
        return redirect(url_for('index'))
    finally:
        if 'connection' in locals():
            connection.close()

# Sửa công việc
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    if request.method == 'POST':
        description = request.form['description']
        due_date = request.form['due_date'] or None  # Nếu không chọn ngày thì giá trị là None
        details = request.form['details'] or None
        category_id = request.form.get('category_id', None)
        is_completed = 1 if 'is_completed' in request.form else 0  # Lấy trạng thái từ form

        try:
            connection = connect_to_db()
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE Tasks 
                SET Description = ?, DueDate = ?, Details = ?, CategoryID = ?, IsCompleted = ?
                WHERE TaskID = ? AND UserID = ?
            """, (description, due_date, details, category_id, is_completed, task_id, current_user.id))
            connection.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"Lỗi khi cập nhật dữ liệu: {e}"
        finally:
            if 'connection' in locals():
                connection.close()
    else:
        try:
            connection = connect_to_db()
            cursor = connection.cursor()
            # Sử dụng fetchone() và tạo từ điển với column names
            cursor.execute("SELECT * FROM Tasks WHERE TaskID = ?", (task_id,))
            columns = [column[0] for column in cursor.description]  # Lấy tên cột
            task = dict(zip(columns, cursor.fetchone()))  # Tạo dict từ cột và giá trị

            # Xử lý để hiển thị "Không có hạn" khi DueDate là NULL
            if task['DueDate'] is None:
                task['DueDate'] = None  # Chỉ cần để None khi không có ngày đến hạn

            cursor.execute("SELECT * FROM Categories")
            categories = cursor.fetchall()

            return render_template('edit.html', task=task, categories=categories)
        except Exception as e:
            return f"Lỗi khi truy vấn dữ liệu: {e}"
        finally:
            if 'connection' in locals():
                connection.close()

# Tìm kiếm và lọc công việc
@app.route('/search', methods=['GET'])
@login_required
def search_task():
    keyword = request.args.get('keyword', '')
    category_id = request.args.get('category_id', '')
    is_completed = request.args.get('is_completed', '')

    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        query = """
            SELECT t.TaskID, t.Description, t.IsCompleted, t.DueDate, t.CreatedDate, c.Name AS Category
            FROM Tasks t
            LEFT JOIN Categories c ON t.CategoryID = c.CategoryID
            WHERE t.UserID = ? AND t.Description LIKE ?
        """
        params = [current_user.id, f"%{keyword}%"]  # Thêm UserID vào tham số

        if category_id:
            query += " AND t.CategoryID = ?"
            params.append(category_id)
        if is_completed:
            query += " AND t.IsCompleted = ?"
            params.append(is_completed)

        cursor.execute(query, params)
        tasks = cursor.fetchall()

        cursor.execute("SELECT * FROM Categories")
        categories = cursor.fetchall()

        return render_template('index.html', tasks=tasks, categories=categories, filters=request.args, username=current_user.username)
    except Exception as e:
        return f"Lỗi khi truy vấn dữ liệu: {e}"
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True) 
