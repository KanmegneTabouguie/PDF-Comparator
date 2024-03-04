from flask import Flask, render_template, request
from PyPDF2 import PdfReader

app = Flask(__name__)

def are_pdfs_identical(file1, file2):
    try:
        with file1, file2:
            pdf1 = PdfReader(file1)
            pdf2 = PdfReader(file2)
            
            num_pages1 = len(pdf1.pages)
            num_pages2 = len(pdf2.pages)

            identical_text = pdf1.pages[0].extract_text() == pdf2.pages[0].extract_text()

            return {
                'identical_text': identical_text,
                'num_pages1': num_pages1,
                'num_pages2': num_pages2
            }
    except Exception as e:
        print(f"Error reading PDFs: {e}")
        return {
            'identical_text': False,
            'num_pages1': 0,
            'num_pages2': 0
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']
        if file1 and file2:
            result = are_pdfs_identical(file1.stream, file2.stream)
            return render_template('index.html', result=result)
    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)
