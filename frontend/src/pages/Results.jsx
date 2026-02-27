import { useLocation, useNavigate } from 'react-router-dom';

const LEVEL_CONFIG = {
    Low: {
        color: '#16a34a',
        bg: '#f0fdf4',
        border: '#bbf7d0',
        label: 'Low Risk',
        icon: (
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#16a34a" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 12l2 2 4-4" /><circle cx="12" cy="12" r="10" /></svg>
        ),
    },
    Moderate: {
        color: '#ca8a04',
        bg: '#fefce8',
        border: '#fde68a',
        label: 'Moderate Risk',
        icon: (
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ca8a04" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z" /><line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" /></svg>
        ),
    },
    High: {
        color: '#dc2626',
        bg: '#fef2f2',
        border: '#fecaca',
        label: 'High Risk',
        icon: (
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#dc2626" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10" /><line x1="15" y1="9" x2="9" y2="15" /><line x1="9" y1="9" x2="15" y2="15" /></svg>
        ),
    },
};

function Results() {
    const location = useLocation();
    const navigate = useNavigate();
    const result = location.state?.result;

    if (!result) {
        return (
            <div className="page results-page">
                <div className="results-container">
                    <div className="results-empty">
                        <h2>No Results</h2>
                        <p>Please complete an assessment first.</p>
                        <button className="btn btn-primary" onClick={() => navigate('/assess')}>
                            Go to Assessment
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    const config = LEVEL_CONFIG[result.risk_level] || LEVEL_CONFIG.Moderate;

    return (
        <div className="page results-page">
            <div className="results-container">
                <div className="results-header">
                    <a href="/assess" className="assess-back">&larr; New Assessment</a>
                    <h1>Triage Results</h1>
                </div>

                {/* Risk Level Card */}
                <div
                    className="result-card result-card--level"
                    style={{ background: config.bg, borderColor: config.border }}
                >
                    <div className="result-level-row">
                        <div className="result-level-icon">{config.icon}</div>
                        <div>
                            <div className="result-level-label" style={{ color: config.color }}>
                                {config.label}
                            </div>
                            <div className="result-level-score">
                                Risk Score: <strong>{result.risk_score}</strong>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Explanation */}
                <div className="result-card">
                    <h3>
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10" /><line x1="12" y1="16" x2="12" y2="12" /><line x1="12" y1="8" x2="12.01" y2="8" /></svg>
                        Analysis
                    </h3>
                    <p className="result-explanation">{result.explanation}</p>
                </div>

                {/* Detected Symptoms */}
                {result.detected_symptoms && result.detected_symptoms.length > 0 && (
                    <div className="result-card">
                        <h3>
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" /><polyline points="14 2 14 8 20 8" /><line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" /></svg>
                            Detected Symptoms
                        </h3>
                        <div className="symptom-tags">
                            {result.detected_symptoms.map((s) => (
                                <span key={s} className="symptom-tag">{s}</span>
                            ))}
                        </div>
                    </div>
                )}

                {/* Recommended Action */}
                <div className="result-card">
                    <h3>
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" /><polyline points="22 4 12 14.01 9 11.01" /></svg>
                        Recommended Action
                    </h3>
                    <p>{result.recommended_action}</p>
                </div>

                {/* Disclaimer */}
                <div className="disclaimer">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" /></svg>
                    <span>
                        Acuvia is a triage support tool and not a medical diagnosis system.
                        Always consult a licensed medical professional.
                    </span>
                </div>

                <div className="results-actions">
                    <button className="btn btn-primary" onClick={() => navigate('/assess')}>
                        New Assessment
                    </button>
                    <button className="btn btn-secondary" onClick={() => navigate('/')}>
                        Home
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Results;
