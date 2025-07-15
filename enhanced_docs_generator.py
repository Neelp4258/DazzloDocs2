#!/usr/bin/env python3
"""
Enhanced DazzloDocs - Professional Document Generator for Birla College Students
Advanced features including charts, tables, flowcharts, and interactive elements
"""

import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white, Color
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, Flowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg before importing pyplot
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from io import BytesIO
from PIL import Image as PILImage
from datetime import datetime
import json

# Enhanced Color Schemes
COLOR_SCHEMES = {
    "Classic Blue": {
        "primary": "#1e40af",
        "secondary": "#3b82f6",
        "accent": "#60a5fa",
        "text": "#1f2937",
        "background": "#f8fafc",
        "highlight": "#dbeafe"
    },
    "Royal Professional": {
        "primary": "#1e3a8a",  # Deep blue
        "secondary": "#dc2626",  # Red
        "accent": "#4f46e5",    # Indigo
        "text": "#111827",      # Almost black
        "background": "#f9fafb",
        "highlight": "#e5e7eb"
    },
    "Modern Elegance": {
        "primary": "#7c3aed",   # Vibrant purple
        "secondary": "#059669",  # Green
        "accent": "#2563eb",    # Blue
        "text": "#1f2937",
        "background": "#f3f4f6",
        "highlight": "#e5e7eb"
    },
    "Corporate Trust": {
        "primary": "#0369a1",   # Professional blue
        "secondary": "#b91c1c",  # Dark red
        "accent": "#1d4ed8",    # Royal blue
        "text": "#111827",
        "background": "#f8fafc",
        "highlight": "#dbeafe"
    },
    "Creative Professional": {
        "primary": "#4338ca",   # Indigo
        "secondary": "#ea580c",  # Orange
        "accent": "#0891b2",    # Cyan
        "text": "#1f2937",
        "background": "#f8fafc",
        "highlight": "#e0f2fe"
    },
    "Executive Impact": {
        "primary": "#312e81",   # Deep indigo
        "secondary": "#be123c",  # Rose
        "accent": "#047857",    # Emerald
        "text": "#1f2937",
        "background": "#f9fafb",
        "highlight": "#f1f5f9"
    }
}

# Enhanced Templates with Advanced Features - Birla College Focused
TEMPLATES = {
    "assignment": {
        "name": "Academic Assignment",
        "sections": ["introduction", "main_content", "analysis", "conclusion", "references"],
        "features": ["tables", "charts", "citations", "references", "code_blocks"],
        "description": "Standard academic assignment with proper formatting and analysis"
    },
    "project_report": {
        "name": "Project Report",
        "sections": ["project_overview", "objectives", "methodology", "implementation", "results", "conclusion", "appendix"],
        "features": ["flowcharts", "tables", "timelines", "charts", "gantt_charts", "code_blocks"],
        "description": "Comprehensive project report with visual elements and analysis"
    },
    "case_study": {
        "name": "Case Study Analysis",
        "sections": ["case_overview", "problem_analysis", "solutions", "implementation", "results", "recommendations"],
        "features": ["charts", "tables", "decision_trees", "swot_analysis", "comparison_tables"],
        "description": "In-depth case study analysis with solutions and visual aids"
    },
    "research_paper": {
        "name": "Research Paper",
        "sections": ["abstract", "introduction", "literature_review", "methodology", "results", "discussion", "conclusion", "references"],
        "features": ["tables", "charts", "citations", "references", "flowcharts", "code_blocks"],
        "description": "Academic research paper with proper formatting and citations"
    },
    "presentation_report": {
        "name": "Presentation Report",
        "sections": ["executive_summary", "key_points", "analysis", "findings", "recommendations"],
        "features": ["charts", "tables", "bullet_points", "highlighted_text"],
        "description": "Professional presentation report with key insights and recommendations"
    },
    "lab_report": {
        "name": "Laboratory Report",
        "sections": ["objective", "materials", "procedure", "observations", "calculations", "results", "conclusion"],
        "features": ["tables", "charts", "formulas", "data_analysis", "graphs"],
        "description": "Scientific laboratory report with data analysis and observations"
    },
    "business_plan": {
        "name": "Business Plan",
        "sections": ["executive_summary", "business_overview", "market_analysis", "strategy", "financial_plan", "implementation"],
        "features": ["charts", "tables", "financial_projections", "market_charts", "timelines"],
        "description": "Comprehensive business plan with financial analysis and market research"
    },
    "technical_documentation": {
        "name": "Technical Documentation",
        "sections": ["system_overview", "architecture", "implementation", "testing", "deployment", "maintenance"],
        "features": ["flowcharts", "diagrams", "code_blocks", "tables", "system_architecture"],
        "description": "Technical documentation with system diagrams and code examples"
    }
}

