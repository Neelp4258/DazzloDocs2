// Template definitions
const TEMPLATES = {
    'assignment': {
        sections: ['introduction', 'main_content', 'analysis', 'conclusion', 'references']
    },
    'project_report': {
        sections: ['project_overview', 'objectives', 'methodology', 'implementation', 'results', 'conclusion', 'appendix']
    },
    'case_study': {
        sections: ['case_overview', 'problem_analysis', 'solutions', 'implementation', 'results', 'recommendations']
    },
    'research_paper': {
        sections: ['abstract', 'introduction', 'literature_review', 'methodology', 'results', 'discussion', 'conclusion', 'references']
    },
    'presentation_report': {
        sections: ['executive_summary', 'key_points', 'analysis', 'findings', 'recommendations']
    },
    'lab_report': {
        sections: ['objective', 'materials', 'procedure', 'observations', 'calculations', 'results', 'conclusion']
    },
    'business_plan': {
        sections: ['executive_summary', 'business_overview', 'market_analysis', 'strategy', 'financial_plan', 'implementation']
    },
    'technical_documentation': {
        sections: ['system_overview', 'architecture', 'implementation', 'testing', 'deployment', 'maintenance']
    }
};

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', handleSubmit);
    }
    
    // Add template change listener
    const templateSelect = document.getElementById('template');
    if (templateSelect) {
        templateSelect.addEventListener('change', updateContentSections);
    }
});

// Update content sections based on template selection
function updateContentSections() {
    const templateKey = document.getElementById('template').value;
    const templateSections = document.getElementById('templateSections');
    
    if (!templateSections) return;
    
    // Clear existing sections
    templateSections.innerHTML = '';
    
    if (templateKey && TEMPLATES[templateKey]) {
        const sections = TEMPLATES[templateKey].sections;
        
        sections.forEach(section => {
            const sectionDiv = document.createElement('div');
            sectionDiv.className = 'content-section';
            sectionDiv.setAttribute('data-section', section);
            
            const displayName = section.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            
            sectionDiv.innerHTML = `
                <h4>${displayName}</h4>
                <div class="form-group">
                    <textarea name="content_${section}" rows="6" placeholder="Enter ${displayName} content..."></textarea>
                </div>
                <div class="feature-buttons">
                    <button type="button" onclick="addTable('${section}')" class="feature-btn">📊 Add Table</button>
                    <button type="button" onclick="addChart('${section}')" class="feature-btn">📈 Add Chart</button>
                    <button type="button" onclick="addCodeBlock('${section}')" class="feature-btn">💻 Add Code</button>
                </div>
            `;
            
            templateSections.appendChild(sectionDiv);
        });
    }
}

// Add table functionality
function addTable(sectionName) {
    const section = document.querySelector(`[data-section="${sectionName}"]`);
    if (!section) return;
    
    const tableId = `table_${Date.now()}`;
    const tableHtml = `
        <div class="feature-container" id="${tableId}">
            <div class="feature-header">
                <h5>📊 Table</h5>
                <button type="button" onclick="removeFeature('${tableId}')" class="remove-btn">✕</button>
            </div>
            <div class="form-group">
                <input type="text" name="table_title_${tableId}" placeholder="Table Title" class="feature-input">
            </div>
            <div class="form-group">
                <input type="text" name="table_headers_${tableId}" placeholder="Headers (comma separated)" class="feature-input">
            </div>
            <div class="form-group">
                <textarea name="table_data_${tableId}" rows="4" placeholder="Data (one row per line, comma separated)" class="feature-textarea"></textarea>
            </div>
        </div>
    `;
    
    section.insertAdjacentHTML('beforeend', tableHtml);
}

// Add chart functionality
function addChart(sectionName) {
    const section = document.querySelector(`[data-section="${sectionName}"]`);
    if (!section) return;
    
    const chartId = `chart_${Date.now()}`;
    const chartHtml = `
        <div class="feature-container" id="${chartId}">
            <div class="feature-header">
                <h5>📈 Chart</h5>
                <button type="button" onclick="removeFeature('${chartId}')" class="remove-btn">✕</button>
            </div>
            <div class="form-group">
                <select name="chart_type_${chartId}" class="feature-input">
                    <option value="bar">Bar Chart</option>
                    <option value="pie">Pie Chart</option>
                    <option value="line">Line Chart</option>
                </select>
            </div>
            <div class="form-group">
                <input type="text" name="chart_title_${chartId}" placeholder="Chart Title" class="feature-input">
            </div>
            <div class="form-group">
                <input type="text" name="chart_labels_${chartId}" placeholder="Labels (comma separated)" class="feature-input">
            </div>
            <div class="form-group">
                <input type="text" name="chart_values_${chartId}" placeholder="Values (comma separated)" class="feature-input">
            </div>
        </div>
    `;
    
    section.insertAdjacentHTML('beforeend', chartHtml);
}

