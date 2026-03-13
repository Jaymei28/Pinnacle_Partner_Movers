import React, { useState, useEffect } from 'react';
import axios from 'axios';

let VITE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

if (VITE_URL && !VITE_URL.includes('.') && !VITE_URL.includes('localhost')) {
    VITE_URL = `${VITE_URL}.onrender.com`;
}

if (VITE_URL && !VITE_URL.startsWith('http')) {
    VITE_URL = `https://${VITE_URL}`;
}
const API_BASE_URL = VITE_URL.endsWith('/api/') ? VITE_URL : `${VITE_URL.replace(/\/$/, '')}/api/`;
const API_URL = `${API_BASE_URL}carriers/`;

const Carriers = () => {
    const [carriers, setCarriers] = useState([]);
    const [loading, setLoading] = useState(false);
    const [selectedCarrier, setSelectedCarrier] = useState(null);
    const [isEditModalOpen, setIsEditModalOpen] = useState(false);
    const [editingCarrier, setEditingCarrier] = useState(null);
    const [error, setError] = useState(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

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

        if (lines.length === 0) return null;

        // DELIMITER DETECTION
        let delimiter = null;
        for (let line of lines) {
            if (line.includes('|')) { delimiter = '|'; break; }
            if (line.includes('\t')) { delimiter = '\t'; break; }
            if (line.includes(',')) {
                const commaCount = (line.match(/,/g) || []).length;
                if (commaCount >= 1) { delimiter = ','; break; }
            }
        }

        const splitLine = (line, delim) => {
            if (!delim) {
                if (line.includes(':') && line.indexOf(':') < 35) {
                    const idx = line.indexOf(':');
                    return [line.substring(0, idx).trim(), line.substring(idx + 1).trim()];
                }
                return [line];
            }
            if (delim !== ',') return line.split(delim).map(c => c.trim());
            const result = [];
            let current = '';
            let inQuotes = false;
            for (let i = 0; i < line.length; i++) {
                if (line[i] === '"') inQuotes = !inQuotes;
                else if (line[i] === ',' && !inQuotes) { result.push(current.trim()); current = ''; }
                else { current += line[i]; }
            }
            result.push(current.trim());
            return result.map(c => c.replace(/^"|"$/g, ''));
        };

        const firstLine = lines[0];
        const orientationKeywords = ['city', 'state', 'days', 'time', 'address', 'terminal'];
        if (orientationKeywords.some(k => firstLine.toLowerCase().includes(k))) {
            return renderOrientationTable(text);
        }

        const rows = lines.map(line => splitLine(line, delimiter));

        return (
            <div className="premium-table-wrapper">
                <table className="premium-data-table">
                    <tbody>
                        {rows.map((row, idx) => (
                            <tr key={idx} className="table-data-row">
                                {row.map((cell, i) => {
                                    const isHeader = idx === 0 || (row.length === 1 && cell === cell.toUpperCase() && cell.length > 3);
                                    const isLabel = i === 0 && row.length === 2;
                                    return (
                                        <td
                                            key={i}
                                            className={isHeader ? "table-header-cell" : isLabel ? "table-label-cell" : "table-value-cell"}
                                            colSpan={row.length === 1 ? "2" : "1"}
                                        >
                                            {renderFormattedText(cell)}
                                        </td>
                                    );
                                })}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        );
    };

    const renderAppProcess = (text) => {
        if (!text) return null;
        let processedText = String(text).replace(/\\n/g, '\n');
        const lines = processedText.split('\n').map(l => l.trim()).filter(l => l.length > 0);

        if (lines.length === 0) return null;

        return (
            <div className="premium-table-wrapper">
                <table className="premium-data-table">
                    <tbody>
                        {lines.map((line, index) => {
                            const lineLower = line.toLowerCase();
                            const cleanLine = line.replace(/^[•\*\-\s]+/, '').trim();

                            let specialClass = "";
                            if (/^step\s+\d+/i.test(line)) specialClass = "app-step-red";
                            else if (lineLower === 'follow up') specialClass = "app-heading-green";
                            else if (lineLower.includes('approved') && lineLower.includes('now what')) specialClass = "app-heading-blue";

                            const isHeader = (index === 0 && line.length < 40) || (line.length < 50 && line === line.toUpperCase() && !/[.\?!]$/.test(line));

                            if (isHeader || specialClass) {
                                return (
                                    <tr key={index} className="table-header-row">
                                        <td colSpan="2" className={`table-header-cell ${specialClass}`}>
                                            {line}
                                        </td>
                                    </tr>
                                );
                            }

                            if (cleanLine.includes(':') && cleanLine.indexOf(':') < 35) {
                                const idx = cleanLine.indexOf(':');
                                return (
                                    <tr key={index} className="table-data-row">
                                        <td className="table-label-cell">{cleanLine.substring(0, idx).trim()}</td>
                                        <td className="table-value-cell">{renderFormattedText(cleanLine.substring(idx + 1).trim())}</td>
                                    </tr>
                                );
                            }

                            return (
                                <tr key={index} className="table-data-row">
                                    <td colSpan="2" className="table-full-cell">{renderFormattedText(line)}</td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        );
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
            <div className="premium-table-wrapper">
                <table className="premium-data-table">
                    <thead>
                        <tr className="table-header-row">
                            <th className="table-header-cell">City / State</th>
                            <th className="table-header-cell">Days</th>
                            <th className="table-header-cell">Start Time</th>
                            <th className="table-header-cell">Terminal Address</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows.map((row, idx) => (
                            <tr key={idx} className="table-data-row">
                                <td className="table-value-cell" style={{ fontWeight: '500' }}>{row.cityState}</td>
                                <td className="table-value-cell">{row.days}</td>
                                <td className="table-value-cell">{row.time}</td>
                                <td className="table-value-cell">{row.address}</td>
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

    const handleEditClick = (e, carrier) => {
        e.stopPropagation();
        setEditingCarrier({ ...carrier });
        setIsEditModalOpen(true);
    };

    const handleUpdateCarrier = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);
        setError(null);

        const formData = new FormData();
        // Append all text fields
        Object.keys(editingCarrier).forEach(key => {
            if (key !== 'logo' && key !== 'active_jobs_count') {
                formData.append(key, editingCarrier[key] || '');
            }
        });

        // Append logo if it's a file object (newly selected)
        const logoInput = document.getElementById('carrier-logo-upload');
        if (logoInput && logoInput.files[0]) {
            formData.append('logo', logoInput.files[0]);
        }

        try {
            const response = await axios.patch(`${API_URL}${editingCarrier.id}/`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            // Update local state
            setCarriers(prev => prev.map(c => c.id === editingCarrier.id ? response.data : c));
            setIsEditModalOpen(false);
            setEditingCarrier(null);
        } catch (err) {
            console.error('Error updating carrier:', err);
            setError('Failed to update carrier. Please check the fields and try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

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

            {loading ? (
                <div className="status-msg">Loading carriers...</div>
            ) : error ? (
                <div className="status-msg error">{error}</div>
            ) : (
                <div className="jobs-table-container">
                    <table className="jobs-listing-table carriers-table">
                        <thead>
                            <tr className="table-header-row-static">
                                <th className="th-id">ID</th>
                                <th className="th-carrier">Name</th>
                                <th className="th-active-jobs">Active Jobs</th>
                                <th className="th-last-updated">Date Updated</th>
                                <th className="th-actions"></th>
                            </tr>
                        </thead>
                        <tbody>
                            {carriers.length === 0 ? (
                                <tr className="empty-row">
                                    <td colSpan="5" className="empty-table-msg">No carriers available at the moment.</td>
                                </tr>
                            ) : (
                                carriers.map(carrier => (
                                    <tr key={carrier.id} className="job-table-row carrier-row" onClick={() => setSelectedCarrier(carrier)}>
                                        <td className="td-id">{carrier.id}</td>
                                        <td className="td-carrier">
                                            <div className="carrier-info-cell">
                                                {carrier.logo ? (
                                                    <img src={carrier.logo} alt={carrier.name} className="table-carrier-logo" />
                                                ) : (
                                                    <div className="table-carrier-placeholder">{carrier.name.charAt(0)}</div>
                                                )}
                                                <span className="job-title-link">{carrier.name}</span>
                                            </div>
                                        </td>
                                        <td className="td-active-jobs">
                                            <span className="count-pill">{carrier.active_jobs_count || 0}</span>
                                        </td>
                                        <td className="td-date">
                                            {carrier.updated_at ? new Date(carrier.updated_at).toLocaleString('en-US', {
                                                month: 'long',
                                                day: 'numeric',
                                                year: 'numeric',
                                                hour: 'numeric',
                                                minute: '2-digit',
                                                hour12: true
                                            }).replace(',', '') : 'N/A'}
                                        </td>
                                        <td className="td-actions">
                                            <div className="carrier-actions">
                                                <button className="btn-action-icon" title="Expand">
                                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7" /></svg>
                                                </button>
                                                <button className="btn-action-icon" title="Edit" onClick={(e) => handleEditClick(e, carrier)}>
                                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" /></svg>
                                                </button>
                                                <button className="btn-action-icon btn-view-orange" title="View Details">
                                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" /></svg>
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
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
                                {selectedCarrier.benefits && (
                                    <div className="lane-section">
                                        <h5 className="lane-section-title">Benefits Summary</h5>
                                        <div className="lane-section-content">{renderGenericTable(selectedCarrier.benefits)}</div>
                                    </div>
                                )}
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
                                            <div className="lane-section-content">{renderAppProcess(selectedCarrier.app_process)}</div>
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

            {/* Edit Carrier Modal */}
            {isEditModalOpen && editingCarrier && (
                <div className="modal-overlay" onClick={() => setIsEditModalOpen(false)}>
                    <div className="modal-content carrier-edit-modal" onClick={e => e.stopPropagation()}>
                        <div className="modal-header-new">
                            <h2>Edit Carrier: {editingCarrier.name}</h2>
                            <button className="close-btn" onClick={() => setIsEditModalOpen(false)}>&times;</button>
                        </div>

                        <form onSubmit={handleUpdateCarrier} className="edit-carrier-form">
                            <div className="form-grid-two-col">
                                <div className="form-group">
                                    <label>Carrier Name</label>
                                    <input
                                        type="text"
                                        value={editingCarrier.name || ''}
                                        onChange={e => setEditingCarrier({ ...editingCarrier, name: e.target.value })}
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Website URL</label>
                                    <input
                                        type="url"
                                        value={editingCarrier.website || ''}
                                        onChange={e => setEditingCarrier({ ...editingCarrier, website: e.target.value })}
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Contact Email</label>
                                    <input
                                        type="email"
                                        value={editingCarrier.contact_email || ''}
                                        onChange={e => setEditingCarrier({ ...editingCarrier, contact_email: e.target.value })}
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Contact Phone</label>
                                    <input
                                        type="text"
                                        value={editingCarrier.contact_phone || ''}
                                        onChange={e => setEditingCarrier({ ...editingCarrier, contact_phone: e.target.value })}
                                    />
                                </div>
                            </div>

                            <div className="form-group full-width">
                                <label>Company Description</label>
                                <textarea
                                    rows="3"
                                    value={editingCarrier.description || ''}
                                    onChange={e => setEditingCarrier({ ...editingCarrier, description: e.target.value })}
                                />
                            </div>

                            <div className="form-group full-width">
                                <label>Carrier Logo</label>
                                <div className="logo-upload-preview">
                                    {editingCarrier.logo && typeof editingCarrier.logo === 'string' && (
                                        <img src={editingCarrier.logo} alt="Current logo" className="current-logo-preview" />
                                    )}
                                    <input
                                        type="file"
                                        id="carrier-logo-upload"
                                        accept="image/*"
                                        className="file-input-custom"
                                    />
                                </div>
                                <p className="help-text">Select a new image to replace the current logo.</p>
                            </div>

                            <div className="form-section-divider">
                                <h4>Company Benefits (Granular)</h4>
                                <p className="section-help">Add individual benefit details here.</p>
                            </div>

                            <div className="form-grid-two-col">
                                <div className="form-group">
                                    <label>401(k)</label>
                                    <textarea rows="2" value={editingCarrier.benefit_401k || ''} onChange={e => setEditingCarrier({ ...editingCarrier, benefit_401k: e.target.value })} />
                                </div>
                                <div className="form-group">
                                    <label>Medical, Dental & Vision</label>
                                    <textarea rows="2" value={editingCarrier.benefit_medical_dental_vision || ''} onChange={e => setEditingCarrier({ ...editingCarrier, benefit_medical_dental_vision: e.target.value })} />
                                </div>
                                <div className="form-group">
                                    <label>Disability & Life</label>
                                    <textarea rows="2" value={editingCarrier.benefit_disability_life || ''} onChange={e => setEditingCarrier({ ...editingCarrier, benefit_disability_life: e.target.value })} />
                                </div>
                                <div className="form-group">
                                    <label>Paid Vacation</label>
                                    <textarea rows="2" value={editingCarrier.benefit_paid_vacation || ''} onChange={e => setEditingCarrier({ ...editingCarrier, benefit_paid_vacation: e.target.value })} />
                                </div>
                            </div>

                            <div className="form-section-divider">
                                <h4>Data Tables & Processes</h4>
                                <p className="section-help">Paste CSV/Table data (Category,Value) for Benefits, Presentation and Qualifications.</p>
                            </div>

                            <div className="form-group full-width">
                                <label>Benefits Summary (Table Format)</label>
                                <textarea
                                    rows="5"
                                    placeholder="Category,Details&#10;Bonus,$500"
                                    value={editingCarrier.benefits || ''}
                                    onChange={e => setEditingCarrier({ ...editingCarrier, benefits: e.target.value })}
                                />
                            </div>

                            <div className="form-group full-width">
                                <label>Pre-Qualifications (Table Format)</label>
                                <textarea
                                    rows="5"
                                    value={editingCarrier.pre_qualifications || ''}
                                    onChange={e => setEditingCarrier({ ...editingCarrier, pre_qualifications: e.target.value })}
                                />
                            </div>

                            <div className="form-group full-width">
                                <label>Presentation (Table Format)</label>
                                <textarea
                                    rows="10"
                                    value={editingCarrier.presentation || ''}
                                    onChange={e => setEditingCarrier({ ...editingCarrier, presentation: e.target.value })}
                                />
                            </div>

                            <div className="form-group full-width">
                                <label>Application Process Steps</label>
                                <textarea
                                    rows="10"
                                    value={editingCarrier.app_process || ''}
                                    onChange={e => setEditingCarrier({ ...editingCarrier, app_process: e.target.value })}
                                />
                            </div>

                            <div className="modal-footer-new">
                                <button type="button" className="btn-cancel" onClick={() => setIsEditModalOpen(false)}>Cancel</button>
                                <button type="submit" className="btn-save-main-new" disabled={isSubmitting}>
                                    {isSubmitting ? 'Saving...' : 'Save Changes'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Carriers;
