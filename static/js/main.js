// Global variables to store templates and features
let templates = {};
let colorSchemes = {};
let chartTypes = [];
let codeLanguages = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Set up form handler first
        const form = document.getElementById('documentForm');
        if (!form) {
            console.error('Document form not found!');
            return;
        }
        form.addEventListener('submit', handleSubmit);
        console.log('Form handler attached successfully');

        // Load all required data
        await Promise.all([
            loadTemplates(),
            loadColorSchemes(),
            loadChartTypes(),
            loadCodeLanguages()
        ]);
        console.log('All data loaded successfully');

        // Initialize the first template's sections
        const templateSelect = document.getElementById('template');
        if (templateSelect && templateSelect.value) {
            updateContentSections();
        }
    } catch (error) {
        console.error('Error during initialization:', error);
        alert('Error initializing the application. Please refresh the page.');
    }
});

// Load data from API
async function loadTemplates() {
    try {
        const response = await fetch('/api/templates');
        templates = await response.json();
        populateTemplateSelect();
    } catch (error) {
        console.error('Error loading templates:', error);
    }
}

async function loadColorSchemes() {
    try {
        const response = await fetch('/api/color-schemes');
        colorSchemes = await response.json();
        populateColorSchemeSelect();
    } catch (error) {
        console.error('Error loading color schemes:', error);
    }
}

async function loadChartTypes() {
    try {
        const response = await fetch('/api/chart-types');
        chartTypes = await response.json();
    } catch (error) {
        console.error('Error loading chart types:', error);
    }
}

async function loadCodeLanguages() {
    try {
        const response = await fetch('/api/code-languages');
        codeLanguages = await response.json();
    } catch (error) {
        console.error('Error loading code languages:', error);
    }
}

// Populate select elements
function populateTemplateSelect() {
    const select = document.getElementById('template');
    if (!select) return;

    // Clear existing options
    select.innerHTML = '<option value="">Select a template...</option>';

    // Add new options
    Object.entries(templates).forEach(([key, template]) => {
        const option = document.createElement('option');
        option.value = key;
        option.textContent = template.name;
        select.appendChild(option);
    });

    // Add change event listener
    select.addEventListener('change', updateContentSections);
}

function populateColorSchemeSelect() {
    const select = document.getElementById('color_scheme');
    if (!select) return;

    // Clear existing options
    select.innerHTML = '<option value="">Select a color scheme...</option>';

    // Add new options
    Object.entries(colorSchemes).forEach(([key, scheme]) => {
        const option = document.createElement('option');
        option.value = key;
        option.textContent = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        select.appendChild(option);
    });
}

// Update content sections based on template
function updateContentSections() {
    const templateKey = document.getElementById('template').value;
    if (!templateKey || !templates[templateKey]) return;

    const template = templates[templateKey];
    const contentSection = document.getElementById('contentSections');
    if (!contentSection) return;
    
    // Clear existing content sections
    const sectionsContainer = contentSection.querySelector('.template-sections');
    if (!sectionsContainer) {
        contentSection.innerHTML = `
            <h3>Document Content</h3>
            <div class="template-sections"></div>
            <button type="button" class="add-section-btn" onclick="addContentSection()">Add Custom Section</button>
        `;
    } else {
        sectionsContainer.innerHTML = '';
    }
    
    // Get the sections container again after potential recreation
    const container = contentSection.querySelector('.template-sections');
    
    // Add each section from the template
    template.sections.forEach(section => {
        const sectionDiv = document.createElement('div');
        sectionDiv.className = 'content-section';
        
        // Convert section name to display format
        const displayName = section.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        
        sectionDiv.innerHTML = `
            <h4>${displayName}</h4>
            <div class="form-group">
                <textarea name="${section}_content" rows="6" placeholder="Enter ${displayName} content..." class="content-textarea"></textarea>
            </div>
            <div class="section-tools">
                <button type="button" onclick="addTableToSection('${section}')" class="tool-btn">Add Table</button>
                <button type="button" onclick="addChartToSection('${section}')" class="tool-btn">Add Chart</button>
                <button type="button" onclick="addCodeBlockToSection('${section}')" class="tool-btn">Add Code Block</button>
            </div>
        `;
        
        container.appendChild(sectionDiv);
    });
}

