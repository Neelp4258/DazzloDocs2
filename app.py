from flask import Flask, request, jsonify, send_file, render_template
from enhanced_docs_generator import EnhancedDocumentGenerator, COLOR_SCHEMES, TEMPLATES
from io import BytesIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-please-change-in-production')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/templates')
def get_templates():
    # Convert templates to the format expected by frontend
    formatted_templates = {}
    for key, template in TEMPLATES.items():
        formatted_templates[key] = {
            'name': key.replace('_', ' ').title(),
            'sections': template.get('sections', [])
        }
    return jsonify(formatted_templates)

@app.route('/api/color-schemes')
def get_color_schemes():
    return jsonify(COLOR_SCHEMES)

@app.route('/api/generate', methods=['POST'])
def generate_document():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['student_name', 'class', 'roll_number', 'subject', 'subject_teacher', 'assignment_topic']
        for field in required_fields:
            if not data['user_data'].get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create enhanced document generator
        doc_generator = EnhancedDocumentGenerator()
        
        # Set user data
        doc_generator.user_data = data['user_data']
        
        # Set template and colors
        if not data.get('template') or not data.get('color_scheme'):
            return jsonify({'error': 'Template and color scheme are required'}), 400
            
        doc_generator.template = TEMPLATES[data['template']]
        doc_generator.set_colors(data['color_scheme'])
        
        # Set content
        doc_generator.content = data.get('content', {})
        
        # Add charts if provided
        if 'charts' in data:
            for section, section_charts in data['charts'].items():
                for chart in section_charts:
                    doc_generator.add_chart(
                        section=section,
                        chart_type=chart['type'],
                        data=chart['data'],
                        title=chart.get('title', '')
                    )
        
        # Add tables if provided
        if 'tables' in data:
            for section, section_tables in data['tables'].items():
                for table_info in section_tables:
                    # Pass the parameters in the correct order: section, data, title
                    doc_generator.add_table(
                        section=section,
                        data=table_info['data'],
                        title=table_info.get('title', 'Table')
                    )
        
        # Add code blocks if provided
        if 'code_blocks' in data:
            for section, section_codes in data['code_blocks'].items():
                for code in section_codes:
                    doc_generator.add_code_block(
                        section=section,
                        code=code['code'],
                        language=code.get('language', 'text')
                    )
        
        # Generate PDF in memory
        pdf_buffer = BytesIO()
        doc_generator.generate_pdf(output=pdf_buffer)
        pdf_buffer.seek(0)
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"DazzloDocs_{data['user_data']['student_name']}_{data['user_data']['subject']}.pdf"
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/chart-types')
def get_chart_types():
    """Get available chart types"""
    return jsonify(['bar', 'pie', 'line'])

@app.route('/api/code-languages')
def get_code_languages():
    """Get available code languages"""
    return jsonify(['python', 'javascript', 'java', 'cpp', 'sql'])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true') 