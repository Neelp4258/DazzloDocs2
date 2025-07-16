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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, Flowable, PageTemplate, Frame
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

# Professional Color Schemes
COLOR_SCHEMES = {
    "professional": {
        "primary": "#2C3E50",      # Dark blue-gray
        "secondary": "#34495E",     # Medium blue-gray
        "accent": "#3498DB",        # Light blue
        "highlight": "#ECF0F1",     # Light gray
        "background": "#FFFFFF",    # White
        "text": "#2C3E50",          # Dark text
        "border": "#BDC3C7"         # Light gray border
    },
    "modern": {
        "primary": "#34495E",       # Slate gray
        "secondary": "#5D6D7E",     # Medium gray
        "accent": "#85929E",        # Light gray
        "highlight": "#F8F9F9",     # Very light gray
        "background": "#FFFFFF",    # White
        "text": "#2C3E50",          # Dark text
        "border": "#D5DBDB"         # Light border
    },
    "classic": {
        "primary": "#2E4053",       # Dark navy
        "secondary": "#566573",     # Medium gray
        "accent": "#7F8C8D",        # Light gray
        "highlight": "#F4F6F6",     # Very light gray
        "background": "#FFFFFF",    # White
        "text": "#2C3E50",          # Dark text
        "border": "#BDC3C7"         # Light border
    },
    "elegant": {
        "primary": "#4A5568",       # Charcoal gray
        "secondary": "#718096",     # Medium gray
        "accent": "#A0AEC0",        # Light gray
        "highlight": "#F7FAFC",     # Very light gray
        "background": "#FFFFFF",    # White
        "text": "#2D3748",          # Dark text
        "border": "#E2E8F0"         # Light border
    },
    "tech_blue": {
        "primary": "#00d4ff",       # Bright cyan
        "secondary": "#0099cc",     # Medium cyan
        "accent": "#66e6ff",        # Light cyan
        "highlight": "#e6f9ff",     # Very light cyan
        "background": "#FFFFFF",    # White
        "text": "#003366",          # Dark blue text
        "border": "#b3e6ff"         # Light cyan border
    },
    "cyber_purple": {
        "primary": "#7c3aed",       # Bright purple
        "secondary": "#5b21b6",     # Medium purple
        "accent": "#a855f7",        # Light purple
        "highlight": "#f3e8ff",     # Very light purple
        "background": "#FFFFFF",    # White
        "text": "#2e1065",          # Dark purple text
        "border": "#c4b5fd"         # Light purple border
    },
    "neon_green": {
        "primary": "#10b981",       # Bright green
        "secondary": "#059669",     # Medium green
        "accent": "#34d399",        # Light green
        "highlight": "#ecfdf5",     # Very light green
        "background": "#FFFFFF",    # White
        "text": "#064e3b",          # Dark green text
        "border": "#6ee7b7"         # Light green border
    },
    "sunset_orange": {
        "primary": "#f59e0b",       # Bright orange
        "secondary": "#d97706",     # Medium orange
        "accent": "#fbbf24",        # Light orange
        "highlight": "#fffbeb",     # Very light orange
        "background": "#FFFFFF",    # White
        "text": "#78350f",          # Dark orange text
        "border": "#fcd34d"         # Light orange border
    },
    "ocean_teal": {
        "primary": "#14b8a6",       # Bright teal
        "secondary": "#0d9488",     # Medium teal
        "accent": "#5eead4",        # Light teal
        "highlight": "#f0fdfa",     # Very light teal
        "background": "#FFFFFF",    # White
        "text": "#134e4a",          # Dark teal text
        "border": "#99f6e4"         # Light teal border
    },
    "midnight_black": {
        "primary": "#1f2937",       # Dark gray
        "secondary": "#374151",     # Medium gray
        "accent": "#6b7280",        # Light gray
        "highlight": "#f9fafb",     # Very light gray
        "background": "#FFFFFF",    # White
        "text": "#111827",          # Dark text
        "border": "#d1d5db"         # Light border
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
        print("TableMaker.create_table called with data:", data)  # Debug print
        
        try:
            # Ensure data is a list of lists
            if not isinstance(data, list) or not data:
                print("Invalid or empty data, using default")  # Debug print
                data = [['No data available']]
            
            # Convert all rows to lists and all values to strings
            processed_data = []
            for row in data:
                if isinstance(row, list):
                    processed_row = [str(cell) if cell is not None else '' for cell in row]
                else:
                    processed_row = [str(row) if row is not None else '']
                processed_data.append(processed_row)
            
            data = processed_data
            
            # Ensure all rows have the same number of columns
            max_cols = max(len(row) for row in data)
            data = [row + [''] * (max_cols - len(row)) for row in data]
            
            # Set column widths
            if not colWidths or not isinstance(colWidths, list) or len(colWidths) != max_cols:
                colWidths = [2*inch] * max_cols
            
            print("Creating table with processed data:", data)  # Debug print
            table = Table(data, colWidths=colWidths)
            
            # Apply table style
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
            
        except Exception as e:
            print(f"Error in create_table: {str(e)}")  # Debug print
            # Return a simple error table
            error_table = Table([['Error creating table']], colWidths=[6*inch])
            error_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]))
            return error_table
    
    def create_financial_table(self, data, title):
        """Create a financial table with currency formatting"""
        try:
            # Ensure data is a list of lists
            if not isinstance(data, list) or not data:
                return self.create_table([['No financial data available']])
            
            # Format currency values
            formatted_data = []
            for row in data:
                if not isinstance(row, list):
                    row = [row]
                formatted_row = []
                for cell in row:
                    try:
                        if isinstance(cell, (int, float)) and cell != 0:
                            formatted_row.append(f"${cell:,.2f}")
                        else:
                            formatted_row.append(str(cell))
                    except:
                        formatted_row.append(str(cell))
                formatted_data.append(formatted_row)
            
            return self.create_table(formatted_data)
            
        except Exception as e:
            print(f"Error in create_financial_table: {str(e)}")  # Debug print
            return self.create_table([['Error creating financial table']])

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

