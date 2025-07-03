# 🖼️ Image Sorter & Labeling Tool for Machine Learning

This is a Django-based web application that allows you to upload multiple images (or a zip of images), classify them into user-defined categories, and download the labeled data in organized folders. Ideal for preparing datasets for machine learning and computer vision tasks.

---

## 🚀 Features

- 📁 Upload single images or `.zip` files (supports `.jpg`, `.png`, `.heic`)
- ✍️ Define custom class names before labeling
- 🖱️ Label images via a simple slideshow interface
- 🔁 Navigate forward/backward to correct labels
- 💾 Save and resume sessions — never lose progress
- 📦 Download labeled images grouped by class in a zip file
- 🗑️ Delete old sessions and their data
- ✅ HEIC images are automatically converted to JPG

---

## 📸 Example Use Cases

- Preparing datasets for ML classification
- Manual image labeling for computer vision tasks
- Organizing image collections by category
- Teaching dataset labeling in workshops

---

## 🧰 Tech Stack

- **Backend**: Django 5
- **Frontend**: HTML, Bootstrap 5 (inlined)
- **Image Handling**: Pillow + pillow-heif
- **Database**: SQLite (default, can be changed)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/image-sorter.git
cd image-sorter
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Run the Server

```bash
python manage.py runserver
```

Visit: http://localhost:8000

---

## 📂 File Structure

```
├── core/
│   ├── models.py           # UploadSession, UploadedImage, LabeledImage
│   ├── views.py            # Upload, label, relabel, delete, download
│   ├── templates/
│   │   ├── index.html      # Upload + Start labeling
│   │   ├── label.html      # Labeling interface
│   │   ├── session_list.html
│   │   └── relabel.html
│   └── urls.py
├── media/                  # Image uploads (auto-created)
├── db.sqlite3              # Default database
└── manage.py
```

---

## 📦 Download Format

After labeling, images are grouped into folders by label and zipped:

```
classified_session_<id>.zip
├── ripe/
│   ├── img1.jpg
│   └── img2.jpg
├── unripe/
│   ├── img3.jpg
│   └── img4.jpg
```

---

## 🧠 Notes

- For large uploads, ZIP is recommended (more efficient)
- You can relabel images at any time via the session list
- Images are stored on the file system (not in the DB)
- Skipped images remain unlabeled — you can return to them

---

## ❌ To-Do / Improvements

- Add keyboard shortcuts for fast labeling
- Grid view for relabeling
- Auto-save last position in browser
- Cloud storage support (e.g. S3)

---

## 🧑‍💻 Author

**Rotich Kibet** | [LinkedIn](https://linkedin.com/in/rotichkibet) | [GitHub](https://github.com/Kibet-Rotich) | [Portfolio](https://kibet-rotich.github.io/portfolio/)

---

## 📄 License

This project is licensed under the MIT License.
