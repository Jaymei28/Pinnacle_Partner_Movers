import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/carriers/';

const Carriers = () => {
    const [carriers, setCarriers] = useState([]);
    const [loading, setLoading] = useState(false);
    const [selectedCarrier, setSelectedCarrier] = useState(null);
    const [error, setError] = useState(null);

    const fetchCarriers = async () => {
        setLoading(true);
        setError(null);
        try {
            // Add timestamp to prevent caching
            const response = await axios.get(`${API_URL}?t=${Date.now()}`, {
                headers: {
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
            });
            setCarriers(response.data);
        } catch (err) {
            console.error('Error fetching carriers:', err);
            setError('Technical issue connecting to the server. Please try again later.');
        } finally {
            setLoading(false);
        }
    };

    const renderGenericTable = (text) => {
        if (!text) return null;
        let processedText = String(text).replace(/\\n/g, '\n');
        const lines = processedText.split('\n').map(l => l.trim()).filter(l => l.length > 0);

        if (lines.length <= 1) return renderFormattedText(text);

        // DELIMITER DETECTION (Pipe or Tab)
        const firstLine = lines[0];
        let delimiter = null;
        if (firstLine.includes('|')) delimiter = '|';
        else if (firstLine.includes('\t')) delimiter = '\t';

        // CASE 1: ORIENTATION TABLE (Specific Keywords)
        const orientationKeywords = ['city', 'state', 'days', 'time', 'address', 'terminal'];
        const isOrientationTable = orientationKeywords.some(k => firstLine.toLowerCase().includes(k));

        if (isOrientationTable) {
            return renderOrientationTable(text);
        }

        // CASE 2: GENERIC TABLE (Delimited)
        if (delimiter) {
            const headers = lines[0].split(delimiter).map(h => h.trim());
            const rows = lines.slice(1).map(line => line.split(delimiter).map(c => c.trim()));

            return (
                <div className="orientation-table-wrapper">
                    <table className="orientation-table">
                        <thead>
                            <tr>
                                {headers.map((h, i) => (
                                    <th key={i}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                            {h.toLowerCase().includes('presentation') && <i className="lucide-refresh-cw" style={{ fontSize: '0.9rem', opacity: 0.7 }}></i>}
                                            {h.toLowerCase().includes('topic') && <i className="lucide-git-branch" style={{ fontSize: '0.9rem', opacity: 0.7 }}></i>}
                                            {h.toLowerCase().includes('description') && <i className="lucide-file-text" style={{ fontSize: '0.9rem', opacity: 0.7 }}></i>}
                                            {h}
                                        </div>
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {rows.map((row, idx) => (
                                <tr key={idx}>
                                    {row.map((cell, i) => (
                                        <td key={i} style={i === 0 ? { fontWeight: '500', color: 'var(--text-dark)' } : {}}>
                                            {renderFormattedText(cell)}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            );
        }

        // FALLBACK: Just formatted text
        return renderFormattedText(text);
    };

    const renderOrientationTable = (text) => {
        if (!text) return null;
        let processedText = String(text).replace(/\\n/g, '\n');
        const lines = processedText.split('\n').map(l => l.trim()).filter(l => l.length > 0);

        const headerKeywords = ['city', 'state', 'days', 'time', 'address', 'terminal'];
        const isTable = lines.length > 1 && headerKeywords.some(k => lines[0].toLowerCase().includes(k));

        if (!isTable) return renderFormattedText(text);

        const rows = [];
        let startIdx = 1;

        for (let i = startIdx; i < lines.length; i++) {
            const line = lines[i];
            const hasTime = /(\d{1,2}:\d{2}\s*(?:AM|PM))/i.test(line);
            const hasState = /\b[A-Z]{2}\b/.test(line);

            if (hasTime || hasState) {
                let entryLine = line;
                if (i + 1 < lines.length) {
                    const nextLine = lines[i + 1];
                    const nextHasTime = /(\d{1,2}:\d{2}\s*(?:AM|PM))/i.test(nextLine);
                    const nextHasState = /\b[A-Z]{2}\b/.test(nextLine);
                    if (!nextHasTime && !nextHasState) {
                        entryLine += ' ' + nextLine;
                        i++;
                    }
                }

                const timeMatch = entryLine.match(/(\d{1,2}:\d{2}\s*(?:AM|PM))/i);
                if (timeMatch) {
                    const time = timeMatch[1];
                    const timeParts = entryLine.split(time);
                    const beforeTime = timeParts[0].trim();
                    const afterTime = timeParts[1].trim();

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

    useEffect(() => {
        fetchCarriers();
    }, []);

    const renderFormattedText = (text) => {
        if (!text) return null;

        // Split by newline and filter out empty lines
        let processedText = String(text).replace(/\\n/g, '\n');
        const lines = processedText.split('\n').map(line => line.trim()).filter(line => line.length > 0);

        if (lines.length === 0) return null;

        return (
            <div className="lane-section-content">
                {lines.map((line, index) => {
                    const isBullet = /^[•\*\-]/.test(line);
                    const isBoldMarkdown = line.startsWith('**') && line.endsWith('**');

                    const cleanLine = line.replace(/^[•\*\-\s]+/, '').replace(/\*\*/g, '');

                    if (!cleanLine) return null;

                    // Improved Header Detection:
                    // Headers are usually short, don't have bullets, and DON'T end in a period.
                    const endsWithPunctuation = /[.\?!]$/.test(cleanLine.trim());
                    const isShort = cleanLine.length < 50;
                    const isProbablyProperty = cleanLine.includes(':') && cleanLine.indexOf(':') < 25;

                    const isHeader = isBoldMarkdown || (!isBullet && isShort && !endsWithPunctuation && !isProbablyProperty);

                    if (isHeader) {
                        return (
                            <div key={index} className="lane-section-title" style={{ fontWeight: '800', marginTop: index > 0 ? '1.25rem' : '0' }}>
                                {cleanLine}
                            </div>
                        );
                    }

                    if (cleanLine.includes(':')) {
                        const colonIndex = cleanLine.indexOf(':');
                        const label = cleanLine.substring(0, colonIndex).trim();
                        const valueParts = cleanLine.substring(colonIndex + 1).trim().split('**');

                        return (
                            <div key={index} className={isBullet ? "lane-item" : "lane-text-line"}>
                                <span className="lane-label" style={{ fontWeight: '700' }}>{label}:</span>
                                <span className="lane-value">
                                    {valueParts.map((part, i) => i % 2 === 1 ? <strong key={i}>{part}</strong> : part)}
                                </span>
                            </div>
                        );
                    }

                    const parts = cleanLine.split('**');
                    return (
                        <div key={index} className={isBullet ? "lane-item" : "lane-text-line"}>
                            <span className="lane-text">
                                {parts.map((part, i) => i % 2 === 1 ? <strong key={i}>{part}</strong> : part)}
                            </span>
                        </div>
                    );
                })}
            </div>
        );
    };

    return (
        <div className="opportunities-view">
            <div className="carriers-header">
                <h2>Carriers</h2>
                <p className="carriers-subtitle">
                    Browse all trucking companies and their benefits packages.
                </p>
            </div>

            {loading ? (
                <div className="status-msg">Loading carriers...</div>
            ) : error ? (
                <div className="status-msg error">{error}</div>
            ) : (
                <div className="carriers-grid">
                    {carriers.length === 0 ? (
                        <div className="status-msg">No carriers available at the moment.</div>
                    ) : (
                        carriers.map(carrier => (
                            <div key={carrier.id} className="carrier-card" onClick={() => setSelectedCarrier(carrier)}>
                                <div className="carrier-card-header">
                                    <h3>{carrier.name}</h3>
                                    {carrier.website && (
                                        <a
                                            href={carrier.website}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            onClick={(e) => e.stopPropagation()}
                                            className="carrier-website-link"
                                        >
                                            Website →
                                        </a>
                                    )}
                                </div>
                                {carrier.description && (
                                    <p className="carrier-description">{carrier.description}</p>
                                )}
                                <button className="btn-view-benefits">View Benefits</button>
                            </div>
                        ))
                    )}
                </div>
            )}

            {/* Carrier Details Modal */}
            {selectedCarrier && (
                <div className="modal-overlay" onClick={() => setSelectedCarrier(null)}>
                    <div className="modal-content carrier-details-modal" onClick={e => e.stopPropagation()}>
                        <button className="close-btn" onClick={() => setSelectedCarrier(null)}>&times;</button>

                        {/* Header */}
                        <div className="carrier-modal-header">
                            <h1>{selectedCarrier.name}</h1>
                            {selectedCarrier.website && (
                                <a
                                    href={selectedCarrier.website}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="carrier-website-btn"
                                >
                                    Visit Website →
                                </a>
                            )}
                        </div>

                        {selectedCarrier.description && (
                            <div className="carrier-description-section">
                                <p>{selectedCarrier.description}</p>
                            </div>
                        )}

                        {/* Contact Information */}
                        {(selectedCarrier.contact_email || selectedCarrier.contact_phone) && (
                            <div className="job-details-section">
                                <h4>Contact Information</h4>
                                <div className="contact-info">
                                    {selectedCarrier.contact_email && (
                                        <p><strong>Email:</strong> {selectedCarrier.contact_email}</p>
                                    )}
                                    {selectedCarrier.contact_phone && (
                                        <p><strong>Phone:</strong> {selectedCarrier.contact_phone}</p>
                                    )}
                                </div>
                            </div>
                        )}

                        {/* Company Benefits */}
                        <div className="lane-info-container">
                            <div className="lane-side-label">Company Benefits & Info</div>
                            <div className="lane-info-content">
                                {selectedCarrier.benefit_401k && (
                                    <div className="lane-section">
                                        <h5 className="lane-section-title">401(k)</h5>
                                        <div className="lane-section-content">{renderFormattedText(selectedCarrier.benefit_401k)}</div>
                                    </div>
                                )}
                                {selectedCarrier.benefit_medical_dental_vision && (
                                    <div className="lane-section">
                                        <h5 className="lane-section-title">Medical, Dental & Vision Plans</h5>
                                        <div className="lane-section-content">{renderFormattedText(selectedCarrier.benefit_medical_dental_vision)}</div>
                                    </div>
                                )}
                                {selectedCarrier.benefit_disability_life && (
                                    <div className="lane-section">
                                        <h5 className="lane-section-title">Disability, Life, Accident & Critical Illness Coverage</h5>
                                        <div className="lane-section-content">{renderFormattedText(selectedCarrier.benefit_disability_life)}</div>
                                    </div>
                                )}
                                {selectedCarrier.benefit_paid_vacation && (
                                    <div className="lane-section">
                                        <h5 className="lane-section-title">Paid Vacation</h5>
                                        <div className="lane-section-content">{renderFormattedText(selectedCarrier.benefit_paid_vacation)}</div>
                                    </div>
                                )}
                                {selectedCarrier.benefit_weekly_paycheck && (
                                    <div className="lane-section">
                                        <h5 className="lane-section-title">Weekly Paycheck</h5>
                                        <div className="lane-section-content">{renderFormattedText(selectedCarrier.benefit_weekly_paycheck)}</div>
                                    </div>
                                )}
                                {selectedCarrier.benefit_driver_ranking_bonus && (
                                    <div className="lane-section">
                                        <h5 className="lane-section-title">Driver Ranking Bonus</h5>
                                        <div className="lane-section-content">{renderFormattedText(selectedCarrier.benefit_driver_ranking_bonus)}</div>
                                    </div>
                                )}
                                {selectedCarrier.benefit_prescription_drug && (
                                    <div className="lane-section">
                                        <h5 className="lane-section-title">Prescription Drug Plans</h5>
                                        <div className="lane-section-content">{renderFormattedText(selectedCarrier.benefit_prescription_drug)}</div>
                                    </div>
                                )}
                                {selectedCarrier.benefit_stock_purchase && (
                                    <div className="lane-section">
                                        <h5 className="lane-section-title">Stock Purchase Program</h5>
                                        <div className="lane-section-content">{renderFormattedText(selectedCarrier.benefit_stock_purchase)}</div>
                                    </div>
                                )}
                                {selectedCarrier.benefit_military_program && (
                                    <div className="lane-section">
                                        <h5 className="lane-section-title">Military Benefits Program</h5>
                                        <div className="lane-section-content">{renderFormattedText(selectedCarrier.benefit_military_program)}</div>
                                    </div>
                                )}
                                {selectedCarrier.benefit_tuition_program && (
                                    <div className="lane-section">
                                        <h5 className="lane-section-title">Debt-Free Tuition Program</h5>
                                        <div className="lane-section-content">{renderFormattedText(selectedCarrier.benefit_tuition_program)}</div>
                                    </div>
                                )}
                                {selectedCarrier.benefit_other && (
                                    <div className="lane-section">
                                        <h5 className="lane-section-title">Other Benefits</h5>
                                        <div className="lane-section-content">{renderFormattedText(selectedCarrier.benefit_other)}</div>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Process & Qualifications */}
                        {(selectedCarrier.presentation || selectedCarrier.pre_qualifications || selectedCarrier.app_process) && (
                            <div className="lane-info-container" style={{ marginTop: '2rem' }}>
                                <div className="lane-side-label">Process & Quals</div>
                                <div className="lane-info-content">
                                    {selectedCarrier.presentation && (
                                        <div className="lane-section">
                                            <h5 className="lane-section-title">Presentation</h5>
                                            <div className="lane-section-content">{renderGenericTable(selectedCarrier.presentation)}</div>
                                        </div>
                                    )}
                                    {selectedCarrier.pre_qualifications && (
                                        <div className="lane-section">
                                            <h5 className="lane-section-title">Pre-Qualifications</h5>
                                            <div className="lane-section-content">{renderGenericTable(selectedCarrier.pre_qualifications)}</div>
                                        </div>
                                    )}
                                    {selectedCarrier.app_process && (
                                        <div className="lane-section">
                                            <h5 className="lane-section-title">Application Process</h5>
                                            <div className="lane-section-content">{renderFormattedText(selectedCarrier.app_process)}</div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}

                        {/* Action Buttons */}
                        <div className="modal-actions">
                            <button
                                className="btn-secondary"
                                onClick={() => setSelectedCarrier(null)}
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

export default Carriers;
