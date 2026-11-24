import sqlite3
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
DATABASE = "notes.db"


# Подключение к БД, row_factory позволяет обращаться к полям по имени
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Создание таблицы
def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT
            )
        """)


# Главная страница со списком всех заметок
@app.route("/")
def index():
    conn = get_db()
    notes = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", notes=notes)


# GET показывает форму, POST сохраняет новую запись
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        conn = get_db()
        # Параметризованный запрос защищает от SQL-инъекций
        conn.execute(
            "INSERT INTO notes (title, content) VALUES (?, ?)",
            (title, content)
        )
        conn.commit()
        conn.close()
        # redirect после POST — чтобы F5 не создавал дубль
        return redirect(url_for("index"))
    return render_template("form.html", note=None)


# GET показывает форму с текущими данными, POST обновляет запись
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()
    note = conn.execute("SELECT * FROM notes WHERE id = ?", (id,)).fetchone()
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        conn.execute(
            "UPDATE notes SET title = ?, content = ? WHERE id = ?",
            (title, content, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    conn.close()
    return render_template("form.html", note=note)


# Удаление по id, затем возврат на главную
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()          # таблица создастся до старта сервера
    app.run(debug=True)
