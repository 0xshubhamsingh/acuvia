import { useNavigate } from 'react-router-dom';

function Home() {
    const navigate = useNavigate();

    return (
        <div className="page home-page">
            <div className="home-container">
                {/* Floating decorative shapes */}
                <div className="home-bg-shape home-bg-shape--1" />
                <div className="home-bg-shape home-bg-shape--2" />
                <div className="home-bg-shape home-bg-shape--3" />

                <div className="home-content">
                    <div className="home-badge">AI-Powered Clinical Decision Support</div>

                    <h1 className="home-title">
                        <span className="home-title-brand">Acuvia</span>
                    </h1>

                    <p className="home-tagline">Precision Triage. Powered by AI.</p>

                    <p className="home-description">
                        An intelligent symptom triage system that analyzes patient data,
                        predicts severity levels using machine learning, and delivers
                        explainable risk classifications in seconds.
                    </p>

                    <button className="btn btn-primary btn-lg" onClick={() => navigate('/assess')}>
                        <span>Start Assessment</span>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <line x1="5" y1="12" x2="19" y2="12" />
                            <polyline points="12 5 19 12 12 19" />
                        </svg>
                    </button>

                    <div className="home-features">
                        <div className="home-feature">
                            <div className="home-feature-icon">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Z" /><path d="M12 6v6l4 2" /></svg>
                            </div>
                            <div>
                                <div className="home-feature-title">Real-Time Analysis</div>
                                <div className="home-feature-desc">Instant risk assessment powered by ML</div>
                            </div>
                        </div>
                        <div className="home-feature">
                            <div className="home-feature-icon">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M9 12l2 2 4-4" /><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Z" /></svg>
                            </div>
                            <div>
                                <div className="home-feature-title">Explainable Results</div>
                                <div className="home-feature-desc">Transparent reasoning for every decision</div>
                            </div>
                        </div>
                        <div className="home-feature">
                            <div className="home-feature-icon">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78Z" /></svg>
                            </div>
                            <div>
                                <div className="home-feature-title">Patient Safety</div>
                                <div className="home-feature-desc">Critical symptom detection built-in</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Home;
