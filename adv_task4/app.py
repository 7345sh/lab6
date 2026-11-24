import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
# Очищает имя файла от опасных символов
from werkzeug.utils import secure_filename


app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        # Проверка, что файл выбран
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("upload"))
    # Список уже загруженных файлов для отображения на странице
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("upload.html", files=files)


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    # send_from_directory безопасно отдаёт файл из папки uploads/
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)
