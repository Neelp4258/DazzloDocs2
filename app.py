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
        print("Received data:", data)  # Debug print
        
        # Check if data has the expected structure
        if not isinstance(data, dict):
            print("Error: data is not a dict, it's a", type(data))  # Debug print
            return jsonify({'error': 'Invalid data format'}), 400
        
        # Get user_data - handle both nested and flat structures
        user_data = data.get('user_data', data)
        print("User data:", user_data)  # Debug print
        
        # Validate required fields
        required_fields = ['student_name', 'class', 'roll_number', 'subject', 'subject_teacher', 
                         'assignment_topic', 'college_name']
        missing_fields = [field for field in required_fields if not user_data.get(field)]
        if missing_fields:
            print("Missing required fields:", missing_fields)  # Debug print
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        # Create enhanced document generator
        doc_generator = EnhancedDocumentGenerator()
        
        # Set user data
        doc_generator.user_data = user_data
        
        # Set template and colors
        if not data.get('template') or not data.get('color_scheme'):
            print("Missing template or color scheme")  # Debug print
            return jsonify({'error': 'Template and color scheme are required'}), 400
            
        template_name = data['template']
        color_scheme = data['color_scheme']
        print(f"Using template: {template_name}, color scheme: {color_scheme}")  # Debug print
        
        if template_name not in TEMPLATES:
            print(f"Invalid template name: {template_name}")  # Debug print
            return jsonify({'error': f'Invalid template name: {template_name}'}), 400
            
        if color_scheme not in COLOR_SCHEMES:
            print(f"Invalid color scheme: {color_scheme}")  # Debug print
            return jsonify({'error': f'Invalid color scheme: {color_scheme}'}), 400
            
        doc_generator.template = TEMPLATES[template_name]
        doc_generator.set_colors(color_scheme)
        
        # Set content
        content = data.get('content', {})
        print("Content data:", content)  # Debug print
        doc_generator.content = content
        
        # Add charts if provided
        if 'charts' in data:
            print("Processing charts:", data['charts'])  # Debug print
            for section, section_charts in data['charts'].items():
                print(f"Processing charts for section {section}:", section_charts)  # Debug print
                if not isinstance(section_charts, list):
                    print(f"Warning: section_charts is not a list for section {section}")  # Debug print
                    continue
                    
                for chart in section_charts:
                    if not isinstance(chart, dict):
                        print(f"Warning: chart is not a dict: {chart}")  # Debug print
                        continue
                    
                    print("Processing chart:", chart)  # Debug print
                    # Process chart data from frontend format
                    labels = chart.get('labels', '').split(',') if isinstance(chart.get('labels'), str) else []
                    values_str = chart.get('values', '').split(',') if isinstance(chart.get('values'), str) else []
                    
                    # Convert values to numbers
                    values = []
                    for val in values_str:
                        try:
                            values.append(float(val.strip()))
                        except (ValueError, AttributeError):
                            print(f"Warning: invalid value in chart: {val}")  # Debug print
                            values.append(0)
                    
                    # Create chart data structure
                    chart_data = {
                        'labels': labels,
                        'values': values,
                        'title': chart.get('title', 'Chart'),
                        'xlabel': 'Categories',
                        'ylabel': 'Values'
                    }
                    print("Created chart data:", chart_data)  # Debug print
                    
                    doc_generator.add_chart(
                        section,
                        chart.get('type', 'bar'),
                        chart_data
                    )
        
        # Add tables if provided
        if 'tables' in data:
            print("Processing tables:", data['tables'])  # Debug print
            for section, section_tables in data['tables'].items():
                print(f"Processing tables for section {section}:", section_tables)  # Debug print
                if not isinstance(section_tables, list):
                    print(f"Warning: section_tables is not a list for section {section}")  # Debug print
                    continue
                    
                for table_info in section_tables:
                    if not isinstance(table_info, dict):
                        print(f"Warning: table_info is not a dict: {table_info}")  # Debug print
                        continue
                    
                    print("Processing table:", table_info)  # Debug print
                    
                    # Process headers and data from the new table structure
                    headers = []
                    data_rows = []
                    
                    # Handle headers
                    if isinstance(table_info.get('headers'), list):
                        headers = [str(h) for h in table_info['headers']]
                    elif isinstance(table_info.get('headers'), str):
                        headers = [h.strip() for h in table_info['headers'].split(',') if h.strip()]
                    
                    # Handle data rows
                    table_data = table_info.get('data', [])
                    if isinstance(table_data, list):
                        for row in table_data:
                            if isinstance(row, list):
                                # Row is already a list
                                data_rows.append([str(cell) for cell in row])
                            elif isinstance(row, str):
                                # Row is a string, split by comma
                                cells = [cell.strip() for cell in row.split(',') if cell.strip()]
                                if cells:
                                    data_rows.append(cells)
                            else:
                                # Single value row
                                data_rows.append([str(row)])
                    elif isinstance(table_data, str):
                        # Fallback for string data (CSV format)
                        rows = [row.strip() for row in table_data.split('\n') if row.strip()]
                        for row in rows:
                            cells = [cell.strip() for cell in row.split(',') if cell.strip()]
                            if cells:
                                data_rows.append(cells)
                    
                    # Construct final table data
                    final_table_data = []
                    if headers:
                        final_table_data.append(headers)
                    if data_rows:
                        final_table_data.extend(data_rows)
                    
                    # If no data, provide default
                    if not final_table_data:
                        final_table_data = [['No data available']]
                    
                    # Ensure all rows have the same number of columns
                    max_cols = max(len(row) for row in final_table_data)
                    final_table_data = [row + [''] * (max_cols - len(row)) for row in final_table_data]
                    
                    print("Final table data:", final_table_data)  # Debug print
                    
                    # Add table to document
                    doc_generator.add_table(
                        section=section,
                        data=final_table_data,
                        title=table_info.get('title', 'Table')
                    )
        
        # Add code blocks if provided
        if 'code_blocks' in data:
            print("Processing code blocks:", data['code_blocks'])  # Debug print
            for section, section_codes in data['code_blocks'].items():
                if not isinstance(section_codes, list):
                    print(f"Warning: section_codes is not a list for section {section}")  # Debug print
                    continue
                    
                for code in section_codes:
                    if not isinstance(code, dict):
                        print(f"Warning: code is not a dict: {code}")  # Debug print
                        continue
                        
                    doc_generator.add_code_block(
                        section=section,
                        code=code.get('code', ''),
                        language=code.get('language', 'text')
                    )
        
        # Generate PDF in memory
        print("Generating PDF...")  # Debug print
        pdf_buffer = BytesIO()
        doc_generator.generate_pdf(output=pdf_buffer)
        pdf_buffer.seek(0)
        
        print("PDF generated successfully")  # Debug print
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"DazzloDocs_{user_data['student_name']}_{user_data['subject']}.pdf"
        )
    except Exception as e:
        import traceback
        print("Error occurred:", str(e))  # Debug print
        print("Traceback:", traceback.format_exc())  # Debug print full traceback
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