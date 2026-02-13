import React, { useState, useEffect } from 'react';
import axios from 'axios';
import searchIcon from '../images/search.svg';
import jobDetailsIcon from '../images/jobdetails.svg';
import presentationIcon from '../images/pesentation.svg';
import preQualIcon from '../images/pre-qualification.svg';
import appProcessIcon from '../images/application-process.svg';

const API_URL = 'http://localhost:8000/api/jobs/';

const Opportunities = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(false);
    const [selectedJob, setSelectedJob] = useState(null);
    const [error, setError] = useState(null);
    const [zipCode, setZipCode] = useState('');
    const [searchZip, setSearchZip] = useState('');
    const [expandedJobId, setExpandedJobId] = useState(null);
    const [openDropdownId, setOpenDropdownId] = useState(null);
    const [carrierSearchQuery, setCarrierSearchQuery] = useState('');
    const [carrierInfoPanel, setCarrierInfoPanel] = useState(null); // { job, type: 'presentation' | 'pre_qualifications' | 'app_process' }

    const toggleExpand = (jobId) => {
        setExpandedJobId(expandedJobId === jobId ? null : jobId);
    };

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

    const renderGenericTable = (text, filterQuery = '') => {
        if (!text) return null;
        let processedText = String(text).replace(/\\n/g, '\n');
        const lines = processedText.split('\n').map(l => l.trim()).filter(l => l.length > 0);

        if (lines.length <= 1) return renderFormattedText(text, true);

        // DELIMITER DETECTION (Pipe, Tab, or Comma)
        // Check first few lines for the best delimiter
        let delimiter = null;
        for (let i = 0; i < Math.min(lines.length, 3); i++) {
            const line = lines[i];
            if (line.includes('|')) { delimiter = '|'; break; }
            if (line.includes('\t')) { delimiter = '\t'; break; }
            if (line.includes(',')) { delimiter = ','; break; }
        }

        // Special case: If first line is "PRESENTATION TOPIC DESCRIPTION" with no delimiter, 
        // and lines below it are delimited, we should still treat it as a table.
        // We'll manually inject the header split if needed.
        const firstLine = lines[0];
        const isPresentationHeader = firstLine.toUpperCase() === "PRESENTATION TOPIC DESCRIPTION";

        if (delimiter || isPresentationHeader) {
            const splitLine = (line, delim) => {
                if (!delim) return [line]; // No split if no delimiter
                if (delim !== ',') return line.split(delim).map(c => c.trim());

                // Robust CSV split for comma delimiter (handles quotes)
                const result = [];
                let currentCell = '';
                let inQuotes = false;
                for (let i = 0; i < line.length; i++) {
                    const char = line[i];
                    if (char === '"') {
                        if (inQuotes && line[i + 1] === '"') {
                            currentCell += '"';
                            i++;
                        } else {
                            inQuotes = !inQuotes;
                        }
                    } else if (char === ',' && !inQuotes) {
                        result.push(currentCell.trim());
                        currentCell = '';
                    } else {
                        currentCell += char;
                    }
                }
                result.push(currentCell.trim());
                return result.map(c => c.replace(/^"|"$/g, ''));
            };

            const rows = [];
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (delimiter && (line.includes(delimiter) || (delimiter === ',' && line.startsWith('"')))) {
                    const cells = splitLine(line, delimiter);
                    if (cells.length > 0 && cells[0] === '' && rows.length > 0) {
                        const lastRow = rows[rows.length - 1];
                        const lastCellIndex = Math.min(lastRow.length - 1, cells.length - 1);
                        if (lastCellIndex >= 0) lastRow[lastCellIndex] += '\n' + cells.slice(1).join(' ');
                    } else {
                        rows.push(cells);
                    }
                } else {
                    if (rows.length > 0) {
                        const lastRow = rows[rows.length - 1];
                        const lastCellIndex = lastRow.length - 1;
                        lastRow[lastCellIndex] += '\n' + line;
                    } else {
                        // First line with no delimiter
                        rows.push([line]);
                    }
                }
            }

            // FILTER ROWS based on query
            const filteredRows = filterQuery
                ? rows.filter(row => row.some(cell => cell.toLowerCase().includes(filterQuery.toLowerCase())))
                : rows;

            if (filteredRows.length === 0 && filterQuery) {
                return (
                    <div className="no-search-results" style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-light)', border: '1px dashed var(--border)', borderRadius: '8px' }}>
                        No matches found for "{filterQuery}"
                    </div>
                );
            }

            return (
                <div className="orientation-table-wrapper">
                    <table className="orientation-table">
                        <tbody>
                            {filteredRows.map((row, idx) => (
                                <tr key={idx}>
                                    {row.map((cell, i) => (
                                        <td key={i} style={idx === 0 ? { fontWeight: '800', background: '#f8fafc' } : {}}>
                                            {renderFormattedText(cell, true)}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            );
        }

        return renderFormattedText(text);
    };

    const renderOrientationTable = (text) => {
        if (!text) return null;
        let processedText = String(text).replace(/\\n/g, '\n');
        const lines = processedText.split('\n').map(l => l.trim()).filter(l => l.length > 0);

        const headerKeywords = ['city', 'state', 'days', 'time', 'address', 'terminal'];
        const isTradOrientation = lines.length > 1 && headerKeywords.some(k => lines[0].toLowerCase().includes(k));

        if (!isTradOrientation) {
            // Check if it's a generic table instead of falling back to text immediately
            const firstLine = lines[0];
            if (firstLine.includes(',') || firstLine.includes('|') || firstLine.includes('\t') || firstLine.toUpperCase() === "PRESENTATION TOPIC DESCRIPTION") {
                return renderGenericTable(text);
            }
            return renderFormattedText(text);
        }

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
                                <td className="cell-city" style={{ fontWeight: 'normal' }}>{row.cityState}</td>
                                <td className="cell-days">{row.days}</td>
                                <td className="cell-time" style={{ fontWeight: 'normal' }}>{row.time}</td>
                                <td className="cell-address">{row.address}</td>
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
            <div className="app-process-container">
                {lines.map((line, index) => {
                    const lineLower = line.toLowerCase();
                    const cleanLine = line.replace(/^[•\*\-\s]+/, '').trim();

                    // 1. TITLE (Large, Bold)
                    if (index === 0 && (lineLower.includes('application process') || line.length < 40)) {
                        return <div key={index} className="app-process-title">{line}</div>;
                    }

                    // 2. STEP X (Red, Underlined)
                    if (/^step\s+\d+/i.test(line)) {
                        return <div key={index} className="app-step-red">{line}</div>;
                    }

                    // 3. FOLLOW UP (Green, Underlined)
                    if (lineLower === 'follow up') {
                        return <div key={index} className="app-heading-green">{line}</div>;
                    }

                    // 4. APPROVED / NOW WHAT (Blue, Underlined)
                    if (lineLower.includes('approved') && lineLower.includes('now what')) {
                        return <div key={index} className="app-heading-blue">{line}</div>;
                    }

                    // 5. EXPECTED / CAN EXPECT (Purple, Underlined)
                    if (lineLower.includes('can expect with') || lineLower.includes('steps you and the driver')) {
                        return <div key={index} className="app-heading-purple">{line}</div>;
                    }

                    // 6. GLOSSARY (Gray, Underlined)
                    if (lineLower.includes('glossary of terms')) {
                        return <div key={index} className="app-heading-gray">{line}</div>;
                    }

                    // 7. BULLETS (Dot on left)
                    const isBullet = /^[•\*\-]/.test(line) || (index > 2 && line.length < 100 && lines[index - 1].includes(':'));

                    // 8. LINKS
                    const isLink = cleanLine.startsWith('http') || cleanLine.includes('.com/') || cleanLine.includes('.org/');

                    if (isBullet) {
                        return (
                            <div key={index} className="app-bullet-item">
                                {isLink ? (
                                    <a href={cleanLine.startsWith('http') ? cleanLine : `https://${cleanLine}`} target="_blank" rel="noopener noreferrer" className="app-link">
                                        {cleanLine}
                                    </a>
                                ) : (
                                    <span>{cleanLine}</span>
                                )}
                            </div>
                        );
                    }

                    // 9. BOLD KEY/VALUE (e.g. ALS: text)
                    if (cleanLine.includes(':') && cleanLine.indexOf(':') < 30) {
                        const colonIdx = cleanLine.indexOf(':');
                        const label = cleanLine.substring(0, colonIdx + 1);
                        const rest = cleanLine.substring(colonIdx + 1);
                        return (
                            <div key={index} className="app-paragraph">
                                <span className="app-text-bold">{label}</span>
                                {rest.includes('http') ? (
                                    <a href={rest.trim().startsWith('http') ? rest.trim() : `https://${rest.trim()}`} target="_blank" rel="noopener noreferrer" className="app-link" style={{ marginLeft: '4px' }}>
                                        {rest.trim()}
                                    </a>
                                ) : (
                                    <span>{rest}</span>
                                )}
                            </div>
                        );
                    }

                    // 10. DEFAULT PARAGRAPH
                    return (
                        <div key={index} className="app-paragraph">
                            {isLink ? (
                                <a href={cleanLine.startsWith('http') ? cleanLine : `https://${cleanLine}`} target="_blank" rel="noopener noreferrer" className="app-link">
                                    {cleanLine}
                                </a>
                            ) : (
                                cleanLine
                            )}
                        </div>
                    );
                })}
            </div>
        );
    };

    const renderFormattedText = (text, forceNormal = false) => {
        if (!text) return null;

        // Split by newline and filter out empty lines
        let processedText = String(text).replace(/\\n/g, '\n');
        const lines = processedText.split('\n').map(line => line.trim()).filter(line => line.length > 0);

        if (lines.length === 0) return null;

        return (
            <div className={`formatted-text-container ${forceNormal ? 'force-normal' : ''}`}>
                {lines.map((line, index) => {
                    const isBullet = /^[•\*\-]/.test(line);
                    const isBoldMarkdown = line.startsWith('**') && line.endsWith('**');

                    // Strip leading/trailing quotes if they exist, along with bullets
                    const cleanLine = line.replace(/^[•\*\-\s\"\'\s]+/, '').replace(/[\"\'\s]+$/, '').replace(/\*\*/g, '');

                    if (!cleanLine) return null;

                    // Headers are usually short, don't have bullets, and DON'T end in a period.
                    const endsWithPunctuation = /[.\?!]$/.test(cleanLine.trim());
                    const isShort = cleanLine.length < 50;
                    const isProbablyProperty = cleanLine.includes(':') && cleanLine.indexOf(':') < 25;

                    // Detect if line is entirely uppercase (CAPS LOCK)
                    // We check if it has at least one letter and no lowercase letters after trimming punctuation
                    const alphaContent = cleanLine.replace(/[^a-zA-Z]/g, '');
                    const isCapsLock = alphaContent.length > 2 && alphaContent === alphaContent.toUpperCase();

                    // In forceNormal mode, we treat short, unpunctuated lines as bullets rather than headers
                    const isHeader = isBoldMarkdown || isCapsLock || (!isBullet && isShort && !endsWithPunctuation && !isProbablyProperty && !forceNormal);

                    // In forceNormal mode, treat items after first line as bullets for lists
                    const effectiveIsBullet = isBullet || (forceNormal && index > 0);

                    if (isHeader) {
                        return (
                            <div key={index} className="lane-section-title" style={{ marginTop: index > 0 ? (forceNormal ? '0.4rem' : '1.25rem') : '0', fontWeight: '800' }}>
                                {cleanLine}
                            </div>
                        );
                    }

                    if (cleanLine.includes(':')) {
                        const colonIndex = cleanLine.indexOf(':');
                        const label = cleanLine.substring(0, colonIndex).trim();
                        const valueParts = cleanLine.substring(colonIndex + 1).trim().split('**');

                        return (
                            <div key={index} className={effectiveIsBullet ? "lane-item" : "lane-text-line"}>
                                <span className="lane-label" style={{ fontWeight: forceNormal ? '400' : 'inherit' }}>{label}:</span>
                                <span className="lane-value">
                                    {valueParts.map((part, i) => part)}
                                </span>
                            </div>
                        );
                    }

                    const parts = cleanLine.split('**');
                    return (
                        <div key={index} className={effectiveIsBullet ? "lane-item" : "lane-text-line"}>
                            <span className="lane-text">
                                {parts.map((part, i) => part)}
                            </span>
                        </div>
                    );
                })}
            </div>
        );
    };

    useEffect(() => {
        fetchJobs();
    }, []);

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = () => {
            if (openDropdownId !== null) {
                setOpenDropdownId(null);
            }
        };

        document.addEventListener('click', handleClickOutside);
        return () => document.removeEventListener('click', handleClickOutside);
    }, [openDropdownId]);

    // parseJobTags, formatDescription, and parseLaneInformation sections removed for better performance and consistency.

    // Handle Body Scroll Lock when Modal is Open
    useEffect(() => {
        if (selectedJob || carrierInfoPanel) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'unset';
        }

        return () => {
            document.body.style.overflow = 'unset';
        };
    }, [selectedJob, carrierInfoPanel]);


    return (
        <div className="opportunities-view">
            <div className="opportunities-header-row">
                <div className="search-bar-container-new">
                    <div className="search-icon-wrapper">
                        <img src={searchIcon} alt="" className="search-icon-gray" />
                    </div>
                    <input
                        type="text"
                        className="search-input-new"
                        placeholder="Search by the zip code listed on the drivers CDL"
                        value={zipCode}
                        onChange={(e) => setZipCode(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                        maxLength="5"
                    />
                    {searchZip && (
                        <button className="btn-clear-inline" onClick={handleClearSearch}>&times;</button>
                    )}
                </div>

                <div className="header-action-buttons">
                    <button className="btn-header-action">
                        <svg className="btn-header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" />
                            <path d="M15 2H9a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1Z" />
                            <path d="m12 11 4 4" />
                            <path d="m16 11-4 4" />
                        </svg>
                        Cheat Sheet
                    </button>
                    <button className="btn-header-action outline">
                        <svg className="btn-header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l2.27-2.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z" />
                        </svg>
                        Carrier Contacts
                    </button>
                </div>
            </div>

            {loading ? (
                <div className="status-msg">Loading jobs...</div>
            ) : error ? (
                <div className="status-msg error">{error}</div>
            ) : (
                <div className="job-cards-list">
                    {jobs.length === 0 ? (
                        <div className="status-msg">
                            {searchZip
                                ? `No jobs found within hiring radius of ${searchZip}. Try a different zip code.`
                                : 'No jobs available at the moment.'}
                        </div>
                    ) : (
                        jobs.map(job => {
                            const states = job.states ? job.states.split(',').map(s => s.trim()) : [];
                            const carrierName = job.carrier?.name || 'Swift';
                            const isExpanded = expandedJobId === job.id;

                            return (
                                <div key={job.id} className={`job-list-card ${isExpanded ? 'is-expanded' : ''}`}>
                                    <div className="card-main-row">
                                        <div className="card-left-content">
                                            <div className="carrier-badge">{carrierName}</div>
                                            <h3 className="job-card-title">{job.title}</h3>
                                            <p className="job-card-pay">
                                                {job.id === 1 ? `Average Weekly Pay: ${job.average_weekly_pay || '$1,300'}` : `${job.average_weekly_pay || '$1,200'} Weekly Average`}
                                            </p>
                                            <p className="job-card-hometime">{job.home_time || 'Daily'}</p>
                                            <div className="job-card-tags">
                                                {job.experience_levels && (
                                                    <span className="card-tag tag-pink">{job.experience_levels.split(',')[0]}</span>
                                                )}
                                                {job.driver_types && (
                                                    <span className="card-tag tag-blue-alt">{job.driver_types.split(',')[0]}</span>
                                                )}
                                                <span className="card-tag tag-green-alt">No Touch Freight</span>
                                                {states.length > 0 && (
                                                    <span className="card-tag tag-purp-alt">{states[0]}</span>
                                                )}
                                            </div>
                                        </div>

                                        <div className="card-right-actions">
                                            <div className="action-buttons-group">
                                                <button
                                                    className="btn-job-details-new"
                                                    onClick={() => setSelectedJob(job)}
                                                >
                                                    <svg className="btn-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                                        <circle cx="12" cy="12" r="3" />
                                                        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1Z" />
                                                    </svg>
                                                    Job Details
                                                </button>
                                                <button className="btn-map-portal">
                                                    <svg className="btn-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                                        <path d="M3 6l6-3 6 3 6-3v15l-6 3-6-3-6 3V6z" />
                                                        <line x1="9" y1="3" x2="9" y2="21" />
                                                        <line x1="15" y1="3" x2="15" y2="21" />
                                                    </svg>
                                                    Map/Portal/Sheet
                                                </button>
                                                <div style={{ position: 'relative' }}>
                                                    <button
                                                        className="btn-icon-only"
                                                        onClick={(e) => {
                                                            e.stopPropagation();
                                                            setOpenDropdownId(openDropdownId === job.id ? null : job.id);
                                                        }}
                                                    >
                                                        <svg className="icon-dots" viewBox="0 0 24 24" fill="currentColor">
                                                            <circle cx="5" cy="12" r="2" />
                                                            <circle cx="12" cy="12" r="2" />
                                                            <circle cx="19" cy="12" r="2" />
                                                        </svg>
                                                    </button>

                                                    {openDropdownId === job.id && job.carrier && (
                                                        <div
                                                            className="carrier-dropdown-menu"
                                                            style={{
                                                                position: 'absolute',
                                                                right: 0,
                                                                top: '100%',
                                                                marginTop: '0.5rem',
                                                                background: 'white',
                                                                border: '1px solid #e0e0e0',
                                                                borderRadius: '8px',
                                                                boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
                                                                zIndex: 1000,
                                                                minWidth: '200px',
                                                                overflow: 'hidden'
                                                            }}
                                                            onClick={(e) => e.stopPropagation()}
                                                        >
                                                            {job.carrier.presentation && (
                                                                <button
                                                                    className="dropdown-menu-item"
                                                                    style={{
                                                                        width: '100%',
                                                                        padding: '0.75rem 1rem',
                                                                        border: 'none',
                                                                        background: 'transparent',
                                                                        textAlign: 'left',
                                                                        cursor: 'pointer',
                                                                        fontSize: '0.9rem',
                                                                        transition: 'background 0.2s'
                                                                    }}
                                                                    onMouseEnter={(e) => e.target.style.background = '#f5f5f5'}
                                                                    onMouseLeave={(e) => e.target.style.background = 'transparent'}
                                                                    onClick={() => {
                                                                        setCarrierSearchQuery('');
                                                                        setCarrierInfoPanel({ job, type: 'presentation' });
                                                                        setOpenDropdownId(null);
                                                                    }}
                                                                >
                                                                    <img src={presentationIcon} alt="" className="btn-icon" /> Presentation
                                                                </button>
                                                            )}
                                                            {job.carrier.pre_qualifications && (
                                                                <button
                                                                    className="dropdown-menu-item"
                                                                    style={{
                                                                        width: '100%',
                                                                        padding: '0.75rem 1rem',
                                                                        border: 'none',
                                                                        background: 'transparent',
                                                                        textAlign: 'left',
                                                                        cursor: 'pointer',
                                                                        fontSize: '0.9rem',
                                                                        transition: 'background 0.2s',
                                                                        borderTop: job.carrier.presentation ? '1px solid #f0f0f0' : 'none'
                                                                    }}
                                                                    onMouseEnter={(e) => e.target.style.background = '#f5f5f5'}
                                                                    onMouseLeave={(e) => e.target.style.background = 'transparent'}
                                                                    onClick={() => {
                                                                        setCarrierSearchQuery('');
                                                                        setCarrierInfoPanel({ job, type: 'pre_qualifications' });
                                                                        setOpenDropdownId(null);
                                                                    }}
                                                                >
                                                                    <img src={preQualIcon} alt="" className="btn-icon" /> Pre-qualifications
                                                                </button>
                                                            )}
                                                            {job.carrier.app_process && (
                                                                <button
                                                                    className="dropdown-menu-item"
                                                                    style={{
                                                                        width: '100%',
                                                                        padding: '0.75rem 1rem',
                                                                        border: 'none',
                                                                        background: 'transparent',
                                                                        textAlign: 'left',
                                                                        cursor: 'pointer',
                                                                        fontSize: '0.9rem',
                                                                        transition: 'background 0.2s',
                                                                        borderTop: (job.carrier.presentation || job.carrier.pre_qualifications) ? '1px solid #f0f0f0' : 'none'
                                                                    }}
                                                                    onMouseEnter={(e) => e.target.style.background = '#f5f5f5'}
                                                                    onMouseLeave={(e) => e.target.style.background = 'transparent'}
                                                                    onClick={() => {
                                                                        setCarrierSearchQuery('');
                                                                        setCarrierInfoPanel({ job, type: 'app_process' });
                                                                        setOpenDropdownId(null);
                                                                    }}
                                                                >
                                                                    <img src={appProcessIcon} alt="" className="btn-icon" /> App Process
                                                                </button>
                                                            )}
                                                            {!job.carrier.presentation && !job.carrier.pre_qualifications && !job.carrier.app_process && (
                                                                <div style={{ padding: '0.75rem 1rem', color: '#999', fontSize: '0.85rem' }}>
                                                                    No carrier info available
                                                                </div>
                                                            )}
                                                        </div>
                                                    )}
                                                </div>
                                                <button
                                                    className={`btn-icon-only no-border expand-arrow ${isExpanded ? 'active' : ''}`}
                                                    onClick={() => toggleExpand(job.id)}
                                                >
                                                    <svg className="icon-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                                                        <path d="m6 9 6 6 6-6" />
                                                    </svg>
                                                </button>
                                            </div>
                                        </div>
                                    </div>

                                    {isExpanded && (
                                        <div className="card-expanded-content">
                                            {/* Location Source Transparency */}
                                            {job.match_type === 'proximity' && (
                                                <div className="location-transparency-badge proximity">
                                                    📍 Proximity match - Just outside standard hiring area
                                                </div>
                                            )}
                                            {job.match_type === 'state_level' && (
                                                <div className="location-transparency-badge state-level">
                                                    🌎 Regional match - Available in your state
                                                </div>
                                            )}
                                            {job.location_source === 'carrier_hq' && !job.match_type && (
                                                <div className="location-transparency-badge carrier-hq">
                                                    📍 Location based on carrier headquarters
                                                </div>
                                            )}
                                            {job.location_source === 'state_only' && !job.match_type && (
                                                <div className="location-transparency-badge state-level">
                                                    ⚠️ Regional opportunity - contact for exact location
                                                </div>
                                            )}

                                            {/* Minimal Detail View in Card */}
                                            <div className="card-detail-grid">
                                                {(job.experience_levels || job.home_time || job.zip_code) && (
                                                    <div className="detail-col">
                                                        <h4 className="detail-group-title">Job Information</h4>
                                                        {job.experience_levels && <div className="detail-row"><span className="detail-label">Experience:</span> <span className="detail-val">{job.experience_levels}</span></div>}
                                                        {job.home_time && <div className="detail-row"><span className="detail-label">Home Time:</span> <span className="detail-val">{job.home_time}</span></div>}
                                                        {job.zip_code && <div className="detail-row"><span className="detail-label">Zip Code:</span> <span className="detail-val">{job.zip_code}</span></div>}
                                                    </div>
                                                )}

                                                {(job.average_weekly_pay || job.pay_range || job.bonus_offer) && (
                                                    <div className="detail-col">
                                                        <h4 className="detail-group-title">Pay & Benefits</h4>
                                                        {job.average_weekly_pay && <div className="detail-row"><span className="detail-label">Weekly Pay:</span> <span className="detail-val">{job.average_weekly_pay}</span></div>}
                                                        {job.pay_range && <div className="detail-row"><span className="detail-label">Pay Range:</span> <span className="detail-val">{job.pay_range}</span></div>}
                                                        {job.bonus_offer && <div className="detail-row"><span className="detail-label">Bonus:</span> <span className="detail-val">{job.bonus_offer}</span></div>}
                                                    </div>
                                                )}
                                            </div>

                                            {job.job_details && (
                                                <div className="card-detail-text-section">
                                                    <h4 className="detail-group-title">Lane Information</h4>
                                                    <div className="formatted-detail-text">{renderFormattedText(job.job_details)}</div>
                                                </div>
                                            )}

                                            {/* Company Benefits & Info */}
                                            {job.carrier && (
                                                <div className="card-detail-text-section secondary">
                                                    <h4 className="detail-group-title">Company Benefits & Info</h4>
                                                    <div className="benefits-mini-list">
                                                        {job.carrier.benefit_medical_dental_vision && <div className="benefit-pill">Medical/Dental/Vision</div>}
                                                        {job.carrier.benefit_401k && <div className="benefit-pill">401(k)</div>}
                                                        {job.carrier.benefit_paid_vacation && <div className="benefit-pill">Paid Vacation</div>}
                                                        {job.carrier.benefit_stock_purchase && <div className="benefit-pill">Stock Purchase</div>}
                                                    </div>
                                                    <div className="formatted-detail-text compact">
                                                        {job.carrier.benefit_other && renderFormattedText(job.carrier.benefit_other)}
                                                    </div>
                                                </div>
                                            )}

                                            {/* Orientation */}
                                            {(job.orientation_details || job.orientation_table) && (
                                                <div className="card-detail-text-section secondary">
                                                    <h4 className="detail-group-title">Orientation</h4>
                                                    {job.orientation_details && (
                                                        <div className="formatted-detail-text">{renderFormattedText(job.orientation_details)}</div>
                                                    )}
                                                    {job.orientation_table && (
                                                        <div className="mini-table-container">
                                                            {renderOrientationTable(job.orientation_table)}
                                                        </div>
                                                    )}
                                                </div>
                                            )}

                                            {/* Job Requirements */}
                                            {(job.account_type || job.drug_test_type || job.sap_required || job.transmissions) && (
                                                <div className="card-detail-text-section secondary">
                                                    <h4 className="detail-group-title">Job Requirements</h4>
                                                    <div className="requirements-mini-grid">
                                                        {job.account_type && <div><strong>Account:</strong> {job.account_type}</div>}
                                                        {job.drug_test_type && <div><strong>Drug Test:</strong> {job.drug_test_type}</div>}
                                                        {job.sap_required && <div><strong>SAP:</strong> {job.sap_required}</div>}
                                                        {job.transmissions && <div><strong>Transmission:</strong> {job.transmissions}</div>}
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>
                            );
                        })
                    )}
                </div>
            )
            }

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

                                    {/* Carrier Process & Qualifications */}
                                    {(selectedJob.carrier.presentation || selectedJob.carrier.pre_qualifications || selectedJob.carrier.app_process) && (
                                        <div className="lane-section" style={{ marginTop: '1rem', borderTop: '1px solid var(--border)', paddingTop: '1rem' }}>
                                            <h5 className="lane-section-title">Carrier Process & Qualifications</h5>
                                            <div className="lane-info-content">
                                                {selectedJob.carrier.presentation && (
                                                    <div className="lane-section">
                                                        <h5 className="lane-section-title">Presentation</h5>
                                                        <div className="lane-section-content">{renderGenericTable(selectedJob.carrier.presentation)}</div>
                                                    </div>
                                                )}
                                                {selectedJob.carrier.pre_qualifications && (
                                                    <div className="lane-section">
                                                        <h5 className="lane-section-title">Pre-Qualifications</h5>
                                                        <div className="lane-section-content">{renderGenericTable(selectedJob.carrier.pre_qualifications)}</div>
                                                    </div>
                                                )}
                                                {selectedJob.carrier.app_process && (
                                                    <div className="lane-section">
                                                        <h5 className="lane-section-title">Application Process</h5>
                                                        <div className="lane-section-content">{renderAppProcess(selectedJob.carrier.app_process)}</div>
                                                    </div>
                                                )}
                                            </div>
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

            {/* Carrier Info Side Panel */}
            {carrierInfoPanel && (
                <div className="modal-overlay" onClick={() => setCarrierInfoPanel(null)}>
                    <div className="modal-content job-details-modal" onClick={e => e.stopPropagation()} style={{ maxWidth: '900px' }}>
                        {/* Sticky Header Wrapper */}
                        <div className="modal-sticky-header">
                            <button className="close-btn" onClick={() => setCarrierInfoPanel(null)}>&times;</button>

                            <div className="job-modal-header" style={{ border: 'none', padding: 0, marginBottom: '1.5rem' }}>
                                <div className="job-modal-tags">
                                    {carrierInfoPanel.job.carrier?.name && (
                                        <span className="tag tag-company">{carrierInfoPanel.job.carrier.name}</span>
                                    )}
                                </div>
                                <h1 className="job-modal-title" style={{ display: 'flex', alignItems: 'center' }}>
                                    {carrierInfoPanel.type === 'presentation' && (
                                        <><img src={presentationIcon} alt="" className="btn-icon" /> Presentation</>
                                    )}
                                    {carrierInfoPanel.type === 'pre_qualifications' && (
                                        <><img src={preQualIcon} alt="" className="btn-icon" /> Pre-Qualifications</>
                                    )}
                                    {carrierInfoPanel.type === 'app_process' && (
                                        <><img src={appProcessIcon} alt="" className="btn-icon" /> Application Process</>
                                    )}
                                </h1>
                                <p className="job-modal-location">
                                    {carrierInfoPanel.job.title}
                                </p>
                            </div>

                            {/* Search Bar for Info */}
                            {(carrierInfoPanel.type === 'presentation' || carrierInfoPanel.type === 'pre_qualifications') && (
                                <div className="carrier-info-search-container">
                                    <div className="search-box">
                                        <img src={searchIcon} alt="search" className="search-icon" style={{ filter: 'grayscale(1) opacity(0.5)' }} />
                                        <input
                                            type="text"
                                            className="search-input"
                                            placeholder={`Search in ${carrierInfoPanel.type === 'presentation' ? 'presentation' : 'pre-qualifications'}...`}
                                            value={carrierSearchQuery}
                                            onChange={(e) => setCarrierSearchQuery(e.target.value)}
                                        />
                                        {carrierSearchQuery && (
                                            <button
                                                className="clear-search-btn"
                                                onClick={() => setCarrierSearchQuery('')}
                                                style={{ position: 'absolute', right: '10px', background: 'none', border: 'none', fontSize: '1.2rem', cursor: 'pointer', color: '#94a3b8' }}
                                            >
                                                &times;
                                            </button>
                                        )}
                                    </div>
                                </div>
                            )}

                        </div>


                        {/* Content */}
                        <div className="lane-info-container">
                            <div className="lane-side-label">
                                {carrierInfoPanel.type === 'presentation' && 'Presentation'}
                                {carrierInfoPanel.type === 'pre_qualifications' && 'Pre-Qualifications'}
                                {carrierInfoPanel.type === 'app_process' && 'Application Process'}
                            </div>
                            <div className="lane-info-content">
                                <div className="lane-section">
                                    {carrierInfoPanel.type === 'presentation' && carrierInfoPanel.job.carrier?.presentation && (
                                        <div className="lane-section-content">
                                            {renderGenericTable(carrierInfoPanel.job.carrier.presentation, carrierSearchQuery)}
                                        </div>
                                    )}
                                    {carrierInfoPanel.type === 'pre_qualifications' && carrierInfoPanel.job.carrier?.pre_qualifications && (
                                        <div className="lane-section-content">
                                            {renderGenericTable(carrierInfoPanel.job.carrier.pre_qualifications, carrierSearchQuery)}
                                        </div>
                                    )}
                                    {carrierInfoPanel.type === 'app_process' && carrierInfoPanel.job.carrier?.app_process && (
                                        <div className="lane-section-content">
                                            {renderAppProcess(carrierInfoPanel.job.carrier.app_process)}
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>

                        {/* Action Buttons */}
                        <div className="modal-actions">
                            <button
                                className="btn-secondary"
                                onClick={() => setCarrierInfoPanel(null)}
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

