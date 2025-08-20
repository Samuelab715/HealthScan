import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")

@app.route('/')
def index():
    """Display the medical information collection form"""
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    """Process the submitted form and display summary"""
    try:
        # Extract form data
        form_data = {}
        
        # Personal Information (optional)
        form_data['name'] = request.form.get('name', '').strip()
        form_data['age'] = request.form.get('age', '').strip()
        form_data['gender'] = request.form.get('gender', '').strip()
        form_data['contact'] = request.form.get('contact', '').strip()
        
        # Medical Information
        # Underlying diseases (multiple selection)
        form_data['diseases'] = request.form.getlist('diseases')
        
        # Allergies (multiple selection)
        form_data['allergies'] = request.form.getlist('allergies')
        
        # Vital signs (optional)
        form_data['blood_pressure'] = request.form.get('blood_pressure', '').strip()
        form_data['temperature'] = request.form.get('temperature', '').strip()
        form_data['heart_rate'] = request.form.get('heart_rate', '').strip()
        
        # Pregnancy status (conditional)
        form_data['pregnancy'] = request.form.get('pregnancy', '').strip()
        
        # Basic validation
        if not form_data['diseases'] and not form_data['allergies']:
            flash('Please select at least one option for underlying diseases or allergies.', 'error')
            return redirect(url_for('index'))
        
        # Log the submission
        app.logger.info(f"Form submitted with data: {form_data}")
        
        return render_template('summary.html', data=form_data)
        
    except Exception as e:
        app.logger.error(f"Error processing form submission: {str(e)}")
        flash('An error occurred while processing your submission. Please try again.', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
