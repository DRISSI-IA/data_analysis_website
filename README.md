![image](https://github.com/user-attachments/assets/41d37864-cbd2-4f66-a66f-d4dbbcb2651e)

# Data Analysis Project

This project is a Django-based web application for analyzing, visualizing, and managing datasets. It includes features like data uploads, statistical summaries, and interactive visualizations.

## Project Structure

```
data_analysis/
├── .vscode/                  # VSCode configurations (optional)
├── data_analysis/            # Main Django project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py           # Project settings
│   ├── urls.py               # URL routing
│   ├── views.py              # Base views
│   ├── wsgi.py
│   └── __pycache__/          # Compiled Python files
├── media/
│   ├── graphs/               # Generated graph images
│   ├── uploads/              # Uploaded datasets
├── pages/                    # Main application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py              # Forms for data uploads
│   ├── models.py             # Data models
│   ├── tests.py
│   ├── urls.py               # Application-specific URLs
│   ├── views.py              # Application views
│   ├── migrations/           # Database migrations
│   └── __pycache__/
├── templates/
│   ├── pages/                # HTML templates
│       ├── base.html
│       ├── home.html
│       ├── overview.html
│       ├── upload.html
│       ├── visualize.html
├── uploads/                  # Example uploaded data
├── db.sqlite3                # SQLite database
├── manage.py                 # Django project management script
```

## Features

- **Data Uploads:** Upload CSV and Excel files for analysis.
- **Visualizations:** Generate graphs such as histograms and heatmaps.
- **Statistical Summaries:** Compute metrics like mean, standard deviation, and mode.
- **Data Management:** Easily manage datasets and results.

## Installation

### Prerequisites
- Python 3.12 or later
- Django 5.0.6 or later

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/DRISSI-IA/data_analysis_website.git
   cd data_analysis
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run database migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Visit the home page at `http://127.0.0.1:8000/`.
2. Upload a dataset on the "Upload" page.
3. View statistical summaries and visualizations on the "Overview" and "Visualize" pages.

## Project Files

### Key Python Files
- `data_analysis/settings.py`: Django project settings.
- `pages/views.py`: Core logic for handling data uploads and analysis.
- `pages/forms.py`: Forms for file uploads.
- `pages/models.py`: Data models for the application.

### Templates
- `templates/pages/base.html`: Main layout.
- `templates/pages/home.html`: Homepage.
- `templates/pages/overview.html`: Statistical overview.
- `templates/pages/upload.html`: Data upload page.
- `templates/pages/visualize.html`: Data visualization page.

### Media
- **Graphs:** Contains generated plots such as histograms and heatmaps.
- **Uploads:** Contains uploaded datasets for analysis.
