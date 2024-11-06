import sqlite3
class MedicalExpertSystem:
    def __init__(self):
        self.conn = sqlite3.connect("patient_history.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patient_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                gender TEXT,
                known_conditions TEXT,
                symptoms TEXT,
                diagnosis TEXT,
                treatment TEXT
            )
        ''')
        self.conn.commit()

        self.knowledge_base = {
            "flu": {
                "symptoms": ["fever", "cough", "headache", "fatigue", "sore throat"],
                "treatment": "Rest, drink fluids, and take antiviral medication if prescribed."
            },
            "cold": {
                "symptoms": ["cough", "runny nose", "sore throat", "sneezing"],
                "treatment": "Drink warm fluids, rest, and take over-the-counter medication."
            },
            "diabetes": {
                "symptoms": ["increased thirst", "frequent urination", "fatigue", "blurred vision"],
                "treatment": "Monitor blood sugar levels, take insulin if needed, and follow a healthy diet."
            },
            "hypertension": {
                "symptoms": ["headache", "shortness of breath", "nosebleeds", "chest pain"],
                "treatment": "Exercise, reduce salt intake, and take prescribed medication."
            },
            "migraine": {
                "symptoms": ["throbbing headache", "nausea", "sensitivity to light", "sensitivity to sound"],
                "treatment": "Rest in a dark, quiet room, take pain relief medication, and use prescription medication for migraines."
            },
            "asthma": {
                "symptoms": ["shortness of breath", "wheezing", "chest tightness", "coughing", "difficulty breathing"],
                "treatment": "Use an inhaler, avoid triggers, take prescribed medications, and follow an asthma action plan."
            },
            "pneumonia": {
                "symptoms": ["chest pain", "cough with phlegm", "fever", "shortness of breath", "fatigue"],
                "treatment": "Take antibiotics if bacterial, rest, drink fluids, and use fever-reducing medication."
            },
            "allergies": {
                "symptoms": ["sneezing", "itchy eyes", "runny nose", "skin rashes", "swelling"],
                "treatment": "Avoid allergens, take antihistamines, and use prescribed medications."
            },
            "covid-19": {
                "symptoms": ["fever", "cough", "loss of taste or smell", "fatigue", "difficulty breathing"],
                "treatment": "Isolate, rest, drink fluids, monitor symptoms, and seek medical care if symptoms worsen."
            },
            "bronchitis": {
                "symptoms": ["cough with mucus", "chest discomfort", "fatigue", "fever", "shortness of breath"],
                "treatment": "Rest, drink fluids, avoid irritants, and take prescribed medication if needed."
            },
            "depression": {
                "symptoms": ["persistent sadness", "loss of interest", "fatigue", "changes in sleep", "feeling hopeless"],
                "treatment": "Seek counseling, take prescribed antidepressants, and make lifestyle changes such as exercise."
            },
            "anxiety": {
                "symptoms": ["nervousness", "rapid heart rate", "sweating", "trembling", "restlessness"],
                "treatment": "Practice relaxation techniques, take prescribed medications, and consider cognitive behavioral therapy."
            },
            "strep throat": {
                "symptoms": ["sore throat", "pain when swallowing", "fever", "red/swollen tonsils", "white patches in the throat"],
                "treatment": "Take antibiotics, rest, drink warm fluids, and take over-the-counter pain relievers."
            },
            "gastroenteritis": {
                "symptoms": ["diarrhea", "vomiting", "nausea", "abdominal pain", "fever"],
                "treatment": "Stay hydrated, rest, avoid solid foods until symptoms improve, and take anti-nausea medication if needed."
            },
            "eczema": {
                "symptoms": ["itchy skin", "red or inflamed patches", "dry skin", "swelling", "crusting"],
                "treatment": "Use moisturizers, avoid triggers, and apply prescribed topical medications."
            },
            "sinusitis": {
                "symptoms": ["facial pain", "congested nose", "runny nose", "headache", "fatigue"],
                "treatment": "Take decongestants, rest, drink fluids, and use nasal sprays if prescribed."
            },
            "urinary tract infection (UTI)": {
                "symptoms": ["painful urination", "frequent urge to urinate", "cloudy or strong-smelling urine", "lower abdominal pain"],
                "treatment": "Take prescribed antibiotics, drink plenty of water, and avoid irritants such as caffeine."
            },
            "heart attack": {
                "symptoms": ["chest pain", "shortness of breath", "nausea", "sweating", "pain in the left arm or jaw"],
                "treatment": "Seek emergency medical help immediately, take prescribed medications, and follow a cardiac care plan."
            },
        }
        
        self.patient_history = {}

    def store_patient_history(self, patient_name, patient_age, patient_gender, patient_conditions, patient_symptoms, diagnosis, treatment):
        """Store patient history in the SQLite database."""
        self.cursor.execute('''
            INSERT INTO patient_history (name, age, gender, known_conditions, symptoms, diagnosis, treatment)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (patient_name, patient_age, patient_gender, ",".join(patient_conditions), ",".join(patient_symptoms), diagnosis, treatment))
        self.conn.commit()

    def get_patient_history(self, patient_name):
        """Retrieve patient history from the database."""
        self.cursor.execute('''
            SELECT * FROM patient_history WHERE name = ?
        ''', (patient_name,))
        return self.cursor.fetchall()

    def diagnose(self, patient_name, patient_symptoms):
        potential_diagnoses = {}

        for disease, info in self.knowledge_base.items():
            matching_symptoms = set(patient_symptoms).intersection(info['symptoms'])
            match_percentage = len(matching_symptoms) / len(info['symptoms'])

            if matching_symptoms:
                potential_diagnoses[disease] = {
                    "match_percentage": match_percentage,
                    "matching_symptoms": list(matching_symptoms),
                    "treatment": info['treatment']
                }

        if potential_diagnoses:
            ranked_diagnoses = sorted(potential_diagnoses.items(), key=lambda x: x[1]["match_percentage"], reverse=True)
            best_match = ranked_diagnoses[0]
            diagnosis, details = best_match
            return diagnosis, details

        return None, "No matching disease found. Please consult a healthcare professional."

    def input_symptoms(self):
        print("Welcome to the Medical Expert System!")
        print("Please enter your name:")
        patient_name = input().strip()

        print("Please provide your age:")
        patient_age = input().strip()

        print("Please provide your gender (M/F/Other):")
        patient_gender = input().strip()

        print("Do you have any known medical conditions? (e.g., diabetes, hypertension):")
        patient_conditions = input().strip().lower().split(',')

        history = self.get_patient_history(patient_name)
        if history:
            print(f"\nMedical history for {patient_name}:")
            for record in history:
                print(f"Diagnosis: {record[6]}, Symptoms: {record[5]}, Treatment: {record[7]}")
        else:
            print(f"No medical history found for {patient_name}.")

        print("\nPlease enter the symptoms you are experiencing (comma-separated):")
        patient_input = input()
        patient_symptoms = [symptom.strip().lower() for symptom in patient_input.split(",")]

        diagnosis, details = self.diagnose(patient_name, patient_symptoms)

        if diagnosis:
            print(f"\nDiagnosis: {diagnosis.capitalize()}")
            print(f"Matching Symptoms: {', '.join(details['matching_symptoms'])}")
            print(f"Match Percentage: {details['match_percentage'] * 100:.1f}%")
            print(f"Suggested Treatment: {details['treatment']}")

            # Store the patient history in the database
            self.store_patient_history(patient_name, patient_age, patient_gender, patient_conditions, patient_symptoms, diagnosis, details['treatment'])
        else:
            print(f"\n{details}")

# Create an instance of the MedicalExpertSystem
expert_system = MedicalExpertSystem()

# Run the system
expert_system.input_symptoms()