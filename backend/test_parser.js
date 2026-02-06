// Test the parser with actual data
const description = `Walmart – Arcadia, FL
Job Details

Experience Required: Trainee; 6 months experience
Home Time: Home daily
Shift/Schedule: NIGHT
Weekend Work: YES
Holiday Work Expectations: Based on Walmart shipping schedule; holiday nights required
Average Weekly Pay: $1,300
Pay Range: $0.43–$0.51 CPM
Weekly Mileage: 2,200
Short Haul Pay: $30 for loads under 90 miles
Stop Pay: $10.00
Load/Unload: Live Unload
Unload Pay: N/A
Bonus Offer: Swift Driver Performance Bonus
Transition Bonus: NO
Pertinent Lane Information: 2 runs per day
Primary lanes: Arcadia, Port Charlotte, Cape Coral, Punta Gorda, Englewood, North Port
Slip seat
Preferred workdays: Thursday–Monday or Friday–Tuesday

Account Overview

Region: East
Hub State: FL
Hub City: Arcadia
Hiring State(s): FL
Total Drivers Needed (Solo): 5 – CLOSED
Total Drivers Needed (Team): 0 – CLOSED
Total Drivers Needed by State: Florida
Hiring Area Zip Code(s): 34269
Must Live Within: 25 miles of 33982
Trainees Accepted: YES
Teams Accepted: NO`;

function parseLaneInformation(description) {
    if (!description) return [];

    let text = description.replace(/\\n/g, '\n');
    const sections = [];
    let currentSection = { title: 'Job Details', items: [] };
    const lines = text.split('\n');

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();
        if (!line) continue;

        // Check if this looks like a section header:
        // - Short line (< 50 chars)
        // - No colon
        const isShortLine = line.length < 50;
        const hasNoColon = !line.includes(':');

        // Section header detection: short line without colon, and has content before it
        if (isShortLine && hasNoColon && currentSection.items.length > 0) {
            sections.push(currentSection);
            currentSection = { title: line, items: [] };
        }
        // Labeled items (key: value)
        else if (line.includes(':')) {
            const colonIndex = line.indexOf(':');
            const label = line.substring(0, colonIndex).trim();
            const value = line.substring(colonIndex + 1).trim();

            // Only treat as label-value if label is reasonable
            if (label.length > 0 && label.length < 50) {
                currentSection.items.push({ label, value, type: 'labeled' });
            } else {
                currentSection.items.push({ text: line, type: 'text' });
            }
        }
        // Regular text
        else {
            currentSection.items.push({ text: line, type: 'text' });
        }
    }

    if (currentSection && currentSection.items.length > 0) {
        sections.push(currentSection);
    }

    return sections;
}

const result = parseLaneInformation(description);
console.log(JSON.stringify(result, null, 2));
