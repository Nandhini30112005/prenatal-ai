from flask import Flask, render_template, request, send_file
import os, uuid
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    nipt = float(request.form['nipt'])
    cvs = float(request.form['cvs'])

    file = request.files['image']
    filename = ""

    if file and file.filename != "":
        filename = str(uuid.uuid4()) + "_" + file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

    imaging_score = round((nipt + cvs) / 2, 2)
    risk_score = (nipt*0.4) + (cvs*0.4) + (imaging_score*0.2)

    if risk_score > 0.7:
        result = "HIGH"
        diagnosis = "DISABLED"
    elif risk_score > 0.4:
        result = "MODERATE"
        diagnosis = "POSSIBLE DISABILITY"
    else:
        result = "LOW"
        diagnosis = "NOT DISABLED"

    confidence = round(risk_score * 100, 2)

    return render_template('index.html',
                           result=result,
                           diagnosis=diagnosis,
                           confidence=confidence,
                           nipt=nipt,
                           cvs=cvs,
                           imaging=imaging_score,
                           image=filename)

@app.route('/report')
def report():
    file_path = "report.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    diagnosis = request.args.get('diagnosis')
    result = request.args.get('result')
    confidence = request.args.get('confidence')

    content = []
    content.append(Paragraph("AI Prenatal Diagnostic Report", styles['Title']))
    content.append(Spacer(1,10))
    content.append(Paragraph(f"Diagnosis: {diagnosis}", styles['Normal']))
    content.append(Paragraph(f"Risk Level: {result}", styles['Normal']))
    content.append(Paragraph(f"Confidence: {confidence}%", styles['Normal']))

    doc.build(content)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)