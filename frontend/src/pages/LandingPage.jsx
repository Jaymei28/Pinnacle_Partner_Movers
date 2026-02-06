import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
    return (
        <div className="landing-page">
            <div className="landing-hero">
                <div className="landing-content">
                    <h1 className="landing-title">Find Your Next Opportunity</h1>
                    <p className="landing-subtitle">
                        Discover amazing job opportunities tailored to your skills and experience
                    </p>
                    <div className="landing-cta">
                        <Link to="/login" className="btn btn-primary btn-large">
                            Get Started
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LandingPage;
