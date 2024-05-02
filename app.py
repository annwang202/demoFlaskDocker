from flask import Flask
from flask import render_template, redirect, request
import os

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app = Flask(__name__,static_url_path='/static')

@app.route("/")
def hello_world():
    directory = os.path.join(app.root_path, 'static', 'doc_uploads')
    photos = [file for file in os.listdir(directory) if file.endswith(('jpg', 'jpeg', 'png', 'gif'))]
    return render_template("index.html",photos=photos)

@app.route('/submit-resource', methods=['GET', 'POST'])
def submit_resource():
    if request.method == 'POST':
        try:
            if request.form.get("create-resource"): 
                print("Hello?")
                resource_type = request.form["type"]
                print(resource_type)
                name = request.form["resource_name"]
                print(name)
                photo_file = request.files["resource_photo"]
                print("form data retrieved?")
                if photo_file:
                    file_content = photo_file.read()
                    print('length of photo:')
                    print(len(file_content))
                    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
                    custom_filename = resource_type.replace(" ", "_") + name.replace(" ", "_")
                    ext = photo_file.filename.rsplit('.', 1)[1].lower()
                    if '.' in photo_file.filename and ext in ALLOWED_EXTENSIONS:
                        if len(photo_file.read()) > MAX_FILE_SIZE:
                            print('Photo file size exceeds the limit')
                        else:
                            print('adding photo to directory')
                            custom_filename = 'doc_uploads/' + custom_filename + '.' + ext
                            with open('static/' + custom_filename, 'wb') as f:
                                f.write(file_content)
        except Exception as e:
            print(f"An error occurred: {e}")
    return redirect('/')

if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 5000,debug=True)
