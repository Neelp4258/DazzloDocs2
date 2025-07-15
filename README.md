# DazzloDocs

A professional document generation system built with Flask. Create beautiful, well-formatted documents with support for charts, tables, and code blocks.

## Features

- Multiple document templates (Research Paper, Project Report, Case Study, etc.)
- Professional color schemes
- Support for charts and graphs
- Code block formatting
- Table generation
- Dynamic content sections

## Prerequisites

- Python 3.9+
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd DazzloDocs
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with the following variables:
```
FLASK_APP=app.py
FLASK_DEBUG=False
PORT=5000
SECRET_KEY=your-secret-key-here
```

## Running Locally

1. Activate the virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Run the application:
```bash
flask run
```

The application will be available at `http://localhost:5000`

## Deployment

This application is configured for deployment on Render.com:

1. Create a new Web Service on Render
2. Connect your repository
3. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Python Version: 3.9
4. Add the environment variables from the `.env` file in Render's environment variables section

## API Endpoints

- `/` - Home page
- `/about` - About page
- `/services` - Services page
- `/contact` - Contact page
- `/api/templates` - Get available templates
- `/api/color-schemes` - Get available color schemes
- `/api/generate` - Generate document (POST)
- `/api/chart-types` - Get available chart types
- `/api/code-languages` - Get available code languages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 