class DocumentPage(PageTemplate):
    def __init__(self, id, pageSize=A4):
        self.pageWidth = pageSize[0]
        self.pageHeight = pageSize[1]
        frame = Frame(
            72,  # x
            72,  # y
            self.pageWidth - 144,  # width
            self.pageHeight - 144,  # height
            leftPadding=0,
            bottomPadding=0,
            rightPadding=0,
            topPadding=0,
        )
        PageTemplate.__init__(self, id, [frame])
        
    def beforeDrawPage(self, canvas, doc):
        """Add header and footer to each page"""
        canvas.saveState()
        
        # Simple header with college name
        canvas.setFont('Helvetica-Bold', 16)
        canvas.setFillColor(HexColor('#2C3E50'))  # Dark blue-gray
        canvas.drawString(72, self.pageHeight - 72, doc.college_name.upper())
        
        # Double line below header - moved down by 10 points
        canvas.setStrokeColor(HexColor('#2C3E50'))
        canvas.setLineWidth(0.5)
        canvas.line(72, self.pageHeight - 95, self.pageWidth - 72, self.pageHeight - 95)
        canvas.line(72, self.pageHeight - 98, self.pageWidth - 72, self.pageHeight - 98)
        
        # Adjust frame position to prevent overlap
        frame = Frame(
            72,  # x
            72,  # y
            self.pageWidth - 144,  # width
            self.pageHeight - 170,  # height - increased top margin
            leftPadding=0,
            bottomPadding=0,
            rightPadding=0,
            topPadding=0,
        )
        
        # Thin border around page
        canvas.setStrokeColor(HexColor('#BDC3C7'))  # Light gray
        canvas.setLineWidth(0.5)
        canvas.rect(36, 36, self.pageWidth - 72, self.pageHeight - 72)
        
        # Footer with page number and watermark
        canvas.setFont('Times-Roman', 8)  # Using Times-Roman instead of Helvetica
        canvas.setFillColor(HexColor('#95A5A6'))  # Gray
        
        # Left side: Page number
        canvas.drawString(72, 50, f"Page {doc.page}")
        
        # Center: Watermark in slanted text
        canvas.saveState()
        watermark_text = "made by DazzloDocs"
        watermark_width = canvas.stringWidth(watermark_text, 'Times-Roman', 8)
        x_position = (self.pageWidth - watermark_width) / 2
        canvas.translate(x_position, 50)
        canvas.rotate(0)  # No rotation for now
        canvas.drawString(0, 0, watermark_text)
        canvas.restoreState()
        
        # Right side: Document title
        canvas.drawRightString(self.pageWidth - 72, 50, doc.title)
        
        canvas.restoreState()

class EnhancedDocumentGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        # Create custom header style with more spacing
        self.styles.add(ParagraphStyle(
            name='CustomHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=25,  # Increased space after header
            spaceBefore=20,  # Added space before header
            leading=24,      # Increased line height
            textColor=HexColor("#2C3E50")
        ))
        
        # Create custom underline style
        self.styles.add(ParagraphStyle(
            name='Underline',
            parent=self.styles['Normal'],
            fontSize=1,      # Very thin line
            leading=0,       # Minimal line height
            spaceBefore=0,   # No space before
            spaceAfter=15,   # Space after underline
            textColor=HexColor("#BDC3C7")  # Lighter color for underline
        ))
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
        try:
            if chart_type == 'bar':
                chart_buffer = self.chart_maker.create_bar_chart(
                    data=data.get('values', []),
                    labels=data.get('labels', []),
                    title=data.get('title', 'Bar Chart'),
                    xlabel=data.get('xlabel', 'Categories'),
                    ylabel=data.get('ylabel', 'Values')
                )
            elif chart_type == 'pie':
                chart_buffer = self.chart_maker.create_pie_chart(
                    data=data.get('values', []),
                    labels=data.get('labels', []),
                    title=data.get('title', 'Pie Chart')
                )
            elif chart_type == 'line':
                chart_buffer = self.chart_maker.create_line_chart(
                    x_data=data.get('labels', []),
                    y_data=data.get('values', []),
                    title=data.get('title', 'Line Chart'),
                    xlabel=data.get('xlabel', 'X Axis'),
                    ylabel=data.get('ylabel', 'Y Axis')
                )
            elif chart_type == 'scatter':
                chart_buffer = self.chart_maker.create_scatter_plot(
                    x_data=data.get('labels', []),
                    y_data=data.get('values', []),
                    title=data.get('title', 'Scatter Plot'),
                    xlabel=data.get('xlabel', 'X Axis'),
                    ylabel=data.get('ylabel', 'Y Axis')
                )
            else:
                print(f"Warning: Unknown chart type: {chart_type}")
                return
            
            if section not in self.charts:
                self.charts[section] = []
            self.charts[section].append({
                'type': chart_type,
                'buffer': chart_buffer,
                'title': data.get('title', f'{chart_type.title()} Chart')
            })
        except Exception as e:
            print(f"Error creating chart: {e}")
            # Create a simple error chart
            if section not in self.charts:
                self.charts[section] = []
            self.charts[section].append({
                'type': 'error',
                'buffer': None,
                'title': f'Error creating {chart_type} chart'
            })
    
    def add_table(self, section, data, title="Table"):
        """Add a table to a section with improved structure and spacing
        
        Args:
            section (str): Section name where the table should be added
            data (list or dict): Table data - can be either:
                - List of lists (direct table data)
                - Dict with 'headers' and 'rows' keys
        """
        if section not in self.tables:
            self.tables[section] = []
        
        # Handle different data formats
        if isinstance(data, list):
            # Direct table data (list of lists)
            table_data = data
            headers = data[0] if data else []
        elif isinstance(data, dict):
            # Dictionary format with headers and rows
            headers = data.get('headers', [])
            rows = data.get('rows', [])
            table_data = [headers] + rows if headers else rows
        else:
            # Fallback - create empty table
            table_data = [['No data available']]
            headers = ['No data available']
        
        # Ensure we have valid data
        if not table_data or not table_data[0]:
            table_data = [['No data available']]
            headers = ['No data available']
        
        # Calculate column widths based on content
        col_widths = []
        for col in range(len(table_data[0])):
            col_content = [str(row[col]) for row in table_data]
            max_width = max(len(content) for content in col_content)
            col_widths.append(min(max(max_width * 0.15 * inch, 1.5*inch), 3*inch))
        
        # Create table with calculated widths
        table = Table(table_data, colWidths=col_widths)
        
        # Debug: Print table data for verification
        print(f"Table data for {section}: {table_data}")
        print(f"Table has {len(table_data)} rows and {len(table_data[0]) if table_data else 0} columns")
        
        # Create professional table style with improved spacing
        table_style = TableStyle([
            # Header styling - separate from content with MUCH more padding
            ('BACKGROUND', (0, 0), (-1, 0), HexColor(self.colors['primary'])),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, 0), 20),  # Much more padding for headers
            ('BOTTOMPADDING', (0, 0), (-1, 0), 20),  # Much more padding for headers
            ('LEFTPADDING', (0, 0), (-1, 0), 12),  # Much more padding for headers
            ('RIGHTPADDING', (0, 0), (-1, 0), 12),  # Much more padding for headers
            
            # Content styling - separate from headers
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('TEXTCOLOR', (0, 1), (-1, -1), HexColor(self.colors['text'])),
            ('TOPPADDING', (0, 1), (-1, -1), 12),  # Content padding
            ('BOTTOMPADDING', (0, 1), (-1, -1), 12),  # Content padding
            ('LEFTPADDING', (0, 1), (-1, -1), 8),  # Content padding
            ('RIGHTPADDING', (0, 1), (-1, -1), 8),  # Content padding
            
            # Borders - thinner for better appearance
            ('GRID', (0, 0), (-1, -1), 0.25, HexColor(self.colors['border'])),
            ('LINEBELOW', (0, 0), (-1, 0), 1, HexColor(self.colors['primary'])),
            
            # Spacing between rows - increased for better readability
            ('LEADING', (0, 0), (-1, -1), 18),
        ])
        
        table.setStyle(table_style)
        
        # Add spacer before table and ensure proper spacing
        self.tables[section].append({
            'table': table,
            'title': title,
            'spacer': Spacer(1, 0.3*inch)  # Increased space before table
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
        """Create professional header and footer"""
        canvas.saveState()
        width, height = A4
        
        # Simple header with college name
        canvas.setFont('Helvetica-Bold', 16)
        canvas.setFillColor(HexColor(self.colors['primary']))
        college_name = self.user_data.get('college_name', 'COLLEGE NAME').upper()
        canvas.drawString(72, height - 72, college_name)
        
        # Double line below header
        canvas.setStrokeColor(HexColor(self.colors['primary']))
        canvas.setLineWidth(0.5)
        canvas.line(72, height - 85, width - 72, height - 85)
        canvas.line(72, height - 88, width - 72, height - 88)
        
        # Thin border around page
        canvas.setStrokeColor(HexColor(self.colors['border']))
        canvas.setLineWidth(0.5)
        canvas.rect(36, 36, width - 72, height - 72)
        
        # Footer with page number and watermark
        canvas.setFont('Times-Roman', 8)  # Using Times-Roman instead of Helvetica
        canvas.setFillColor(HexColor(self.colors['secondary']))
        
        # Left side: Page number
        canvas.drawString(72, 50, f"Page {canvas.getPageNumber()}")
        
        # Center: Watermark in slanted text
        canvas.saveState()
        watermark_text = "made by DazzloDocs"
        watermark_width = canvas.stringWidth(watermark_text, 'Times-Roman', 8)
        x_position = (width - watermark_width) / 2
        canvas.translate(x_position, 50)
        canvas.rotate(0)  # No rotation for now
        canvas.drawString(0, 0, watermark_text)
        canvas.restoreState()
        
        # Right side: Document title
        title_text = f"{self.user_data.get('subject', '')} | {self.user_data.get('student_name', '')}"
        canvas.drawRightString(width - 72, 50, title_text)
        
        canvas.restoreState()

    def create_title_page(self, story):
        """Create a simple and clean title page"""
        # Add initial spacing
        story.append(Spacer(1, 2*inch))
        
        # College Name
        college_style = ParagraphStyle(
            'CollegeHeader',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=HexColor(self.colors['primary']),
            alignment=TA_CENTER,
            spaceAfter=30
        )
        college_name = self.user_data.get('college_name', 'COLLEGE NAME').upper()
        story.append(Paragraph(college_name, college_style))
        
        # Document Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=20,
            textColor=HexColor(self.colors['secondary']),
            alignment=TA_CENTER,
            spaceAfter=20
        )
        story.append(Paragraph(self.user_data.get('subject', '').upper(), title_style))
        
        # Assignment Topic
        if self.user_data.get('assignment_topic'):
            topic_style = ParagraphStyle(
                'TopicStyle',
                parent=self.styles['Normal'],
                fontSize=14,
                textColor=HexColor(self.colors['text']),
                alignment=TA_CENTER,
                spaceAfter=40
            )
            story.append(Paragraph(f"Topic: {self.user_data.get('assignment_topic', '')}", topic_style))
        
        # Personal Information Table with simpler styling
        data = [
            ['Student Name:', self.user_data.get('student_name', '')],
            ['Class:', self.user_data.get('class', '')],
            ['Roll Number:', self.user_data.get('roll_number', '')],
            ['Subject Teacher:', self.user_data.get('subject_teacher', '')]
        ]
        
        # Add optional fields if they exist
        optional_fields = [
            ('Project Date:', 'project_date'),
            ('Submission Date:', 'submission_date')
        ]
        
        for label, field in optional_fields:
            if self.user_data.get(field):
                data.append([label, self.user_data.get(field)])
        
        # Create table with clean styling
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), HexColor(self.colors['text'])),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor(self.colors['border']))
        ]))
        
        story.append(table)
        story.append(PageBreak())
    
    def create_content_pages(self, story):
        """Create the content pages with sections"""
        for section in self.template["sections"]:
            if section in self.content and self.content[section]:
                # Add header with more spacing
                story.append(Spacer(1, 20))  # Space before section
                story.append(Paragraph(section.replace('_', ' ').title(), self.styles['CustomHeader']))
                
                # Add thin underline with spacing
                story.append(Paragraph("_" * 80, self.styles['Underline']))
                
                # Add content with proper spacing
                story.append(Spacer(1, 10))  # Space after underline
                story.append(Paragraph(self.content[section], self.styles['Normal']))
                story.append(Spacer(1, 20))  # Space after content

    def generate_pdf(self, output=None):
        """Generate the enhanced PDF document"""
        if output is None:
            output = f"DazzloDocs_{self.user_data.get('student_name', 'Student')}_{self.user_data.get('subject', 'Document')}.pdf"
        
        # Create document with standard margins
        doc = SimpleDocTemplate(
            output,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build story
        story = []
        
        # Create title page
        self.create_title_page(story)
        
        # Create content pages
        self.create_content_pages(story)
        
        # Build document with header/footer
        doc.build(
            story,
            onFirstPage=self.create_header_footer,
            onLaterPages=self.create_header_footer
        )
        
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