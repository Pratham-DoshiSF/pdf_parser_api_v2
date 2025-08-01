from flask import Flask, request, jsonify
import os
import shutil
import tempfile
import uuid
from markitdown import MarkItDown

app = Flask(__name__)
md = MarkItDown(enable_plugins=True)

@app.route("/pdf_to_markdown", methods=["POST"])
def pdf_conversion():
    if 'pdf_file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    suffix = os.path.splitext(pdf_file.filename)[1]
    pdf_dir = os.path.join("/tmp/", str(uuid.uuid4()))
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, f"upload{suffix}")

    try:
        # Save the file to disk
        pdf_file.save(pdf_path)

        # Convert to markdown
        result = md.convert(pdf_path)

        return jsonify({
            "filename": pdf_file.filename,
            "content_type": pdf_file.content_type,
            "content": result.text_content,
        })

    finally:
        # Clean up temp directory
        if os.path.exists(pdf_dir):
            shutil.rmtree(pdf_dir)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)