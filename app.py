import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")

@app.route('/')
def index():
    """Display the homepage with link to medical form"""
    return render_template('index.html')

@app.route('/form')
def medical_form():
    """Display the medical information collection form"""
    # Clear any existing session data
    session.pop('medical_data', None)
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    """Process the submitted form and redirect to symptoms selection"""
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
            return redirect(url_for('medical_form'))
        
        # Store medical data in session for symptoms selection
        session['medical_data'] = form_data
        
        # Log the submission
        app.logger.info(f"Medical form submitted with data: {form_data}")
        
        # Redirect to symptoms selection
        return redirect(url_for('symptoms_selection'))
        
    except Exception as e:
        app.logger.error(f"Error processing form submission: {str(e)}")
        flash('An error occurred while processing your submission. Please try again.', 'error')
        return redirect(url_for('medical_form'))

@app.route('/symptoms')
def symptoms_selection():
    """Display symptoms selection form"""
    if 'medical_data' not in session:
        flash('Please complete the medical information form first.', 'error')
        return redirect(url_for('medical_form'))
    
    return render_template('symptoms.html')

@app.route('/diagnose', methods=['POST'])
def diagnose():
    """Process symptoms and provide diagnostic results"""
    try:
        if 'medical_data' not in session:
            flash('Please complete the medical information form first.', 'error')
            return redirect(url_for('medical_form'))
        
        # Get medical data from session
        medical_data = session['medical_data']
        
        # Get selected symptoms
        symptoms = request.form.getlist('symptoms')
        
        if not symptoms:
            flash('Please select at least one symptom.', 'error')
            return redirect(url_for('symptoms_selection'))
        
        # Generate diagnosis
        diagnosis_result = generate_diagnosis(medical_data, symptoms)
        
        # Log the diagnosis
        app.logger.info(f"Diagnosis generated for symptoms: {symptoms}")
        
        # Clear session data
        session.pop('medical_data', None)
        
        return render_template('diagnosis.html', 
                             medical_data=medical_data, 
                             symptoms=symptoms, 
                             diagnosis=diagnosis_result)
        
    except Exception as e:
        app.logger.error(f"Error generating diagnosis: {str(e)}")
        flash('An error occurred while processing your symptoms. Please try again.', 'error')
        return redirect(url_for('symptoms_selection'))

