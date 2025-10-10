import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import google.generativeai as genai
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from io import BytesIO
import tempfile

# ============================
# Flask & Logging setup
# ============================
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key_for_replit")
CORS(app)

# ============================
# Gemini Model Configuration
# ============================
MODEL_NAME = "models/gemini-2.5-pro"   # ✅ confirmed available
gemini_model = None

def get_gemini_model(api_key):
    """Initialize and return the Gemini model."""
    global gemini_model
    if gemini_model is None:
        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel(MODEL_NAME)
    return gemini_model

# ============================
# Routes
# ============================
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/generator/<topic_id>')
def generator(topic_id):
    return render_template('generator.html', topic_id=topic_id)

@app.route('/api/generate-content', methods=['POST'])
def generate_content():
    """Generate educational content using Gemini 2.5 Pro"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        api_key = data.get('api_key')
        prompt = data.get('prompt')
        temperature = float(data.get('temperature', 0.7))
        content_type = data.get('content_type', 'mcq')

        if not api_key:
            return jsonify({'error': 'Gemini API key is required'}), 400
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        model = get_gemini_model(api_key)
        enhanced_prompt = enhance_prompt_for_content_type(prompt, content_type)

        response = model.generate_content(
            enhanced_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature
            )
        )

        # ✅ Handle Gemini 2.5 response structure safely
        if response.candidates and response.candidates[0].content.parts:
            raw_text = response.candidates[0].content.parts[0].text.strip()
        else:
            raise ValueError("Empty response from Gemini")

        # ✅ Try to parse JSON
        try:
            content = json.loads(raw_text)
        except json.JSONDecodeError:
            logging.warning("Model response was not valid JSON. Returning as plain text.")
            content = {"text": raw_text}

        return jsonify({
            'success': True,
            'content': content,
            'content_type': content_type
        })

    except Exception as e:
        logging.error(f"Error generating content: {e}")
        return jsonify({
            'error': f'Failed to generate content: {str(e)}',
            'error_type': 'generation_error'
        }), 500

# ============================
# Prompt Enhancer
# ============================
def enhance_prompt_for_content_type(prompt, content_type):
    """Enhance the prompt with strict JSON output instructions."""
    content_type_instructions = {
        'mcq': '''
Return the output strictly in valid JSON. Do not include any text outside the JSON.
Use this structure:
{
  "title": "Topic Title",
  "questions": [
    {
      "question": "Question text",
      "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "correct_answer": "A",
      "explanation": "Why this answer is correct"
    }
  ]
}
''',
        'cheat_sheet': '''
Return valid JSON only. Structure:
{
  "title": "Cheat Sheet Title",
  "sections": [
    {"heading": "Section Title", "content": ["Point 1", "Point 2"]}
  ],
  "quick_tips": ["Tip 1", "Tip 2"]
}
''',
        'textual': '''
Return valid JSON only. Structure:
{
  "title": "Exercise Title",
  "questions": [
    {"type": "short_answer", "question": "Q", "sample_answer": "Expected"},
    {"type": "essay", "question": "Q", "guidelines": "Guidelines"}
  ]
}
'''
    }

    instruction = content_type_instructions.get(content_type, content_type_instructions['mcq'])
    return f"{prompt}\n\n{instruction}"

# ============================
# Excel & JSON Export
# ============================
@app.route('/api/export-excel', methods=['POST'])
def export_excel():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        content = data.get('content')
        content_type = data.get('content_type')
        topic_title = data.get('topic_title', 'English Course Content')

        if not content:
            return jsonify({'error': 'No content to export'}), 400

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Course Content"

        title_font = Font(name='Arial', size=16, bold=True)
        header_font = Font(name='Arial', size=12, bold=True)
        normal_font = Font(name='Arial', size=10)
        title_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
        header_fill = PatternFill(start_color='D9E2F3', end_color='D9E2F3', fill_type='solid')

        row = 1
        ws.merge_cells(f'A{row}:E{row}')
        title_cell = ws[f'A{row}']
        title_cell.value = f"{topic_title} - {content_type.upper()}"
        title_cell.font = title_font
        title_cell.fill = title_fill
        title_cell.alignment = Alignment(horizontal='center')
        row += 2

        # Export based on content type
        if content_type == 'mcq':
            export_mcq_to_excel(ws, content, row, header_font, normal_font, header_fill)
        elif content_type == 'cheat_sheet':
            export_cheat_sheet_to_excel(ws, content, row, header_font, normal_font, header_fill)
        elif content_type == 'textual':
            export_textual_to_excel(ws, content, row, header_font, normal_font, header_fill)

        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width

        excel_file = BytesIO()
        wb.save(excel_file)
        excel_file.seek(0)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        temp_file.write(excel_file.getvalue())
        temp_file.close()

        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=f"{topic_title.replace(' ', '_')}_{content_type}.xlsx",
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        logging.error(f"Error exporting to Excel: {str(e)}")
        return jsonify({'error': f'Failed to export to Excel: {str(e)}'}), 500

@app.route('/api/export-json', methods=['POST'])
def export_json():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        content = data.get('content')
        content_type = data.get('content_type')
        topic_title = data.get('topic_title', 'English Course Content')

        if not content:
            return jsonify({'error': 'No content to export'}), 400

        json_export = {
            'metadata': {
                'title': topic_title,
                'content_type': content_type,
                'generated_at': datetime.now().isoformat(),
                'application': 'English Communication Course Builder'
            },
            'content': content
        }

        json_content = json.dumps(json_export, indent=2, ensure_ascii=False)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json', mode='w', encoding='utf-8')
        temp_file.write(json_content)
        temp_file.close()

        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=f"{topic_title.replace(' ', '_')}_{content_type}.json",
            mimetype='application/json'
        )

    except Exception as e:
        logging.error(f"Error exporting to JSON: {str(e)}")
        return jsonify({'error': f'Failed to export to JSON: {str(e)}'}), 500

# ============================
# Export helpers
# ============================
def export_mcq_to_excel(ws, content, start_row, header_font, normal_font, header_fill):
    row = start_row
    headers = ['Question', 'Option A', 'Option B', 'Option C', 'Option D', 'Correct Answer', 'Explanation']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=row, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
    row += 1
    questions = content.get('questions', [])
    for q in questions:
        ws.cell(row=row, column=1, value=q.get('question', '')).font = normal_font
        options = q.get('options', [])
        for i, option in enumerate(options[:4], 2):
            ws.cell(row=row, column=i, value=option).font = normal_font
        ws.cell(row=row, column=6, value=q.get('correct_answer', '')).font = normal_font
        ws.cell(row=row, column=7, value=q.get('explanation', '')).font = normal_font
        row += 1

def export_cheat_sheet_to_excel(ws, content, start_row, header_font, normal_font, header_fill):
    row = start_row
    sections = content.get('sections', [])
    for section in sections:
        ws.merge_cells(f'A{row}:C{row}')
        heading_cell = ws[f'A{row}']
        heading_cell.value = section.get('heading', '')
        heading_cell.font = header_font
        heading_cell.fill = header_fill
        row += 1
        for item in section.get('content', []):
            ws.cell(row=row, column=1, value=f"• {item}").font = normal_font
            row += 1
        row += 1
    if content.get('quick_tips'):
        ws.merge_cells(f'A{row}:C{row}')
        tips_cell = ws[f'A{row}']
        tips_cell.value = "Quick Tips"
        tips_cell.font = header_font
        tips_cell.fill = header_fill
        row += 1
        for tip in content.get('quick_tips', []):
            ws.cell(row=row, column=1, value=f"• {tip}").font = normal_font
            row += 1

def export_textual_to_excel(ws, content, start_row, header_font, normal_font, header_fill):
    row = start_row
    headers = ['Type', 'Question', 'Sample Answer/Guidelines']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=row, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
    row += 1
    questions = content.get('questions', [])
    for q in questions:
        ws.cell(row=row, column=1, value=q.get('type', '')).font = normal_font
        ws.cell(row=row, column=2, value=q.get('question', '')).font = normal_font
        answer_or_guidelines = q.get('sample_answer', '') or q.get('guidelines', '')
        ws.cell(row=row, column=3, value=answer_or_guidelines).font = normal_font
        row += 1

# ============================
# Run
# ============================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
