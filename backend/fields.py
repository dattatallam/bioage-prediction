GROUPS = [
    ("Health measurements", [
        ("chronological_age", "Age (years)", "number", "e.g. 45"),
        ("BMI", "BMI", "number", "e.g. 25.3"),
        ("weight", "Weight (kg)", "number", "e.g. 70"),
        ("height", "Height (cm)", "number", "e.g. 170"),
        ("waist", "Waist (cm)", "number", "e.g. 90"),
        ("pulse", "Pulse (beats/min)", "number", "e.g. 72"),
        ("systolic_bp", "Systolic BP (mmHg)", "number", "e.g. 120"),
        ("diastolic_bp", "Diastolic BP (mmHg)", "number", "e.g. 80"),
        ("total_cholesterol", "Total cholesterol (mg/dL)", "number", "e.g. 185"),
        ("hemoglobin", "Hemoglobin (g/dL)", "number", "e.g. 14"),
        ("hematocrit", "Hematocrit (%)", "number", "e.g. 42"),
        ("creatinine", "Creatinine (mg/dL)", "number", "e.g. 1.0"),
        ("uric_acid", "Uric acid (mg/dL)", "number", "e.g. 5.3"),
    ]),
    ("Lifestyle", [
        ("gender", "Gender", "select", [("0", "Male"), ("1", "Female")]),
        ("smoking_status", "Smoking status", "select", [("0", "Never"), ("1", "Former"), ("2", "Current")]),
        ("sleep_category", "Sleep category", "select", [("0", "Less than 6 hours"), ("1", "6 to under 9 hours"), ("2", "9 hours or more")]),
        ("physical_activity", "Physical activity", "select", [("0", "None"), ("1", "Some"), ("2", "Active")]),
    ]),
]
CODES = [c for _, fs in GROUPS for c, *_ in fs]

