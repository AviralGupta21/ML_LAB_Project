import streamlit as st
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
import time

# Page Configuration
st.set_page_config(
    page_title="Solance AI - Student Mental Health Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Dark AI Dashboard
def load_css():
    css = """
    <style>
        /* Main Background */
        .stApp {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            color: #ffffff;
        }
        
        /* Hide Streamlit default elements */
        .stDeployButton {
            display: none;
        }
        
        #MainMenu {
            visibility: hidden;
        }
        
        header {
            visibility: hidden;
        }
        
        /* Glassmorphism Cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 25px;
            margin: 10px 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        }
        
        /* Header Styles */
        .main-header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
        }
        
        .main-title {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(45deg, #00ff88, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }
        
        .main-subtitle {
            font-size: 1.1rem;
            color: #b8b8b8;
            margin-bottom: 15px;
        }
        
        .status-badge {
            display: inline-block;
            padding: 8px 20px;
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid #00ff88;
            border-radius: 25px;
            color: #00ff88;
            font-size: 0.9rem;
            font-weight: 600;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(0, 255, 136, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
        }
        
        /* Prediction Result Styles */
        .prediction-high-risk {
            background: linear-gradient(135deg, #ff416c, #ff4b2b);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-size: 1.3rem;
            font-weight: 600;
            margin: 15px 0;
            box-shadow: 0 4px 20px rgba(255, 65, 108, 0.4);
            animation: glow-red 2s ease-in-out infinite alternate;
        }
        
        .prediction-low-risk {
            background: linear-gradient(135deg, #00ff88, #00d4ff);
            color: #000;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-size: 1.3rem;
            font-weight: 600;
            margin: 15px 0;
            box-shadow: 0 4px 20px rgba(0, 255, 136, 0.4);
            animation: glow-green 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow-red {
            from { box-shadow: 0 4px 20px rgba(255, 65, 108, 0.4); }
            to { box-shadow: 0 4px 30px rgba(255, 65, 108, 0.6); }
        }
        
        @keyframes glow-green {
            from { box-shadow: 0 4px 20px rgba(0, 255, 136, 0.4); }
            to { box-shadow: 0 4px 30px rgba(0, 255, 136, 0.6); }
        }
        
        /* Circular Progress */
        .circular-progress {
            position: relative;
            width: 200px;
            height: 200px;
            margin: 20px auto;
        }
        
        .circular-progress svg {
            transform: rotate(-90deg);
        }
        
        .progress-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 2rem;
            font-weight: bold;
        }
        
        /* Insight Cards */
        .insight-card {
            background: rgba(255, 255, 255, 0.03);
            border-left: 4px solid #00ff88;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            transition: all 0.3s ease;
        }
        
        .insight-card:hover {
            background: rgba(255, 255, 255, 0.08);
            transform: translateX(5px);
        }
        
        .insight-title {
            font-weight: 600;
            color: #00ff88;
            margin-bottom: 5px;
        }
        
        .insight-importance {
            background: rgba(0, 255, 136, 0.2);
            height: 6px;
            border-radius: 3px;
            margin: 8px 0;
            overflow: hidden;
        }
        
        .insight-importance-fill {
            height: 100%;
            background: linear-gradient(90deg, #00ff88, #00d4ff);
            border-radius: 3px;
            transition: width 1s ease;
        }
        
        .insight-explanation {
            font-size: 0.9rem;
            color: #b8b8b8;
            line-height: 1.4;
        }
        
        /* History Cards */
        .history-card {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 10px;
            padding: 12px;
            margin: 8px 0;
            border-left: 3px solid #00d4ff;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .history-time {
            font-size: 0.8rem;
            color: #888;
        }
        
        .history-result {
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85rem;
        }
        
        .history-high-risk {
            background: rgba(255, 65, 108, 0.2);
            color: #ff416c;
        }
        
        .history-low-risk {
            background: rgba(0, 255, 136, 0.2);
            color: #00ff88;
        }
        
        /* Form Styles */
        .stSelectbox > div > div > input,
        .stNumberInput > div > div > input {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        /* Button Styles */
        .stButton > button {
            background: linear-gradient(45deg, #00ff88, #00d4ff);
            color: black;
            border: none;
            padding: 12px 30px;
            font-weight: 600;
            border-radius: 25px;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 255, 136, 0.4);
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Load ML Models and Artifacts
@st.cache_resource
def load_models():
    try:
        model = pickle.load(open('model.pkl', 'rb'))
        encoders = pickle.load(open('encoders.pkl', 'rb'))
        columns = pickle.load(open('columns.pkl', 'rb'))
        scaler = pickle.load(open('scaler.pkl', 'rb'))
        return model, encoders, columns, scaler
    except FileNotFoundError:
        st.error("Model files not found. Please ensure model.pkl, encoders.pkl, columns.pkl, and scaler.pkl are in the same directory.")
        return None, None, None, None

model, encoders, columns, scaler = load_models()

# Feature importance and explanations
FEATURE_IMPORTANCE = {
    "Did you seek any specialist for a treatment?": 0.1425,
    "Marital status": 0.0725,
    "What is your course?": 0.0475,
    "gender": 0.0375,
    "What is your CGPA?": 0.0350,
    "Do you have Panic attack?": 0.0300,
    "Do you have Anxiety?": 0.0225,
    "Your current year of Study": 0.0175,
    "Age": 0.0000
}

FEATURE_EXPLANATIONS = {
    "What is your course?": "Different academic disciplines impose varying levels of workload, competition, and career uncertainty, which can significantly influence stress levels and mental well-being among students.",
    "Marital status": "Personal relationship dynamics and responsibilities can impact emotional stability, social support systems, and overall mental health.",
    "Age": "Students at different age groups experience varying academic pressures, life responsibilities, and coping mechanisms, which can affect their mental health differently.",
    "Do you have Anxiety?": "Anxiety is strongly correlated with depression and often acts as an early psychological indicator of mental health distress.",
    "Your current year of Study": "Academic pressure tends to increase in higher years due to workload, expectations, and career-related stress, making it a relevant factor in mental health assessment.",
    "What is your CGPA?": "Academic performance can directly influence self-esteem, stress levels, and future concerns, all of which are closely linked to mental health.",
    "Do you have Panic attack?": "Experiencing panic attacks may indicate underlying psychological distress or anxiety disorders, which are strongly associated with depression.",
    "gender": "Gender-related societal expectations, emotional expression patterns, and stress factors may contribute to differences in mental health outcomes.",
    "Did you seek any specialist for a treatment?": "Seeking professional help often reflects prior or ongoing mental health challenges, making it a strong indicator in predicting depression."
}

# Course options
COURSE_OPTIONS = [
    "Engineering","Islamic Education","BIT","Laws","Mathematics","Pendidikan islam","BCS",
    "Human Resources","Irkhs","Psychology","KENMS","Accounting","ENM","Marine science","KOE",
    "Banking Studies","Business Administration","KIRKHS","Usuluddin","TAASL","Engine","ALA",
    "Biomedical science","BENL","IT","CTS","Econs","MHSC","Malcom","Human Sciences",
    "Communication","Diploma Nursing","Radiography","DIPLOMA TESL","Nursing"
]

def preprocess_input(data, encoders, columns, scaler):
    """Preprocess input data for prediction"""
    try:
        # Convert to DataFrame
        df = pd.DataFrame([data])
        
        # Convert all columns to proper types first
        for column in df.columns:
            if column == 'Age':
                df[column] = pd.to_numeric(df[column], errors='coerce')
            else:
                df[column] = df[column].astype(str)
        
        # Encode categorical variables
        for column in df.columns:
            if column in encoders:
                # Handle unseen categories
                if data[column] not in encoders[column].classes_:
                    # Add the new category to encoder
                    encoders[column].classes_ = np.append(encoders[column].classes_, data[column])
                df[column] = encoders[column].transform([data[column]])
        
        # Ensure all required columns are present
        for col in columns:
            if col not in df.columns:
                df[col] = 0
        
        # Reorder columns to match training data
        df = df[columns]
        
        # Convert to float for scaling
        df = df.astype(float)
        
        # Scale features
        df_scaled = scaler.transform(df)
        
        return df_scaled
    except Exception as e:
        st.error(f"Error in preprocessing: {str(e)}")
        return None

def get_top_contributing_features(data):
    """Get top 3 contributing features based on feature importance"""
    # Filter features that are present in the input and have non-zero importance
    contributing_features = []
    for feature, importance in FEATURE_IMPORTANCE.items():
        if importance > 0 and feature in data:
            contributing_features.append((feature, importance))
    
    # Sort by importance and get top 3
    contributing_features.sort(key=lambda x: x[1], reverse=True)
    return contributing_features[:3]

def create_circular_progress(percentage, is_high_risk):
    """Create circular progress indicator"""
    color = "#ff416c" if is_high_risk else "#00ff88"
    circumference = 2 * 3.14159 * 45
    stroke_dashoffset = circumference - (percentage / 100) * circumference
    
    svg = f"""
    <div class="circular-progress">
        <svg width="200" height="200">
            <circle cx="100" cy="100" r="45" stroke="rgba(255,255,255,0.1)" stroke-width="10" fill="none"/>
            <circle cx="100" cy="100" r="45" stroke="{color}" stroke-width="10" fill="none"
                    stroke-dasharray="{circumference}" stroke-dashoffset="{stroke_dashoffset}"
                    stroke-linecap="round"/>
        </svg>
        <div class="progress-text" style="color: {color}">{percentage}%</div>
    </div>
    """
    return svg

def main():
    # Load CSS
    load_css()
    
    # Load models
    model, encoders, columns, scaler = load_models()
    
    if model is None:
        st.stop()
    
    # Initialize session state for history
    if 'prediction_history' not in st.session_state:
        st.session_state.prediction_history = []
    
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="main-title">🧠 Student Mental Health Predictor</div>
        <div class="main-subtitle">ML-Powered Assessment</div>
        <div class="status-badge">✨ Model Active</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #00ff88; margin-bottom: 20px;">📝 Assessment Form</h3>', unsafe_allow_html=True)
        
        with st.form("prediction_form"):
            # Gender
            gender = st.selectbox(
                "Gender",
                ["Male", "Female"],
                key="gender"
            )
            
            # Age
            age = st.number_input(
                "Age",
                min_value=15,
                max_value=65,
                value=20,
                key="age"
            )
            
            # Course
            course = st.selectbox(
                "What is your course?",
                COURSE_OPTIONS,
                key="course"
            )
            
            # Year of Study
            year_of_study = st.selectbox(
                "Your current year of Study",
                ["year 1", "year 2", "year 3", "year 4"],
                key="year_of_study"
            )
            
            # CGPA
            cgpa = st.selectbox(
                "What is your CGPA?",
                ["0 - 1.99", "2.00 - 2.49", "2.50 - 2.99", "3.00 - 3.49", "3.50 - 4.00"],
                key="cgpa"
            )
            
            # Marital Status
            marital_status = st.selectbox(
                "Marital status",
                ["Yes", "No"],
                key="marital_status"
            )
            
            # Anxiety
            anxiety = st.selectbox(
                "Do you have Anxiety?",
                ["Yes", "No"],
                key="anxiety"
            )
            
            # Panic Attack
            panic_attack = st.selectbox(
                "Do you have Panic attack?",
                ["Yes", "No"],
                key="panic_attack"
            )
            
            # Specialist Treatment
            specialist = st.selectbox(
                "Did you seek any specialist for a treatment?",
                ["Yes", "No"],
                key="specialist"
            )
            
            # Submit Button
            submit_button = st.form_submit_button("� Predict", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if submit_button:
            # Prepare input data
            input_data = {
                "gender": gender,
                "Age": age,
                "What is your course?": course,
                "Your current year of Study": year_of_study,
                "What is your CGPA?": cgpa,
                "Marital status": marital_status,
                "Do you have Anxiety?": anxiety,
                "Do you have Panic attack?": panic_attack,
                "Did you seek any specialist for a treatment?": specialist
            }
            
            # Preprocess input
            processed_data = preprocess_input(input_data, encoders, columns, scaler)
            
            if processed_data is not None:
                # Make prediction
                prediction = model.predict(processed_data)[0]
                probability = model.predict_proba(processed_data)[0]
                
                # Determine result
                is_depressed = prediction == 1
                confidence = probability[1] * 100 if is_depressed else probability[0] * 100
                
                # Store in history
                history_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "prediction": "Depressed" if is_depressed else "Low Risk",
                    "confidence": confidence
                }
                st.session_state.prediction_history.insert(0, history_entry)
                
                # Keep only last 5 predictions
                if len(st.session_state.prediction_history) > 5:
                    st.session_state.prediction_history = st.session_state.prediction_history[:5]
                
                # Display Prediction Result
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<h3 style="color: #00ff88; margin-bottom: 20px;">🎯 Prediction Result</h3>', unsafe_allow_html=True)
                
                if is_depressed:
                    st.markdown('<div class="prediction-high-risk">⚠️ Likely Depressed</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="prediction-low-risk">✅ Low Risk</div>', unsafe_allow_html=True)
                
                # Confidence Score
                st.markdown('<h4 style="color: #00d4ff; margin: 20px 0; text-align: center;">Confidence Score</h4>', unsafe_allow_html=True)
                st.markdown(create_circular_progress(int(confidence), is_depressed), unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # AI Insights
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<h3 style="color: #00ff88; margin-bottom: 20px;">🧠 AI Insights</h3>', unsafe_allow_html=True)
                
                top_features = get_top_contributing_features(input_data)
                
                for i, (feature, importance) in enumerate(top_features):
                    importance_percentage = importance * 100
                    
                    st.markdown(f'''
                    <div class="insight-card" style="animation-delay: {i * 0.1}s;">
                        <div class="insight-title">🔹 {feature}</div>
                        <div class="insight-importance">
                            <div class="insight-importance-fill" style="width: {importance_percentage * 20}%;"></div>
                        </div>
                        <div style="font-size: 0.85rem; color: #888; margin-bottom: 8px;">
                            Importance: {importance_percentage:.1f}%
                        </div>
                        <div class="insight-explanation">
                            {FEATURE_EXPLANATIONS.get(feature, "No explanation available.")}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            # Default state when no prediction made
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('''
            <div style="text-align: center; padding: 40px;">
                <div style="font-size: 3rem; margin-bottom: 20px;">🤖</div>
                <h3 style="color: #00ff88; margin-bottom: 15px;">Ready for Assessment</h3>
                <p style="color: #b8b8b8;">Complete the form to receive your mental health prediction and AI-powered insights.</p>
            </div>
            ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # History Section
    if st.session_state.prediction_history:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #00ff88; margin-bottom: 20px;">📊 Recent Predictions</h3>', unsafe_allow_html=True)
        
        for entry in st.session_state.prediction_history:
            risk_class = "history-high-risk" if entry["prediction"] == "Depressed" else "history-low-risk"
            
            st.markdown(f'''
            <div class="history-card">
                <div>
                    <div style="font-weight: 600; margin-bottom: 5px;">{entry["prediction"]}</div>
                    <div class="history-time">{entry["timestamp"]}</div>
                </div>
                <div class="history-result {risk_class}">
                    {entry["confidence"]:.1f}% confidence
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()