function createContentSection(section) {
    const div = document.createElement('div');
    div.className = 'content-section';
    
    const title = section.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    
    div.innerHTML = `
        <h4>${title}</h4>
        <div class="form-group">
            <textarea name="${section}_content" rows="6" placeholder="Enter ${title} content..." class="content-textarea"></textarea>
        </div>
        <div class="section-tools">
            <button type="button" onclick="addColumnToSection('${section}')" class="tool-btn">Add Column</button>
            <button type="button" onclick="addTableToSection('${section}')" class="tool-btn">Add Table</button>
            <button type="button" onclick="addChartToSection('${section}')" class="tool-btn">Add Chart</button>
        </div>
    `;
    
    return div;
}

function addColumnToSection(sectionId) {
    const section = document.querySelector(`[name="${sectionId}_content"]`).closest('.content-section');
    const columnId = Date.now();
    
    const columnDiv = document.createElement('div');
    columnDiv.className = 'column-container';
    columnDiv.id = `column_${columnId}`;
    
    columnDiv.innerHTML = `
        <div class="feature-header">
            <h5>Column</h5>
            <button type="button" class="remove-feature" onclick="removeFeature('column_${columnId}')">Remove</button>
        </div>
        <div class="form-group">
            <input type="text" name="column_header_${columnId}" placeholder="Column Header">
            <textarea name="column_content_${columnId}" rows="4" placeholder="Column content..."></textarea>
        </div>
    `;
    
    section.appendChild(columnDiv);
}

function addTableToSection(sectionId) {
    const section = document.querySelector(`[name="${sectionId}_content"]`).closest('.content-section');
    const tableId = Date.now();
    
    const tableDiv = document.createElement('div');
    tableDiv.className = 'table-container';
    tableDiv.id = `table_${tableId}`;
    
    tableDiv.innerHTML = `
        <div class="feature-header">
            <h5>Table</h5>
            <button type="button" class="remove-feature" onclick="removeFeature('table_${tableId}')">Remove</button>
        </div>
        <div class="form-group">
            <input type="text" name="table_title_${tableId}" placeholder="Table Title" class="feature-input">
            <input type="text" name="table_headers_${tableId}" placeholder="Column Headers (comma-separated)" class="feature-input">
            <textarea name="table_data_${tableId}" rows="4" placeholder="Data (one row per line, columns comma-separated)" class="feature-textarea"></textarea>
        </div>
    `;
    
    section.appendChild(tableDiv);
}

function addChartToSection(sectionId) {
    const section = document.querySelector(`[name="${sectionId}_content"]`).closest('.content-section');
    const chartId = Date.now();
    
    const chartDiv = document.createElement('div');
    chartDiv.className = 'chart-container';
    chartDiv.id = `chart_${chartId}`;
    
    chartDiv.innerHTML = `
        <div class="feature-header">
            <h5>Chart</h5>
            <button type="button" class="remove-feature" onclick="removeFeature('chart_${chartId}')">Remove</button>
        </div>
        <div class="form-group">
            <select name="chart_type_${chartId}" class="feature-input">
                ${chartTypes.map(type => `<option value="${type}">${type}</option>`).join('')}
            </select>
            <input type="text" name="chart_title_${chartId}" placeholder="Chart Title" class="feature-input">
            <input type="text" name="chart_labels_${chartId}" placeholder="Labels (comma-separated)" class="feature-input">
            <input type="text" name="chart_values_${chartId}" placeholder="Values (comma-separated)" class="feature-input">
        </div>
    `;
    
    section.appendChild(chartDiv);
}

function addCodeBlockToSection(sectionId) {
    const section = document.querySelector(`[name="${sectionId}_content"]`).closest('.content-section');
    const codeId = Date.now();
    
    const codeDiv = document.createElement('div');
    codeDiv.className = 'code-container';
    codeDiv.id = `code_${codeId}`;
    
    codeDiv.innerHTML = `
        <div class="feature-header">
            <h5>Code Block</h5>
            <button type="button" class="remove-feature" onclick="removeFeature('code_${codeId}')">Remove</button>
        </div>
        <div class="form-group">
            <select name="code_language_${codeId}" class="feature-input">
                ${codeLanguages.map(lang => `<option value="${lang}">${lang}</option>`).join('')}
            </select>
            <textarea name="code_content_${codeId}" rows="6" placeholder="Enter your code here..." class="feature-textarea"></textarea>
        </div>
    `;
    
    section.appendChild(codeDiv);
}