// Add code block functionality
function addCodeBlock(sectionName) {
    const section = document.querySelector(`[data-section="${sectionName}"]`);
    if (!section) return;
    
    const codeId = `code_${Date.now()}`;
    const codeHtml = `
        <div class="feature-container" id="${codeId}">
            <div class="feature-header">
                <h5>💻 Code Block</h5>
                <button type="button" onclick="removeFeature('${codeId}')" class="remove-btn">✕</button>
            </div>
            <div class="form-group">
                <select name="code_language_${codeId}" class="feature-input">
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="java">Java</option>
                    <option value="cpp">C++</option>
                    <option value="html">HTML</option>
                    <option value="css">CSS</option>
                    <option value="sql">SQL</option>
                    <option value="text">Text</option>
                </select>
            </div>
            <div class="form-group">
                <textarea name="code_content_${codeId}" rows="6" placeholder="Enter your code here..." class="feature-textarea"></textarea>
            </div>
        </div>
    `;
    
    section.insertAdjacentHTML('beforeend', codeHtml);
}

// Remove feature
function removeFeature(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}

async function handleSubmit(event) {
    event.preventDefault();
    console.log('Form submission started');
    
    try {
        // Show loading state
        const submitButton = event.target.querySelector('button[type="submit"]');
        if (!submitButton) {
            throw new Error('Submit button not found');
        }
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Generating...';
        submitButton.disabled = true;
        
        // Collect form data
        const formData = new FormData(event.target);
        const data = {
            user_data: {
                student_name: formData.get('student_name'),
                college_name: formData.get('college_name'),
                class: formData.get('class'),
                roll_number: formData.get('roll_number'),
                subject: formData.get('subject'),
                subject_teacher: formData.get('subject_teacher'),
                assignment_topic: formData.get('assignment_topic'),
                project_date: formData.get('project_date'),
                submission_date: formData.get('submission_date'),
                contact_number: formData.get('contact_number'),
                self_introduction: formData.get('self_introduction')
            },
            template: formData.get('template'),
            color_scheme: formData.get('color_scheme'),
            content: {},
            tables: {},
            charts: {},
            code_blocks: {}
        };

        // Collect content from dynamic sections
        const contentSections = document.querySelectorAll('.content-section');
        contentSections.forEach(section => {
            const sectionName = section.getAttribute('data-section');
            const textarea = section.querySelector('textarea');
            if (sectionName && textarea) {
                data.content[sectionName] = textarea.value;
            }
        });

        // Collect tables, charts, and code blocks
        const featureContainers = document.querySelectorAll('.feature-container');
        featureContainers.forEach(container => {
            const section = container.closest('.content-section');
            if (!section) return;
            
            const sectionName = section.getAttribute('data-section');
            const containerId = container.id;
            
            if (containerId.startsWith('table_')) {
                if (!data.tables[sectionName]) data.tables[sectionName] = [];
                const tableData = {
                    title: formData.get(`table_title_${containerId}`) || 'Table',
                    headers: formData.get(`table_headers_${containerId}`) || '',
                    data: formData.get(`table_data_${containerId}`) || ''
                };
                data.tables[sectionName].push(tableData);
            } else if (containerId.startsWith('chart_')) {
                if (!data.charts[sectionName]) data.charts[sectionName] = [];
                const chartData = {
                    type: formData.get(`chart_type_${containerId}`) || 'bar',
                    title: formData.get(`chart_title_${containerId}`) || 'Chart',
                    labels: formData.get(`chart_labels_${containerId}`) || '',
                    values: formData.get(`chart_values_${containerId}`) || ''
                };
                data.charts[sectionName].push(chartData);
            } else if (containerId.startsWith('code_')) {
                if (!data.code_blocks[sectionName]) data.code_blocks[sectionName] = [];
                const codeData = {
                    language: formData.get(`code_language_${containerId}`) || 'text',
                    code: formData.get(`code_content_${containerId}`) || ''
                };
                data.code_blocks[sectionName].push(codeData);
            }
        });

        console.log('Sending data to server...', data);
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to generate document');
        }

        console.log('Generating document download...');
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `DazzloDocs_${data.user_data.student_name}_${data.user_data.subject}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();

        submitButton.textContent = originalText;
        submitButton.disabled = false;
    } catch (error) {
        console.error('Error:', error);
        alert(error.message || 'An error occurred while generating the document');
        
        const submitButton = event.target.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.textContent = originalText || 'Generate Document';
            submitButton.disabled = false;
        }
    }
} 