def generate_diagnosis(medical_data, symptoms):
    """Generate diagnostic recommendations based on medical info and symptoms"""
    
    # Define Ghana-relevant conditions and their associated symptoms
    conditions = {
        'Malaria': {
            'symptoms': ['high_fever', 'chills_rigors', 'sweating', 'severe_headache', 'body_aches', 'nausea', 'vomiting', 'severe_fatigue'],
            'severity': 'Moderate to Severe',
            'recommendations': [
                'Seek immediate medical attention for proper diagnosis and treatment',
                'Get tested for malaria parasites (rapid diagnostic test or microscopy)',
                'Take prescribed antimalarial medication as directed',
                'Stay hydrated and rest in a cool environment',
                'Use mosquito nets and repellents to prevent reinfection',
                'Monitor for severe complications (cerebral malaria signs)'
            ]
        },
        'Typhoid Fever': {
            'symptoms': ['high_fever', 'severe_headache', 'abdominal_pain', 'rose_colored_spots', 'diarrhea', 'constipation', 'severe_fatigue', 'loss_of_appetite'],
            'severity': 'Severe',
            'recommendations': [
                'Seek immediate medical attention for proper diagnosis',
                'Get blood culture or Widal test for confirmation',
                'Take prescribed antibiotics for full duration',
                'Maintain strict hygiene and safe water/food practices',
                'Stay well hydrated and get adequate nutrition',
                'Isolate to prevent spread to others'
            ]
        },
        'Cholera': {
            'symptoms': ['severe_watery_diarrhea', 'severe_vomiting', 'dehydration', 'abdominal_cramps', 'rapid_heartbeat'],
            'severity': 'Severe',
            'recommendations': [
                'Seek immediate emergency medical care',
                'Start oral rehydration solution (ORS) immediately',
                'Get intravenous fluids if severely dehydrated',
                'Take prescribed antibiotics if recommended',
                'Maintain strict hygiene to prevent spread',
                'Report to health authorities for public health response'
            ]
        },
        'Gastroenteritis (Food Poisoning)': {
            'symptoms': ['nausea', 'vomiting', 'diarrhea', 'stomach_pain', 'abdominal_cramps', 'fatigue'],
            'severity': 'Mild to Moderate',
            'recommendations': [
                'Stay hydrated with ORS or clean water',
                'Follow BRAT diet (Bananas, Rice, Applesauce, Toast)',
                'Rest and avoid dairy products temporarily',
                'Seek medical attention if symptoms persist beyond 3 days',
                'Practice food safety and proper hand hygiene'
            ]
        },
        'Common Cold': {
            'symptoms': ['runny_nose', 'sneezing', 'sore_throat', 'mild_cough', 'fatigue', 'headache'],
            'severity': 'Mild',
            'recommendations': [
                'Rest and stay well hydrated',
                'Use steam inhalation for nasal congestion',
                'Gargle with warm salt water for sore throat',
                'Should resolve within 7-10 days',
                'Avoid close contact with others to prevent spread'
            ]
        },
        'Influenza (Flu)': {
            'symptoms': ['fever', 'body_aches', 'severe_fatigue', 'headache', 'dry_cough', 'chills'],
            'severity': 'Moderate',
            'recommendations': [
                'Rest and get plenty of fluids',
                'Consider antiviral medication if within 48 hours',
                'Monitor temperature and seek care if symptoms worsen',
                'Isolation recommended to prevent spread',
                'Get annual flu vaccination for prevention'
            ]
        },
        'Upper Respiratory Infection': {
            'symptoms': ['sore_throat', 'runny_nose', 'mild_cough', 'sneezing', 'nasal_congestion', 'headache'],
            'severity': 'Mild to Moderate',
            'recommendations': [
                'Rest and stay hydrated',
                'Use steam inhalation for congestion relief',
                'Warm beverages may help soothe throat',
                'See a doctor if symptoms persist beyond 10 days',
                'Maintain good hygiene to prevent spread'
            ]
        },
        'Dehydration/Heat Illness': {
            'symptoms': ['dehydration', 'rapid_heartbeat', 'confusion', 'severe_fatigue', 'headache'],
            'severity': 'Moderate to Severe',
            'recommendations': [
                'Move to a cool, shaded area immediately',
                'Drink ORS or clean water in small, frequent sips',
                'Seek medical attention if symptoms are severe',
                'Avoid strenuous activity during hot weather',
                'Wear light-colored, loose clothing in hot weather'
            ]
        },
        'Allergic Reaction': {
            'symptoms': ['skin_rash', 'itching', 'sneezing', 'runny_nose', 'watery_eyes'],
            'severity': 'Mild to Moderate',
            'recommendations': [
                'Avoid known allergens',
                'Use antihistamines as directed',
                'Apply cool compresses to affected skin areas',
                'Seek immediate medical attention for severe reactions',
                'Keep a record of triggers for future prevention'
            ]
        }
    }
    
    # Calculate condition scores based on symptom matches
    condition_scores = {}
    
    for condition_name, condition_data in conditions.items():
        score = 0
        condition_symptoms = condition_data['symptoms']
        
        # Calculate how many symptoms match
        for symptom in symptoms:
            if symptom in condition_symptoms:
                score += 1
        
        # Calculate percentage match
        if len(condition_symptoms) > 0:
            match_percentage = (score / len(condition_symptoms)) * 100
            condition_scores[condition_name] = {
                'score': score,
                'percentage': match_percentage,
                'data': condition_data
            }
    
    # Find the best matches
    sorted_conditions = sorted(condition_scores.items(), 
                             key=lambda x: (x[1]['score'], x[1]['percentage']), 
                             reverse=True)
    
    # Generate diagnosis result
    diagnosis = {
        'primary_condition': None,
        'alternative_conditions': [],
        'general_recommendations': [],
        'risk_factors': []
    }
    
    if sorted_conditions:
        # Primary condition (highest score)
        primary = sorted_conditions[0]
        if primary[1]['score'] > 0:
            diagnosis['primary_condition'] = {
                'name': primary[0],
                'confidence': min(primary[1]['percentage'] + 20, 95),  # Boost confidence slightly
                'severity': primary[1]['data']['severity'],
                'recommendations': primary[1]['data']['recommendations']
            }
        
        # Alternative conditions
        for condition_name, condition_info in sorted_conditions[1:3]:  # Top 2 alternatives
            if condition_info['score'] > 0:
                diagnosis['alternative_conditions'].append({
                    'name': condition_name,
                    'confidence': condition_info['percentage'],
                    'severity': condition_info['data']['severity']
                })
    
    # Add risk factors based on medical history
    risk_factors = []
    
    # Check for high-risk conditions
    high_risk_diseases = ['diabetes', 'hypertension', 'heart_disease', 'asthma']
    for disease in medical_data.get('diseases', []):
        if disease in high_risk_diseases:
            risk_factors.append(f"Pre-existing {disease.replace('_', ' ').title()} may increase complications")
    
    # Check vital signs
    temperature = medical_data.get('temperature', '')
    if temperature:
        try:
            temp_float = float(temperature)
            if temp_float >= 100.4:
                risk_factors.append("Elevated temperature detected - monitor closely")
        except ValueError:
            pass
    
    # Check age factors
    age = medical_data.get('age', '')
    if age:
        try:
            age_int = int(age)
            if age_int >= 65:
                risk_factors.append("Advanced age may require closer medical supervision")
            elif age_int <= 2:
                risk_factors.append("Young age requires careful monitoring")
        except ValueError:
            pass
    
    # Check pregnancy
    if medical_data.get('pregnancy') == 'yes':
        risk_factors.append("Pregnancy requires special medical considerations")
    
    diagnosis['risk_factors'] = risk_factors
    
    # General recommendations
    diagnosis['general_recommendations'] = [
        'Monitor symptoms and seek medical attention if they worsen',
        'Stay hydrated and get adequate rest',
        'Follow up with healthcare provider if symptoms persist',
        'This is not a substitute for professional medical advice'
    ]
    
    return diagnosis

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)