class ChartMaker:
    def __init__(self, colors):
        self.colors = colors
        plt.style.use('default')
    
    def create_bar_chart(self, data, labels, title, xlabel="Categories", ylabel="Values"):
        """Create a professional bar chart"""
        plt.figure(figsize=(10, 6))
        bars = plt.bar(labels, data, 
                      color=[self.colors['primary'], self.colors['secondary'], 
                            self.colors['accent'], self.colors['highlight']])
        
        plt.title(title, fontsize=14, pad=20, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + max(data)*0.01,
                    f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        
        return buffer
    
    def create_pie_chart(self, data, labels, title):
        """Create a professional pie chart"""
        plt.figure(figsize=(8, 6))
        colors = [self.colors['primary'], self.colors['secondary'],
                 self.colors['accent'], self.colors['highlight']]
        
        wedges, texts, autotexts = plt.pie(data, labels=labels, autopct='%1.1f%%',
                                          colors=colors, startangle=90)
        
        plt.title(title, fontsize=14, pad=20, fontweight='bold')
        
        # Enhance text appearance
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        
        return buffer
    
    def create_line_chart(self, x_data, y_data, title, xlabel="X Axis", ylabel="Y Axis"):
        """Create a professional line chart"""
        plt.figure(figsize=(10, 6))
        plt.plot(x_data, y_data, marker='o', linewidth=2, markersize=8,
                color=self.colors['primary'])
        
        plt.title(title, fontsize=14, pad=20, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        
        return buffer
    
    def create_scatter_plot(self, x_data, y_data, title, xlabel="X Axis", ylabel="Y Axis"):
        """Create a professional scatter plot"""
        plt.figure(figsize=(10, 6))
        plt.scatter(x_data, y_data, c=self.colors['primary'], alpha=0.7, s=100)
        
        plt.title(title, fontsize=14, pad=20, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        
        return buffer

class FlowchartMaker:
    def __init__(self, colors):
        self.colors = colors
    
    def create_flowchart(self, nodes, edges, title):
        """Create a professional flowchart"""
        plt.figure(figsize=(12, 8))
        G = nx.DiGraph()
        G.add_edges_from(edges)
        
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos,
                             node_color=self.colors['accent'],
                             node_size=3000,
                             alpha=0.9,
                             edgecolors=self.colors['primary'],
                             linewidths=2)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos,
                             edge_color=self.colors['primary'],
                             arrows=True,
                             arrowsize=20,
                             arrowstyle='->',
                             width=2)
        
        # Add labels
        nx.draw_networkx_labels(G, pos,
                              labels=dict(zip(G.nodes(), nodes)),
                              font_size=10,
                              font_weight='bold',
                              font_color='white')
        
        plt.title(title, fontsize=16, pad=20, fontweight='bold')
        plt.axis('off')
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        
        return buffer

class TableMaker:
    def __init__(self, colors):
        self.colors = colors
    
    def create_table(self, data, colWidths=None, style=None):
        """Create a professionally formatted table"""
        if not colWidths:
            colWidths = [2*inch] * len(data[0])
        
        table = Table(data, colWidths=colWidths)
        
        if not style:
            style = TableStyle([
                # Header styling
                ('BACKGROUND', (0, 0), (-1, 0), HexColor(self.colors['primary'])),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                
                # Content styling
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                
                # Borders and spacing
                ('GRID', (0, 0), (-1, -1), 1, HexColor(self.colors['secondary'])),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                
                # Alternating row colors
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), 
                 [HexColor(self.colors['background']), HexColor(self.colors['highlight'])])
            ])
        
        table.setStyle(style)
        return table
    
    def create_financial_table(self, data, title):
        """Create a financial table with currency formatting"""
        # Add currency formatting
        formatted_data = []
        for row in data:
            formatted_row = []
            for cell in row:
                if isinstance(cell, (int, float)) and cell != 0:
                    formatted_row.append(f"${cell:,.2f}")
                else:
                    formatted_row.append(str(cell))
            formatted_data.append(formatted_row)
        
        return self.create_table(formatted_data)

