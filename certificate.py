from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

def generate_certificate( training_name):
    current_date = datetime.now().strftime("%d-%m-%Y")
    
    
    name = training_name
    filename = f"certyfikat {name}.pdf"
    # Create a PDF document
    pdf_canvas = canvas.Canvas(filename, pagesize=letter)

    # Set font and size
    pdf_canvas.setFont("Helvetica", 12)

    # Certificate title
    pdf_canvas.drawCentredString(300, 700, "Certyfikat ukonczenia")

    # Participant name
    pdf_canvas.drawCentredString(300, 650, f"Ten certyfikat potwierdza, iz uczestnik")

    # Training name
    pdf_canvas.drawCentredString(300, 630, f"pomyslnie ukonczyl kurs szkoleniowy {name} ")

    # Date
    pdf_canvas.drawCentredString(300, 610, f"Data: {current_date}")

    # Add any additional information or styling as needed

    # Save the PDF
    pdf_canvas.save()




