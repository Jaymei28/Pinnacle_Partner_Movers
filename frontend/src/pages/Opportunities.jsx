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
    const [activeTab, setActiveTab] = useState('description');
    const [error, setError] = useState(null);
    const [zipCode, setZipCode] = useState('');
    const [searchZip, setSearchZip] = useState('');
    const [expandedJobId, setExpandedJobId] = useState(null);
    const [openDropdownId, setOpenDropdownId] = useState(null);
    const [carrierSearchQuery, setCarrierSearchQuery] = useState('');
    const [carrierInfoPanel, setCarrierInfoPanel] = useState(null);

    const toggleExpand = (jobId) => {
        setExpandedJobId(expandedJobId === jobId ? null : jobId);
    };

    const fetchJobs = async (driverZip = '') => {
        setLoading(true);
        setError(null);
        try {
            let url = API_URL;
            const params = new URLSearchParams();
            if (driverZip) params.append('zip_code', driverZip);

            const queryString = params.toString();
            if (queryString) url += `?${queryString}`;

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
        setSearchZip(zipCode.trim());
        fetchJobs(zipCode.trim());
    };

    const handleViewDetails = (job) => {
        setSelectedJob(job);
        setActiveTab('description');
    };

    const handleClearSearch = () => {
        setZipCode('');
        setSearchZip('');
        fetchJobs();
    };

    const toggleHiringStatus = async (e, job) => {
        e.stopPropagation(); // Prevent opening details modal if badge is clicked
        const newStatus = job.hiring_status === 'full' ? 'open' : 'full';
        try {
            await axios.patch(`${API_URL}${job.id}/`, { hiring_status: newStatus });
            setJobs(prevJobs => prevJobs.map(j =>
                j.id === job.id ? { ...j, hiring_status: newStatus } : j
            ));
        } catch (err) {
            console.error('Error updating status:', err);
        }
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
                <div className="premium-table-wrapper">
                    <table className="premium-data-table">
                        <tbody>
                            {filteredRows.map((row, idx) => (
                                <tr key={idx} className="table-data-row">
                                    {row.map((cell, i) => (
                                        <td key={i} className={idx === 0 ? "table-header-cell" : "table-value-cell"}>
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
                                <td className="table-value-cell" style={{ fontWeight: 'normal' }}>{row.cityState}</td>
                                <td className="table-value-cell">{row.days}</td>
                                <td className="table-value-cell" style={{ fontWeight: 'normal' }}>{row.time}</td>
                                <td className="table-value-cell">{row.address}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        );
    };

    const renderKeyDataTable = (text) => {
        if (!text) return null;
        let processedText = String(text).replace(/\\n/g, '\n');
        const lines = processedText.split('\n').map(line => line.trim()).filter(line => line.length > 0);

        if (lines.length === 0) return null;

        // Detect delimiter if not using colons
        let delimiter = null;
        if (!lines[0].includes(':')) {
            if (lines[0].includes('|')) delimiter = '|';
            else if (lines[0].includes(',')) delimiter = ',';
            else if (lines[0].includes('\t')) delimiter = '\t';
        }

        const splitLineDelimited = (line, delim) => {
            if (delim !== ',') return line.split(delim).map(c => c.trim());
            // Basic CSV split
            const result = [];
            let current = '';
            let inQuotes = false;
            for (let i = 0; i < line.length; i++) {
                if (line[i] === '"') inQuotes = !inQuotes;
                else if (line[i] === ',' && !inQuotes) {
                    result.push(current.trim());
                    current = '';
                } else {
                    current += line[i];
                }
            }
            result.push(current.trim());
            return result.map(c => c.replace(/^"|"$/g, ''));
        };

        return (
            <div className="premium-table-wrapper">
                <table className="premium-data-table">
                    <tbody>
                        {lines.map((line, index) => {
                            // Header Detection (Special case for "Category" and "Details")
                            const isTableHeading = (line.toLowerCase().includes('category') && (line.toLowerCase().includes('details') || line.toLowerCase().includes('value'))) ||
                                (index === 0 && delimiter && !line.includes(':'));

                            if (isTableHeading) {
                                const headers = delimiter ? splitLineDelimited(line, delimiter) : [line];
                                return (
                                    <tr key={index} className="table-header-row">
                                        {headers.map((h, i) => (
                                            <td key={i} className="table-header-cell" colSpan={headers.length === 1 ? "2" : "1"}>
                                                {h}
                                            </td>
                                        ))}
                                    </tr>
                                );
                            }

                            // Standard identification logic
                            const isBullet = /^[•\* \-]/.test(line);
                            const isBoldMarkdown = line.startsWith('**') && line.endsWith('**');
                            const cleanLine = line.replace(/^[•\* \-\s\"\'\s]+/, '').replace(/[\"\'\s]+$/, '').replace(/\*\*/g, '');

                            if (!cleanLine) return null;

                            // 1. Delimited Format (CSV/Pipe)
                            if (delimiter && line.includes(delimiter)) {
                                const parts = splitLineDelimited(line, delimiter);
                                if (parts.length >= 2) {
                                    return (
                                        <tr key={index} className="table-data-row">
                                            <td className="table-label-cell">{parts[0]}</td>
                                            <td className="table-value-cell">{renderFormattedText(parts.slice(1).join(' '), true)}</td>
                                        </tr>
                                    );
                                }
                            }

                            // 2. Colon Format (Key: Value)
                            if (cleanLine.includes(':')) {
                                const colonIndex = cleanLine.indexOf(':');
                                const label = cleanLine.substring(0, colonIndex).trim();
                                const value = cleanLine.substring(colonIndex + 1).trim();

                                return (
                                    <tr key={index} className="table-data-row">
                                        <td className="table-label-cell">{label}</td>
                                        <td className="table-value-cell">{renderFormattedText(value, true)}</td>
                                    </tr>
                                );
                            }

                            // 3. Header/Title Format
                            const endsWithPunctuation = /[.\?!]$/.test(cleanLine.trim());
                            const isShort = cleanLine.length < 50;
                            const alphaContent = cleanLine.replace(/[^a-zA-Z]/g, '');
                            const isCapsLock = alphaContent.length > 2 && alphaContent === alphaContent.toUpperCase();
                            const isProbablyHeader = isBoldMarkdown || isCapsLock || (!isBullet && isShort && !endsWithPunctuation);

                            if (isProbablyHeader) {
                                return (
                                    <tr key={index} className="table-header-row">
                                        <td colSpan="2" className="table-header-cell">
                                            {cleanLine}
                                        </td>
                                    </tr>
                                );
                            }

                            // 4. Default Row
                            return (
                                <tr key={index} className="table-data-row">
                                    <td colSpan="2" className="table-full-cell">
                                        {isBullet && <span className="bullet-dot">•</span>}
                                        {renderFormattedText(cleanLine, true)}
                                    </td>
                                </tr>
                            );
                        })}
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
            <div className="opportunities-filters-row">
                <div className="search-zip-container-new">
                    <input
                        type="text"
                        className="filter-zip-input"
                        placeholder="Search job zipcode"
                        value={zipCode}
                        onChange={(e) => setZipCode(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                        maxLength="5"
                    />
                    {zipCode && (
                        <button className="btn-clear-zip" onClick={handleClearSearch}>&times;</button>
                    )}
                </div>

                <div className="filter-buttons">
                    <button className="btn-search-main" onClick={handleSearch}>Search</button>
                </div>
            </div>

            <div className="jobs-count-row">
                Showing {jobs.length} jobs
            </div>

            {loading ? (
                <div className="status-msg">Loading jobs...</div>
            ) : error ? (
                <div className="status-msg error">{error}</div>
            ) : (
                <div className="jobs-table-container">
                    <table className="jobs-listing-table">
                        <thead>
                            <tr className="table-header-row-static">
                                <th className="th-carrier">Carrier</th>
                                <th className="th-title">Title</th>
                                <th className="th-status">Hiring</th>
                                <th className="th-exp">Experience</th>
                                <th className="th-driver">Driver Type</th>
                                <th className="th-freight">Freight</th>
                                <th className="th-hometime">Home Time</th>
                                <th className="th-actions"></th>
                            </tr>
                        </thead>
                        <tbody>
                            {jobs.length === 0 ? (
                                <tr>
                                    <td colSpan="8" className="empty-table-msg">
                                        No jobs available matching your criteria.
                                    </td>
                                </tr>
                            ) : (
                                jobs.map(job => (
                                    <tr key={job.id} className="job-table-row">
                                        <td className="td-carrier">
                                            {job.carrier?.logo ? (
                                                <img src={job.carrier.logo} alt="" className="table-carrier-logo" />
                                            ) : (
                                                <div className="table-carrier-placeholder">{job.carrier?.name?.charAt(0)}</div>
                                            )}
                                        </td>
                                        <td className="td-title">
                                            <div className="job-title-link" onClick={() => handleViewDetails(job)}>{job.title}</div>
                                            <div className="job-pay-sub">
                                                <svg viewBox="0 0 24 24" className="pay-arrow-icon"><path d="M11 17l-5-5 5-5M18 12H6" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" /></svg>
                                                Avg. Weekly Pay: {job.average_weekly_pay || '$1,300 - 2,100'}
                                            </div>
                                        </td>
                                        <td className="td-status">
                                            <span
                                                className={`status-badge editable ${job.hiring_status === 'full' ? 'status-full' : 'status-open'}`}
                                                onClick={(e) => toggleHiringStatus(e, job)}
                                                title="Click to toggle status"
                                            >
                                                {job.hiring_status === 'full' ? 'Marked as full' : 'Open to hiring'}
                                            </span>
                                        </td>
                                        <td className="td-exp">{job.experience_required || '12 months'}</td>
                                        <td className="td-driver">{job.driver_type || 'Lease Purchase'}</td>
                                        <td className="td-freight">{job.freight_type || 'Dry Van'}</td>
                                        <td className="td-hometime">{job.home_time || 'Bi-Weekly'}</td>
                                        <td className="td-actions">
                                            <button className="btn-view-eye" onClick={() => handleViewDetails(job)}>
                                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" /></svg>
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            )}

            {selectedJob && (
                <div className="modal-overlay" onClick={() => setSelectedJob(null)}>
                    <div className="modal-content job-details-modal tabbed-modal" onClick={e => e.stopPropagation()}>
                        {/* MODAL HEADER */}
                        <div className="tabbed-modal-header">
                            <div className="modal-header-left">
                                <button className="close-button-new" onClick={() => setSelectedJob(null)}>&times;</button>
                                {selectedJob.carrier?.logo ? (
                                    <img src={selectedJob.carrier.logo} alt={selectedJob.carrier.name} className="modal-carrier-logo" />
                                ) : (
                                    <div className="modal-carrier-logo-placeholder">{selectedJob.carrier?.name?.charAt(0)}</div>
                                )}
                                <div className="modal-title-box">
                                    <h2 className="modal-main-title">{selectedJob.title}</h2>
                                    <p className="modal-sub-title">↳ <span>{selectedJob.carrier?.name}</span></p>
                                </div>
                            </div>
                        </div>

                        <div className="tabbed-modal-body">
                            {/* SIDEBAR TABS */}
                            <div className="modal-tabs-sidebar">
                                <button className={`modal-tab-btn ${activeTab === 'description' ? 'active' : ''}`} onClick={() => setActiveTab('description')}>Job Description</button>
                                <button className={`modal-tab-btn ${activeTab === 'pay' ? 'active' : ''}`} onClick={() => setActiveTab('pay')}>Pay Details</button>
                                <button className={`modal-tab-btn ${activeTab === 'equipment' ? 'active' : ''}`} onClick={() => setActiveTab('equipment')}>Equipment</button>
                                <button className={`modal-tab-btn ${activeTab === 'disqualifiers' ? 'active' : ''}`} onClick={() => setActiveTab('disqualifiers')}>Key Disqualifiers</button>
                                <button className={`modal-tab-btn ${activeTab === 'benefits' ? 'active' : ''}`} onClick={() => setActiveTab('benefits')}>Benefits</button>
                                <button className={`modal-tab-btn ${activeTab === 'requirements' ? 'active' : ''}`} onClick={() => setActiveTab('requirements')}>Requirements</button>
                                <button className={`modal-tab-btn ${activeTab === 'app_process' ? 'active' : ''}`} onClick={() => setActiveTab('app_process')}>Application Process</button>
                            </div>

                            {/* MAIN CONTENT AREA */}
                            <div className="modal-tab-content">
                                <div className="tab-pane-container">
                                    {activeTab === 'description' && (
                                        <div className="job-summary-container">
                                            {renderKeyDataTable(selectedJob.job_details)}
                                        </div>
                                    )}

                                    {activeTab === 'pay' && (
                                        <div className="job-summary-container">
                                            {renderKeyDataTable(selectedJob.pay_details)}
                                        </div>
                                    )}

                                    {activeTab === 'equipment' && (
                                        <div className="job-summary-container">
                                            {renderKeyDataTable(selectedJob.equipment_details)}
                                        </div>
                                    )}

                                    {activeTab === 'disqualifiers' && (
                                        <div className="job-summary-container">
                                            {renderKeyDataTable(selectedJob.key_disqualifiers)}
                                        </div>
                                    )}

                                    {activeTab === 'benefits' && (
                                        <div className="premium-table-wrapper">
                                            <table className="premium-data-table">
                                                <tbody>
                                                    <tr className="table-header-row">
                                                        <td className="table-header-cell">Category</td>
                                                        <td className="table-header-cell">Details</td>
                                                    </tr>
                                                    {selectedJob.carrier?.benefit_medical_dental_vision && (
                                                        <tr className="table-data-row">
                                                            <td className="table-label-cell">Medical / Dental / Vision</td>
                                                            <td className="table-value-cell">{selectedJob.carrier.benefit_medical_dental_vision}</td>
                                                        </tr>
                                                    )}
                                                    {selectedJob.carrier?.benefit_401k && (
                                                        <tr className="table-data-row">
                                                            <td className="table-label-cell">401(k) Retirement</td>
                                                            <td className="table-value-cell">{selectedJob.carrier.benefit_401k}</td>
                                                        </tr>
                                                    )}
                                                    {selectedJob.carrier?.benefit_paid_vacation && (
                                                        <tr className="table-data-row">
                                                            <td className="table-label-cell">Paid Vacation</td>
                                                            <td className="table-value-cell">{selectedJob.carrier.benefit_paid_vacation}</td>
                                                        </tr>
                                                    )}
                                                    {selectedJob.carrier?.benefit_weekly_paycheck && (
                                                        <tr className="table-data-row">
                                                            <td className="table-label-cell">Weekly Pay</td>
                                                            <td className="table-value-cell">{selectedJob.carrier.benefit_weekly_paycheck}</td>
                                                        </tr>
                                                    )}
                                                </tbody>
                                            </table>
                                        </div>
                                    )}

                                    {activeTab === 'requirements' && (
                                        <div className="job-summary-container">
                                            {renderKeyDataTable(selectedJob.requirements_details)}
                                        </div>
                                    )}

                                    {activeTab === 'app_process' && (
                                        <div className="lane-section-content">
                                            {selectedJob.carrier?.app_process ? renderAppProcess(selectedJob.carrier.app_process) : 'Please contact the carrier for application details.'}
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Carrier Info Side Panel */}
            {
                carrierInfoPanel && (
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
                )
            }
        </div >
    );
};

export default Opportunities;

