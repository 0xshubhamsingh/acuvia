import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const COMORBIDITY_OPTIONS = [
    'Diabetes',
    'Hypertension',
    'Heart Disease',
    'Asthma',
    'COPD',
    'Chronic Kidney Disease',
    'Cancer',
    'Obesity',
    'Liver Disease',
    'Immunodeficiency',
];

function Assessment() {
    const navigate = useNavigate();
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('');
    const [comorbidities, setComorbidities] = useState([]);
    const [symptoms, setSymptoms] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const toggleComorbidity = (item) => {
        setComorbidities((prev) =>
            prev.includes(item) ? prev.filter((c) => c !== item) : [...prev, item]
        );
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (!age || !gender || !symptoms.trim()) {
            setError('Please fill in all required fields.');
            return;
        }

        setLoading(true);

        try {
            const apiUrl = import.meta.env.VITE_API_URL || '';
            const res = await fetch(`${apiUrl}/assess`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    age: parseInt(age, 10),
                    gender,
                    comorbidities: comorbidities.map((c) => c.toLowerCase()),
                    symptoms,
                }),
            });

            if (!res.ok) throw new Error('Assessment failed. Please try again.');

            const data = await res.json();
            navigate('/results', { state: { result: data } });
        } catch (err) {
            setError(err.message || 'Something went wrong.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page assess-page">
            <div className="assess-container">
                <div className="assess-header">
                    <a href="/" className="assess-back">&larr; Back</a>
                    <h1>Patient Assessment</h1>
                    <p>Enter patient details and describe observed symptoms for AI-powered triage analysis.</p>
                </div>

                <form className="assess-form" onSubmit={handleSubmit}>
                    {/* Row: Age + Gender */}
                    <div className="form-row">
                        <div className="form-group">
                            <label htmlFor="age">Age <span className="required">*</span></label>
                            <input
                                id="age"
                                type="number"
                                min="0"
                                max="120"
                                placeholder="e.g. 45"
                                value={age}
                                onChange={(e) => setAge(e.target.value)}
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="gender">Gender <span className="required">*</span></label>
                            <select id="gender" value={gender} onChange={(e) => setGender(e.target.value)}>
                                <option value="">Select gender</option>
                                <option value="male">Male</option>
                                <option value="female">Female</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                    </div>

                    {/* Comorbidities */}
                    <div className="form-group">
                        <label>Known Conditions</label>
                        <div className="chips-container">
                            {COMORBIDITY_OPTIONS.map((item) => (
                                <button
                                    type="button"
                                    key={item}
                                    className={`chip ${comorbidities.includes(item) ? 'chip--active' : ''}`}
                                    onClick={() => toggleComorbidity(item)}
                                >
                                    {comorbidities.includes(item) && (
                                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12" /></svg>
                                    )}
                                    {item}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Symptoms */}
                    <div className="form-group">
                        <label htmlFor="symptoms">Symptom Description <span className="required">*</span></label>
                        <textarea
                            id="symptoms"
                            rows="5"
                            placeholder="Describe all symptoms in detail, e.g. 'Patient reports persistent chest pain with sweating, difficulty breathing, and dizziness for the past 2 hours...'"
                            value={symptoms}
                            onChange={(e) => setSymptoms(e.target.value)}
                        />
                    </div>

                    {error && <div className="form-error">{error}</div>}

                    <button type="submit" className="btn btn-primary btn-lg btn-full" disabled={loading}>
                        {loading ? (
                            <span className="loading-wrapper">
                                <span className="spinner" />
                                Analyzing…
                            </span>
                        ) : (
                            'Run Triage Assessment'
                        )}
                    </button>
                </form>
            </div>
        </div>
    );
}

export default Assessment;