// Advanced Features
function addChart() {
    const container = document.getElementById('advancedFeatures');
    const chartId = Date.now();
    
    const chartDiv = document.createElement('div');
    chartDiv.className = 'feature-container';
    chartDiv.id = `chart_${chartId}`;
    
    chartDiv.innerHTML = `
        <div class="feature-header">
            <h4>Chart</h4>
            <button type="button" class="remove-feature" onclick="removeFeature('chart_${chartId}')">Remove</button>
        </div>
        <div class="form-group">
            <label>Chart Type</label>
            <select name="chart_type_${chartId}">
                ${chartTypes.map(type => `<option value="${type}">${type}</option>`).join('')}
            </select>
        </div>
        <div class="form-group">
            <label>Title</label>
            <input type="text" name="chart_title_${chartId}" placeholder="Chart title">
        </div>
        <div class="form-group">
            <label>Data Labels (comma-separated)</label>
            <input type="text" name="chart_labels_${chartId}" placeholder="Label 1, Label 2, Label 3">
        </div>
        <div class="form-group">
            <label>Data Values (comma-separated)</label>
            <input type="text" name="chart_values_${chartId}" placeholder="10, 20, 30">
        </div>
    `;
    
    container.appendChild(chartDiv);
}

function addTable() {
    const container = document.getElementById('advancedFeatures');
    const tableId = Date.now();
    
    const tableDiv = document.createElement('div');
    tableDiv.className = 'feature-container';
    tableDiv.id = `table_${tableId}`;
    
    tableDiv.innerHTML = `
        <div class="feature-header">
            <h4>Table</h4>
            <button type="button" class="remove-feature" onclick="removeFeature('table_${tableId}')">Remove</button>
        </div>
        <div class="form-group">
            <label>Title</label>
            <input type="text" name="table_title_${tableId}" placeholder="Table title">
        </div>
        <div class="form-group">
            <label>Headers (comma-separated)</label>
            <input type="text" name="table_headers_${tableId}" placeholder="Column 1, Column 2, Column 3">
        </div>
        <div class="form-group">
            <label>Data (one row per line, columns comma-separated)</label>
            <textarea name="table_data_${tableId}" rows="4" placeholder="Data 1, Data 2, Data 3&#10;Data 4, Data 5, Data 6"></textarea>
        </div>
    `;
    
    container.appendChild(tableDiv);
}

function addCodeBlock() {
    const container = document.getElementById('advancedFeatures');
    const codeId = Date.now();
    
    const codeDiv = document.createElement('div');
    codeDiv.className = 'feature-container';
    codeDiv.id = `code_${codeId}`;
    
    codeDiv.innerHTML = `
        <div class="feature-header">
            <h4>Code Block</h4>
            <button type="button" class="remove-feature" onclick="removeFeature('code_${codeId}')">Remove</button>
        </div>
        <div class="form-group">
            <label>Language</label>
            <select name="code_language_${codeId}">
                ${codeLanguages.map(lang => `<option value="${lang}">${lang}</option>`).join('')}
            </select>
        </div>
        <div class="form-group">
            <label>Code</label>
            <textarea name="code_content_${codeId}" rows="6" placeholder="Enter your code here..."></textarea>
        </div>
    `;
    
    container.appendChild(codeDiv);
}

function addContentSection() {
    const container = document.getElementById('contentSections');
    const sectionId = Date.now();
    
    const sectionDiv = document.createElement('div');
    sectionDiv.className = 'content-section';
    sectionDiv.id = `section_${sectionId}`;
    
    sectionDiv.innerHTML = `
        <div class="feature-header">
            <input type="text" name="section_header_${sectionId}" placeholder="Enter Section Header..." class="section-header-input">
            <button type="button" class="remove-feature" onclick="removeFeature('section_${sectionId}')">Remove</button>
        </div>
        <div class="form-group">
            <textarea name="section_content_${sectionId}" rows="6" placeholder="Enter your content here..."></textarea>
        </div>
    `;
    
    container.appendChild(sectionDiv);
}