class CodeBlockMaker:
    def __init__(self, colors):
        self.colors = colors
    
    def create_code_block(self, code, language="python"):
        """Create a formatted code block"""
        code_style = ParagraphStyle(
            'CodeBlock',
            parent=getSampleStyleSheet()['Normal'],
            fontName='Courier',
            fontSize=9,
            leftIndent=20,
            rightIndent=20,
            backColor=HexColor(self.colors['background']),
            borderColor=HexColor(self.colors['secondary']),
            borderWidth=1,
            borderPadding=10,
            spaceAfter=12
        )
        
        return Paragraph(f"<b>{language.upper()}:</b><br/>{code}", code_style)

class EnhancedDocumentGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.user_data = {}
        self.template = None
        self.colors = None
        self.content = {}
        self.charts = {}
        self.tables = {}
        self.flowcharts = {}
        self.code_blocks = {}
        
        # Initialize tools
        self.chart_maker = None
        self.flowchart_maker = None
        self.table_maker = None
        self.code_maker = None
    
    def set_colors(self, color_scheme):
        """Set color scheme and initialize tools"""
        self.colors = COLOR_SCHEMES[color_scheme]
        self.chart_maker = ChartMaker(self.colors)
        self.flowchart_maker = FlowchartMaker(self.colors)
        self.table_maker = TableMaker(self.colors)
        self.code_maker = CodeBlockMaker(self.colors)
    
    def add_chart(self, section, chart_type, data, **kwargs):
        """Add a chart to a section"""
        if chart_type == 'bar':
            chart_buffer = self.chart_maker.create_bar_chart(**data, **kwargs)
        elif chart_type == 'pie':
            chart_buffer = self.chart_maker.create_pie_chart(**data, **kwargs)
        elif chart_type == 'line':
            chart_buffer = self.chart_maker.create_line_chart(**data, **kwargs)
        elif chart_type == 'scatter':
            chart_buffer = self.chart_maker.create_scatter_plot(**data, **kwargs)
        
        if section not in self.charts:
            self.charts[section] = []
        self.charts[section].append({
            'type': chart_type,
            'buffer': chart_buffer,
            'title': kwargs.get('title', f'{chart_type.title()} Chart')
        })
    
    def add_table(self, section, data, title="Table"):
        """Add a table to a section"""
        if section not in self.tables:
            self.tables[section] = []
        self.tables[section].append({
            'data': data,
            'title': title
        })
    
    def add_flowchart(self, section, nodes, edges, title):
        """Add a flowchart to a section"""
        if section not in self.flowcharts:
            self.flowcharts[section] = []
        flowchart_buffer = self.flowchart_maker.create_flowchart(nodes, edges, title)
        self.flowcharts[section].append({
            'buffer': flowchart_buffer,
            'title': title
        })
    
    def add_code_block(self, section, code, language="python"):
        """Add a code block to a section"""
        if section not in self.code_blocks:
            self.code_blocks[section] = []
        self.code_blocks[section].append({
            'code': code,
            'language': language
        })
    
    def create_header_footer(self, canvas, doc):
        """Create professional header and footer with Birla College branding"""
        canvas.saveState()
        width, height = A4
        
        # Draw double border
        canvas.setStrokeColor(HexColor(self.colors['border']))
        # Outer border
        canvas.rect(30, 30, width - 60, height - 60)
        # Inner border
        canvas.rect(35, 35, width - 70, height - 70)
        
        # Header with gradient effect
        canvas.setFillColor(HexColor(self.colors['primary']))
        canvas.rect(0, height - 42, width, 40, fill=1)
        
        # Add logo to header
        if os.path.exists('static/logo.png'):
            img = PILImage.open('static/logo.png')
            img_width, img_height = img.size
            aspect = img_height / float(img_width)
            canvas.drawImage('static/logo.png', 
                           50, height - 35,  # Position
                           width=25, height=25*aspect)  # Size
        
        canvas.setFont('Helvetica-Bold', 12)
        canvas.setFillColor(white)
        canvas.drawString(85, height - 27, f"BK BIRLA COLLEGE - {self.user_data.get('subject', '')}")
        
        canvas.setFont('Helvetica', 10)
        canvas.drawRightString(width - 50, height - 27, f"{self.template['name']}")
        
        # Footer
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(HexColor(self.colors['text']))
        canvas.drawString(50, 30, f"Student: {self.user_data.get('student_name', '')} | Class: {self.user_data.get('class', '')} | Roll: {self.user_data.get('roll_number', '')}")
        canvas.drawRightString(width - 50, 30, f"Page {canvas.getPageNumber()} | Generated: {datetime.now().strftime('%Y-%m-%d')}")
        
        canvas.restoreState()
    
    def create_title_page(self, story):
        """Create the classic Birla College title page with blue header and red title"""
        # Add initial spacing
        story.append(Spacer(1, inch))
        
        # College Name (Blue)
        college_style = ParagraphStyle(
            'CollegeHeader',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=HexColor('#0000FF'),  # Pure blue
            alignment=TA_CENTER,
            spaceAfter=60
        )
        story.append(Paragraph("BK BIRLA COLLEGE", college_style))
        
        # Document Title (Red)
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=HexColor('#FF0000'),  # Pure red
            alignment=TA_CENTER,
            spaceAfter=30
        )
        story.append(Paragraph(self.user_data.get('subject', '').upper(), title_style))
        
        # Assignment Topic
        if self.user_data.get('assignment_topic'):
            topic_style = ParagraphStyle(
                'TopicStyle',
                parent=self.styles['Normal'],
                fontSize=14,
                textColor=black,
                alignment=TA_LEFT,
                spaceAfter=20
            )
            story.append(Paragraph(f"Assignment Topic: {self.user_data.get('assignment_topic', '')}", topic_style))
        
        # Personal Information Table
        data = [
            ['Student Name:', self.user_data.get('student_name', '')],
            ['Class:', self.user_data.get('class', '')],
            ['Roll Number:', self.user_data.get('roll_number', '')],
            ['Subject Teacher:', self.user_data.get('subject_teacher', '')]
        ]
        
        # Add optional fields if they exist
        optional_fields = [
            ('Project Date:', 'project_date'),
            ('Submission Date:', 'submission_date'),
            ('Contact Number:', 'contact_number')
        ]
        
        for label, field in optional_fields:
            if self.user_data.get(field):
                data.append([label, self.user_data.get(field)])
        
        # Create table with proper styling
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, black)
        ]))
        
        story.append(table)
        
        # Add self introduction if provided
        if self.user_data.get('self_introduction'):
            story.append(Spacer(1, 0.5*inch))
            intro_style = ParagraphStyle(
                'IntroStyle',
                parent=self.styles['Normal'],
                fontSize=11,
                textColor=black,
                alignment=TA_JUSTIFY,
                spaceAfter=20
            )
            story.append(Paragraph("Self Introduction:", intro_style))
            story.append(Paragraph(self.user_data.get('self_introduction', ''), intro_style))
        
        story.append(PageBreak())
    
    def create_content_pages(self, story):
        """Create enhanced content pages with all features"""
        # Section name mapping for better display
        section_names = {
            'introduction': 'Introduction',
            'main_content': 'Main Content',
            'analysis': 'Analysis',
            'conclusion': 'Conclusion',
            'references': 'References',
            'project_overview': 'Project Overview',
            'objectives': 'Objectives',
            'methodology': 'Methodology',
            'implementation': 'Implementation',
            'results': 'Results',
            'appendix': 'Appendix',
            'case_overview': 'Case Overview',
            'problem_analysis': 'Problem Analysis',
            'solutions': 'Solutions',
            'recommendations': 'Recommendations',
            'abstract': 'Abstract',
            'literature_review': 'Literature Review',
            'discussion': 'Discussion',
            'executive_summary': 'Executive Summary',
            'key_points': 'Key Points',
            'findings': 'Findings',
            'objective': 'Objective',
            'materials': 'Materials',
            'procedure': 'Procedure',
            'observations': 'Observations',
            'calculations': 'Calculations',
            'business_overview': 'Business Overview',
            'market_analysis': 'Market Analysis',
            'strategy': 'Strategy',
            'financial_plan': 'Financial Plan',
            'system_overview': 'System Overview',
            'architecture': 'Architecture',
            'testing': 'Testing',
            'deployment': 'Deployment',
            'maintenance': 'Maintenance'
        }
        
        for section in self.template['sections']:
            # Section header
            section_style = ParagraphStyle(
                'SectionHeader',
                parent=self.styles['Heading2'],
                fontSize=18,
                spaceAfter=15,
                spaceBefore=25,
                textColor=HexColor(self.colors['primary']),
                fontName='Helvetica-Bold'
            )
            
            # Use mapped name or format the section name
            section_title = section_names.get(section, section.replace('_', ' ').title())
            story.append(Paragraph(section_title, section_style))
            
            # Section content with better default text
            default_content = {
                'introduction': 'This section provides an introduction to the topic and outlines the scope of the document.',
                'main_content': 'This section contains the main content and analysis of the topic.',
                'analysis': 'This section provides detailed analysis and interpretation of the data and findings.',
                'conclusion': 'This section summarizes the key findings and provides concluding remarks.',
                'references': 'List of references and sources used in this document.',
                'project_overview': 'This section provides an overview of the project, its goals, and scope.',
                'objectives': 'This section outlines the specific objectives and goals of the project.',
                'methodology': 'This section describes the methods and approaches used in the project.',
                'implementation': 'This section details the implementation process and technical details.',
                'results': 'This section presents the results and findings of the project.',
                'appendix': 'This section contains additional supporting materials and data.',
                'case_overview': 'This section provides an overview of the case study and its context.',
                'problem_analysis': 'This section analyzes the problems and challenges identified.',
                'solutions': 'This section presents proposed solutions and approaches.',
                'recommendations': 'This section provides recommendations and next steps.',
                'abstract': 'This section provides a concise summary of the research and findings.',
                'literature_review': 'This section reviews relevant literature and previous research.',
                'discussion': 'This section discusses the implications and significance of the findings.',
                'executive_summary': 'This section provides a high-level summary for executives.',
                'key_points': 'This section highlights the key points and main takeaways.',
                'findings': 'This section presents the main findings and discoveries.',
                'objective': 'This section states the objective and purpose of the experiment.',
                'materials': 'This section lists the materials and equipment used.',
                'procedure': 'This section describes the experimental procedure and methodology.',
                'observations': 'This section records the observations and data collected.',
                'calculations': 'This section shows the calculations and data analysis.',
                'business_overview': 'This section provides an overview of the business concept.',
                'market_analysis': 'This section analyzes the market and competitive landscape.',
                'strategy': 'This section outlines the business strategy and approach.',
                'financial_plan': 'This section presents the financial projections and plan.',
                'system_overview': 'This section provides an overview of the system architecture.',
                'architecture': 'This section describes the system architecture and design.',
                'testing': 'This section details the testing approach and results.',
                'deployment': 'This section describes the deployment process and requirements.',
                'maintenance': 'This section outlines the maintenance and support requirements.'
            }
            
            content = self.content.get(section, default_content.get(section, f"Content for {section_title} section."))
            
            # Split content into paragraphs
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    para_style = ParagraphStyle(
                        'Content',
                        parent=self.styles['Normal'],
                        fontSize=11,
                        spaceAfter=10,
                        alignment=TA_JUSTIFY,
                        leading=14
                    )
                    story.append(Paragraph(para.strip(), para_style))
            
            # Add charts for this section
            if section in self.charts:
                for chart in self.charts[section]:
                    story.append(Spacer(1, 15))
                    chart_title_style = ParagraphStyle(
                        'ChartTitle',
                        parent=self.styles['Normal'],
                        fontSize=12,
                        alignment=TA_CENTER,
                        textColor=HexColor(self.colors['secondary']),
                        fontName='Helvetica-Bold'
                    )
                    story.append(Paragraph(chart['title'], chart_title_style))
                    story.append(Spacer(1, 5))
                    
                    img = Image(chart['buffer'], width=6*inch, height=3.5*inch)
                    story.append(img)
            
            # Add tables for this section
            if section in self.tables:
                for table_data in self.tables[section]:
                    story.append(Spacer(1, 15))
                    table_title_style = ParagraphStyle(
                        'TableTitle',
                        parent=self.styles['Normal'],
                        fontSize=12,
                        alignment=TA_CENTER,
                        textColor=HexColor(self.colors['secondary']),
                        fontName='Helvetica-Bold'
                    )
                    story.append(Paragraph(table_data['title'], table_title_style))
                    story.append(Spacer(1, 5))
                    
                    table = self.table_maker.create_table(table_data['data'])
                    story.append(table)
            
            # Add flowcharts for this section
            if section in self.flowcharts:
                for flowchart in self.flowcharts[section]:
                    story.append(Spacer(1, 15))
                    flowchart_title_style = ParagraphStyle(
                        'FlowchartTitle',
                        parent=self.styles['Normal'],
                        fontSize=12,
                        alignment=TA_CENTER,
                        textColor=HexColor(self.colors['secondary']),
                        fontName='Helvetica-Bold'
                    )
                    story.append(Paragraph(flowchart['title'], flowchart_title_style))
                    story.append(Spacer(1, 5))
                    
                    img = Image(flowchart['buffer'], width=6*inch, height=4*inch)
                    story.append(img)
            
            # Add code blocks for this section
            if section in self.code_blocks:
                for code_block in self.code_blocks[section]:
                    story.append(Spacer(1, 15))
                    code_element = self.code_maker.create_code_block(
                        code_block['code'], 
                        code_block['language']
                    )
                    story.append(code_element)
            
            story.append(Spacer(1, 20))
    
    def generate_pdf(self, output=None):
        """Generate the enhanced PDF document"""
        if output is None:
            output = f"DazzloDocs_{self.user_data.get('student_name', 'Student')}_{self.user_data.get('subject', 'Document')}.pdf"
        
        # Handle BytesIO output
        if hasattr(output, 'write'):
            doc = SimpleDocTemplate(
                output,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
        else:
            doc = SimpleDocTemplate(
                output,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
        
        story = []
        
        # Create title page
        self.create_title_page(story)
        
        # Create content pages
        self.create_content_pages(story)
        
        # Build PDF
        doc.build(story, onFirstPage=self.create_header_footer, onLaterPages=self.create_header_footer)
        
        return output

    def add_document_content(self, story):
        """Add the main document content with sections"""
        # Section Title Style
        section_title_style = ParagraphStyle(
            'SectionTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=HexColor(self.colors['primary']),
            spaceBefore=20,
            spaceAfter=10
        )

        # Content Style
        content_style = ParagraphStyle(
            'Content',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=HexColor(self.colors['text']),
            alignment=TA_JUSTIFY,
            spaceAfter=10
        )

        # Add each section from the template
        for section in self.template.get('sections', []):
            # Add section title
            title = section.replace('_', ' ').title()
            story.append(Paragraph(title, section_title_style))
            
            # Add section content from user_data if available
            content_key = f"{section}_content"
            if content_key in self.user_data:
                story.append(Paragraph(self.user_data[content_key], content_style))
            
            # Add charts if specified for this section
            if 'charts' in self.template.get('features', []) and f"{section}_chart" in self.user_data:
                self.add_chart(story, section)
            
            # Add tables if specified for this section
            if 'tables' in self.template.get('features', []) and f"{section}_table" in self.user_data:
                self.add_table(story, section)
            
            story.append(Spacer(1, 0.2*inch))

    def add_chart(self, story, section):
        """Add a chart to the document"""
        chart_data = self.user_data.get(f"{section}_chart")
        if not chart_data:
            return

        # Create figure with matplotlib
        plt.figure(figsize=(8, 5))
        
        chart_type = chart_data.get('type', 'bar')
        data = chart_data.get('data', {})
        
        if chart_type == 'bar':
            plt.bar(data.get('labels', []), data.get('values', []))
        elif chart_type == 'line':
            plt.plot(data.get('labels', []), data.get('values', []))
        elif chart_type == 'pie':
            plt.pie(data.get('values', []), labels=data.get('labels', []))
        
        plt.title(chart_data.get('title', ''))
        plt.xlabel(chart_data.get('xlabel', ''))
        plt.ylabel(chart_data.get('ylabel', ''))
        
        # Save chart to buffer
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight')
        img_buffer.seek(0)
        
        # Add chart to document
        img = Image(img_buffer)
        img.drawHeight = 4*inch
        img.drawWidth = 6*inch
        story.append(img)
        plt.close()

    def generate(self):
        """Generate the complete document"""
        story = []
        
        # Create title page
        self.create_title_page(story)
        
        # Add document content
        self.add_document_content(story)
        
        # Generate PDF
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build document with header/footer
        doc.build(story, onFirstPage=self.create_header_footer, onLaterPages=self.create_header_footer)

# Export the classes and data for use in the web application
__all__ = ['EnhancedDocumentGenerator', 'COLOR_SCHEMES', 'TEMPLATES', 'ChartMaker', 'FlowchartMaker', 'TableMaker', 'CodeBlockMaker'] 