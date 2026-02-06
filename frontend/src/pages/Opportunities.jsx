import React, { useState, useEffect } from 'react';
import axios from 'axios';
import searchIcon from '../images/search.svg';
import jobDetailsIcon from '../images/jobdetails.svg';

const API_URL = 'http://localhost:8000/api/jobs/';

const Opportunities = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(false);
    const [selectedJob, setSelectedJob] = useState(null);
    const [error, setError] = useState(null);
    const [zipCode, setZipCode] = useState('');
    const [searchZip, setSearchZip] = useState('');

    const fetchJobs = async (driverZip = '') => {
        setLoading(true);
        setError(null);
        try {
            const url = driverZip
                ? `${API_URL}?zip_code=${driverZip}`
                : API_URL;
            const response = await axios.get(url);
            setJobs(response.data);
        } catch (err) {
            console.error('Error fetching jobs:', err);
            setError('Technical issue connecting to the job board. Please try again later.');
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = () => {
        if (zipCode.trim()) {
            setSearchZip(zipCode.trim());
            fetchJobs(zipCode.trim());
        }
    };

    const handleClearSearch = () => {
        setZipCode('');
        setSearchZip('');
        fetchJobs();
    };

    const renderOrientationTable = (text) => {
        if (!text) return null;
        let processedText = String(text).replace(/\\n/g, '\n');
        const lines = processedText.split('\n').map(l => l.trim()).filter(l => l.length > 0);

        // Basic detection if it's a table based on header keywords
        const headerKeywords = ['city', 'state', 'days', 'time', 'address', 'terminal'];
        const isTable = lines.length > 1 && headerKeywords.some(k => lines[0].toLowerCase().includes(k));

        if (!isTable) return renderFormattedText(text);

        const rows = [];
        let startIdx = 1; // Skip header

        for (let i = startIdx; i < lines.length; i++) {
            const line = lines[i];

            // Primary data lines usually have a Time or typical State code
            const hasTime = /(\d{1,2}:\d{2}\s*(?:AM|PM))/i.test(line);
            const hasState = /\b[A-Z]{2}\b/.test(line);

            if (hasTime || hasState) {
                let entryLine = line;
                // Check if next line is a continuation (address)
                if (i + 1 < lines.length) {
                    const nextLine = lines[i + 1];
                    const nextHasTime = /(\d{1,2}:\d{2}\s*(?:AM|PM))/i.test(nextLine);
                    const nextHasState = /\b[A-Z]{2}\b/.test(nextLine);
                    if (!nextHasTime && !nextHasState) {
                        entryLine += ' ' + nextLine;
                        i++; // Skip the next line
                    }
                }

                // Parse the combined line
                const timeMatch = entryLine.match(/(\d{1,2}:\d{2}\s*(?:AM|PM))/i);
                if (timeMatch) {
                    const time = timeMatch[1];
                    const timeParts = entryLine.split(time);
                    const beforeTime = timeParts[0].trim();
                    const afterTime = timeParts[1].trim();

                    // Split beforeTime into City/State and Days
                    const stateMatch = beforeTime.match(/\b([A-Z]{2})\b/);
                    let cityState = beforeTime;
                    let days = '';
                    if (stateMatch) {
                        const state = stateMatch[1];
                        const stIdx = beforeTime.lastIndexOf(state);
                        cityState = beforeTime.substring(0, stIdx + 2).trim();
                        days = beforeTime.substring(stIdx + 2).trim();
                    }

                    rows.push({ cityState, days, time, address: afterTime });
                } else {
                    rows.push({ cityState: line, days: '', time: '', address: '' });
                }
            }
        }

        return (
            <div className="orientation-table-wrapper">
                <table className="orientation-table">
                    <thead>
                        <tr>
                            <th>City / State</th>
                            <th>Days</th>
                            <th>Start Time</th>
                            <th>Terminal Address</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows.map((row, idx) => (
                            <tr key={idx}>
                                <td className="cell-city">{row.cityState}</td>
                                <td className="cell-days">{row.days}</td>
                                <td className="cell-time">{row.time}</td>
                                <td className="cell-address">{row.address}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        );
    };

    const renderFormattedText = (text) => {
        if (!text) return null;

        // Split by newline and filter out empty lines
        let processedText = String(text).replace(/\\n/g, '\n');
        const lines = processedText.split('\n').map(line => line.trim()).filter(line => line.length > 0);

        if (lines.length === 0) return null;

        return (
            <>
                {lines.map((line, index) => {
                    // Remove bullets and bold markers
                    const cleanLine = line.replace(/^[•\*\-\s]+/, '').replace(/\*\*/g, '');

                    if (!cleanLine) return null;

                    // Section Header (ALL CAPS)
                    if (cleanLine.length >= 3 && cleanLine === cleanLine.toUpperCase() && !cleanLine.includes(':')) {
                        return (
                            <div key={index} className="lane-section-title" style={{ marginTop: index > 0 ? '0.6rem' : '0', marginBottom: '0.25rem' }}>
                                {cleanLine}
                            </div>
                        );
                    }

                    // Labeled Item
                    if (cleanLine.includes(':')) {
                        const colonIndex = cleanLine.indexOf(':');
                        const label = cleanLine.substring(0, colonIndex).trim();
                        const value = cleanLine.substring(colonIndex + 1).trim();

                        return (
                            <div key={index} className="lane-item">
                                <span className="lane-label">{label}:</span>
                                <span className="lane-value">{value}</span>
                            </div>
                        );
                    }

                    // Regular text
                    return (
                        <div key={index} className="lane-item">
                            <span className="lane-text">{cleanLine}</span>
                        </div>
                    );
                })}
            </>
        );
    };

    useEffect(() => {
        fetchJobs();
    }, []);

    // parseJobTags, formatDescription, and parseLaneInformation sections removed for better performance and consistency.


    return (
        <div className="opportunities-view">
            <div className="job-search-header">
                <h2>Job Search Filter</h2>
                <p className="search-subtitle">
                    Searching by the drivers zip code on their CDL will result in showing you only the positions they are in the hiring radius for.
                </p>

                <div className="search-bar-container">
                    <input
                        type="text"
                        className="search-input"
                        placeholder="Search by the zip code listed on the drivers CDL"
                        value={zipCode}
                        onChange={(e) => setZipCode(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                        maxLength="5"
                    />
                    <button className="btn-search" onClick={handleSearch}>
                        <img src={searchIcon} alt="" className="search-icon" />
                        Search
                    </button>
                    {searchZip && (
                        <button className="btn-clear-search" onClick={handleClearSearch}>
                            Clear
                        </button>
                    )}
                </div>
            </div>

            {loading ? (
                <div className="status-msg">Loading jobs...</div>
            ) : error ? (
                <div className="status-msg error">{error}</div>
            ) : (
                <div className="job-list-container">
                    {jobs.length === 0 ? (
                        <div className="status-msg">
                            {searchZip
                                ? `No jobs found within hiring radius of ${searchZip}. Try a different zip code.`
                                : 'No jobs available at the moment.'}
                        </div>
                    ) : (
                        jobs.map(job => {
                            // Use structured fields from database instead of parsing description
                            const states = job.states_covered ? job.states_covered.split(',').map(s => s.trim()) : [];
                            const carrierName = job.carrier?.name || 'Unknown Carrier';

                            return (
                                <div key={job.id} className="job-list-item">
                                    <div className="job-item-content">
                                        <div className="job-tags-left">
                                            <span className="tag tag-company">{carrierName}</span>
                                            {job.home_time && (
                                                <span className="tag tag-schedule">{job.home_time}</span>
                                            )}
                                            {job.freight_type && (
                                                <span className="tag tag-freight">{job.freight_type}</span>
                                            )}
                                        </div>

                                        <div className="job-item-main">
                                            <h3 className="job-item-title">{job.title}</h3>
                                            {job.salary && <p className="job-item-pay">{job.salary}</p>}
                                        </div>

                                        <div className="job-tags-center">
                                            {job.experience_required && (
                                                <span className="tag tag-experience">{job.experience_required}</span>
                                            )}
                                            {job.driver_type && (
                                                <span className="tag tag-driver-type">{job.driver_type}</span>
                                            )}
                                            {states.length > 0 && states.slice(0, 3).map((state, idx) => (
                                                <span key={idx} className="tag tag-state">{state}</span>
                                            ))}
                                        </div>

                                        <div className="job-item-actions">
                                            <button
                                                className="btn-job-details"
                                                onClick={() => setSelectedJob(job)}
                                            >
                                                <img src={jobDetailsIcon} alt="" className="btn-icon" />
                                                Job Details
                                            </button>
                                            <button className="btn-more">⋯</button>
                                        </div>
                                    </div>
                                </div>
                            );
                        })
                    )}
                </div>
            )}

            {selectedJob && (
                <div className="modal-overlay" onClick={() => setSelectedJob(null)}>
                    <div className="modal-content job-details-modal" onClick={e => e.stopPropagation()}>
                        <button className="close-btn" onClick={() => setSelectedJob(null)}>&times;</button>

                        {/* Header */}
                        <div className="job-modal-header">
                            <div className="job-modal-tags">
                                {selectedJob.carrier?.name && (
                                    <span className="tag tag-company">{selectedJob.carrier.name}</span>
                                )}
                                {selectedJob.equipment_type && (
                                    <span className="tag tag-equipment">{selectedJob.equipment_type}</span>
                                )}
                            </div>
                            <h1 className="job-modal-title">{selectedJob.title}</h1>
                            <p className="job-modal-location">
                                <svg style={{ width: '16px', height: '16px', display: 'inline-block', marginRight: '4px', verticalAlign: 'middle' }} viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" />
                                </svg>
                                {selectedJob.state}
                            </p>
                        </div>

                        {/* SECTION 1: Basic Information */}
                        <div className="job-details-section">
                            <h4 className="section-header">Basic Information</h4>
                            <div className="job-info-grid">
                                {selectedJob.pay_range && <div className="info-item"><h4>Pay Range</h4><p>{selectedJob.pay_range}</p></div>}
                                {selectedJob.average_weekly_pay && <div className="info-item"><h4>Avg. Weekly Pay</h4><p>{selectedJob.average_weekly_pay}</p></div>}
                                {selectedJob.salary && <div className="info-item"><h4>Pay Info</h4><p>{selectedJob.salary}</p></div>}
                                {selectedJob.pay_type && <div className="info-item"><h4>Pay Type</h4><p>{selectedJob.pay_type}</p></div>}
                                {selectedJob.short_haul_pay && <div className="info-item"><h4>Short Haul Pay</h4><p>{selectedJob.short_haul_pay}</p></div>}
                                {selectedJob.stop_pay && <div className="info-item"><h4>Stop Pay</h4><p>{selectedJob.stop_pay}</p></div>}
                                {selectedJob.bonus_offer && <div className="info-item"><h4>Bonus</h4><p>{selectedJob.bonus_offer}</p></div>}
                                {selectedJob.exact_home_time && <div className="info-item"><h4>Exact Home Time</h4><p>{selectedJob.exact_home_time}</p></div>}
                                {selectedJob.home_time && <div className="info-item"><h4>Home Time</h4><p>{selectedJob.home_time}</p></div>}
                                {selectedJob.load_unload_type && <div className="info-item"><h4>Load/Unload</h4><p>{selectedJob.load_unload_type}</p></div>}
                                {selectedJob.unload_pay && <div className="info-item"><h4>Unload Pay</h4><p>{selectedJob.unload_pay}</p></div>}
                            </div>
                        </div>

                        {/* SECTION 2: Lane Information */}
                        <div className="lane-info-container">
                            <div className="lane-side-label">Lane Information</div>
                            <div className="lane-info-content">
                                {selectedJob.job_details && (
                                    <div className="lane-section">
                                        <h5 className="lane-section-title">Job Details</h5>
                                        <div className="lane-section-content">{renderFormattedText(selectedJob.job_details)}</div>
                                    </div>
                                )}
                                {selectedJob.account_overview && (
                                    <div className="lane-section">
                                        <h5 className="lane-section-title">Account Overview</h5>
                                        <div className="lane-section-content">{renderFormattedText(selectedJob.account_overview)}</div>
                                    </div>
                                )}
                                {selectedJob.administrative_details && (
                                    <div className="lane-section">
                                        <h5 className="lane-section-title">Administrative Details</h5>
                                        <div className="lane-section-content">{renderFormattedText(selectedJob.administrative_details)}</div>
                                    </div>
                                )}
                                {selectedJob.description && (
                                    <div className="lane-section">
                                        <h5 className="lane-section-title">Additional Information</h5>
                                        <div className="lane-section-content">{renderFormattedText(selectedJob.description)}</div>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* SECTION 3: Company Benefits & Info */}
                        {selectedJob.carrier && (
                            <div className="lane-info-container">
                                <div className="lane-side-label">Company Benefits & Info</div>
                                <div className="lane-info-content">
                                    {selectedJob.carrier.benefit_medical_dental_vision && (
                                        <div className="lane-section">
                                            <h5 className="lane-section-title">Medical/Dental/Vision</h5>
                                            <div className="lane-section-content">{renderFormattedText(selectedJob.carrier.benefit_medical_dental_vision)}</div>
                                        </div>
                                    )}
                                    {selectedJob.carrier.benefit_401k && (
                                        <div className="lane-section">
                                            <h5 className="lane-section-title">401(k)</h5>
                                            <div className="lane-section-content">{renderFormattedText(selectedJob.carrier.benefit_401k)}</div>
                                        </div>
                                    )}
                                    {selectedJob.carrier.benefit_paid_vacation && (
                                        <div className="lane-section">
                                            <h5 className="lane-section-title">Paid Vacation</h5>
                                            <div className="lane-section-content">{renderFormattedText(selectedJob.carrier.benefit_paid_vacation)}</div>
                                        </div>
                                    )}
                                    {selectedJob.carrier.benefit_stock_purchase && (
                                        <div className="lane-section">
                                            <h5 className="lane-section-title">Stock Purchase</h5>
                                            <div className="lane-section-content">{renderFormattedText(selectedJob.carrier.benefit_stock_purchase)}</div>
                                        </div>
                                    )}
                                    {selectedJob.carrier.benefit_prescription_drug && (
                                        <div className="lane-section">
                                            <h5 className="lane-section-title">Prescription Drugs</h5>
                                            <div className="lane-section-content">{renderFormattedText(selectedJob.carrier.benefit_prescription_drug)}</div>
                                        </div>
                                    )}
                                    {selectedJob.carrier.benefit_tuition_program && (
                                        <div className="lane-section">
                                            <h5 className="lane-section-title">Tuition Program</h5>
                                            <div className="lane-section-content">{renderFormattedText(selectedJob.carrier.benefit_tuition_program)}</div>
                                        </div>
                                    )}
                                    {selectedJob.carrier.benefit_other && (
                                        <div className="lane-section">
                                            <h5 className="lane-section-title">Other Benefits</h5>
                                            <div className="lane-section-content">{renderFormattedText(selectedJob.carrier.benefit_other)}</div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}

                        {/* SECTION 4: Orientation */}
                        {(selectedJob.orientation_details || selectedJob.orientation_table) && (
                            <div className="lane-info-container">
                                <div className="lane-side-label">Orientation</div>
                                <div className="lane-info-content">
                                    {selectedJob.orientation_details && (
                                        <div className="lane-section">
                                            <div className="lane-section-content">{renderFormattedText(selectedJob.orientation_details)}</div>
                                        </div>
                                    )}
                                    {selectedJob.orientation_table && (
                                        <div className="lane-section">
                                            <div className="orientation-table-container">
                                                <div className="orientation-table-data">{renderOrientationTable(selectedJob.orientation_table)}</div>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}

                        {/* SECTION 5: Job Requirements */}
                        <div className="job-details-section">
                            <h4 className="section-header">Job Requirements</h4>
                            <div className="requirements-badges">
                                {selectedJob.trainees_accepted && <div className="req-badge"><strong>Trainees Accepted:</strong> {selectedJob.trainees_accepted}</div>}
                                {selectedJob.account_type && <div className="req-badge"><strong>Account Type:</strong> {selectedJob.account_type}</div>}
                                {selectedJob.cameras && <div className="req-badge"><strong>Cameras:</strong> {selectedJob.cameras}</div>}
                                {selectedJob.driver_types && <div className="req-badge"><strong>Driver Types:</strong> {selectedJob.driver_types}</div>}
                                {selectedJob.drug_test_type && <div className="req-badge"><strong>Drug Test:</strong> {selectedJob.drug_test_type}</div>}
                                {selectedJob.experience_levels && <div className="req-badge"><strong>Experience:</strong> {selectedJob.experience_levels}</div>}
                                {selectedJob.freight_types && <div className="req-badge"><strong>Freight Types:</strong> {selectedJob.freight_types}</div>}
                                {selectedJob.sap_required && <div className="req-badge"><strong>SAP Required:</strong> {selectedJob.sap_required}</div>}
                                {selectedJob.transmissions && <div className="req-badge"><strong>Transmissions:</strong> {selectedJob.transmissions}</div>}
                                {selectedJob.states && <div className="req-badge"><strong>States:</strong> {selectedJob.states}</div>}
                            </div>
                        </div>

                        {/* Action Buttons */}
                        <div className="modal-actions">
                            <button
                                className="btn-primary btn-apply"
                                onClick={() => window.open(selectedJob.apply_link || '#', '_blank')}
                            >
                                Apply for this Position
                            </button>
                            <button
                                className="btn-secondary"
                                onClick={() => setSelectedJob(null)}
                            >
                                Close
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Opportunities;