function removeFeature(id) {
    document.getElementById(id).remove();
}

// Form submission
function setupFormHandlers() {
    const form = document.getElementById('documentForm');
    form.addEventListener('submit', handleSubmit);
}

async function handleSubmit(event) {
    event.preventDefault();
    console.log('Form submission started');
    
    try {
        // Show loading state
        const submitButton = event.target.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Generating...';
        submitButton.disabled = true;
        
        // Collect form data
        const formData = new FormData(event.target);
        const data = {
            user_data: {
                student_name: formData.get('student_name'),
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

        console.log('Collecting content sections...');
        // Collect content sections
        document.querySelectorAll('.content-section').forEach(section => {
            const textarea = section.querySelector('textarea[name$="_content"]');
            if (textarea) {
                const sectionName = textarea.name.replace('_content', '');
                data.content[sectionName] = textarea.value;

                // Collect tables in this section
                const tables = section.querySelectorAll('.table-container');
                if (tables.length > 0) {
                    if (!data.tables[sectionName]) {
                        data.tables[sectionName] = [];
                    }
                    tables.forEach(tableContainer => {
                        const tableId = tableContainer.id.replace('table_', '');
                        const title = formData.get(`table_title_${tableId}`) || 'Table';
                        const headersStr = formData.get(`table_headers_${tableId}`) || '';
                        const rawData = formData.get(`table_data_${tableId}`) || '';
                        
                        if (headersStr && rawData) {
                            const headers = headersStr.split(',').map(h => h.trim());
                            const rows = rawData.split('\n')
                                .map(row => row.split(',').map(cell => cell.trim()))
                                .filter(row => row.length === headers.length && row.some(cell => cell));
                            
                            // Combine headers and data
                            const tableData = [headers, ...rows];
                            
                            data.tables[sectionName].push({
                                title: title,
                                data: tableData
                            });
                        }
                    });
                }

                // Collect charts in this section
                const charts = section.querySelectorAll('.chart-container');
                if (charts.length > 0) {
                    if (!data.charts[sectionName]) {
                        data.charts[sectionName] = [];
                    }
                    charts.forEach(chartContainer => {
                        const chartId = chartContainer.id.replace('chart_', '');
                        const type = formData.get(`chart_type_${chartId}`);
                        const title = formData.get(`chart_title_${chartId}`) || 'Chart';
                        const labelsStr = formData.get(`chart_labels_${chartId}`) || '';
                        const valuesStr = formData.get(`chart_values_${chartId}`) || '';
                        
                        if (type && labelsStr && valuesStr) {
                            const labels = labelsStr.split(',').map(l => l.trim());
                            const values = valuesStr.split(',').map(v => parseFloat(v.trim())).filter(v => !isNaN(v));
                            
                            data.charts[sectionName].push({
                                type: type,
                                title: title,
                                data: {
                                    labels: labels,
                                    values: values
                                }
                            });
                        }
                    });
                }

                // Collect code blocks in this section
                const codeBlocks = section.querySelectorAll('.code-container');
                if (codeBlocks.length > 0) {
                    if (!data.code_blocks[sectionName]) {
                        data.code_blocks[sectionName] = [];
                    }
                    codeBlocks.forEach(codeContainer => {
                        const codeId = codeContainer.id.replace('code_', '');
                        const language = formData.get(`code_language_${codeId}`) || 'text';
                        const code = formData.get(`code_content_${codeId}`) || '';
                        
                        if (code.trim()) {
                            data.code_blocks[sectionName].push({
                                language: language,
                                code: code
                            });
                        }
                    });
                }
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

        console.log('Server response received:', response.status);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to generate document');
        }

        // Handle successful response
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
        
        // Reset button state
        submitButton.textContent = originalText;
        submitButton.disabled = false;
        
        console.log('Document generation completed successfully');
    } catch (error) {
        console.error('Error during document generation:', error);
        alert('Error generating document: ' + error.message);
        
        // Reset button state
        const submitButton = event.target.querySelector('button[type="submit"]');
        submitButton.textContent = 'Generate Document';
        submitButton.disabled = false;
    }
} 