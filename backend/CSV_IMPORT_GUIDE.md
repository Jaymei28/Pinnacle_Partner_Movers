# CSV Import Format Guide for Jobs & Carriers

## 📋 Simple CSV Format (Recommended)

This is the easiest format to use. Just create a CSV file with these columns:

### Required Columns:
```csv
carrier_name,job_title,zip_code,salary,home_time
```

### Optional Columns (add what you have):
```csv
state,city,experience_required,driver_type,freight_type,equipment_type,states_covered,description,benefits,orientation
```

---

## 📝 Example CSV File

Here's a complete example you can copy and paste:

```csv
carrier_name,job_title,zip_code,state,city,salary,home_time,experience_required,driver_type,freight_type,states_covered,description
Swift Transportation,CDL-A Truck Driver - Phoenix,85001,AZ,Phoenix,$1200 Weekly,Daily,0 Months,Company Driver,No Touch,"AZ,CA,NV","Long haul trucking position with competitive pay and benefits"
Walmart,CDL-A Driver - Opelika AL,36801,AL,Opelika,$1300 Weekly,Daily,6 Months,Company Driver,No Touch Freight,"AL,GA,FL","Walmart dedicated route with consistent schedule"
Schneider,Regional Driver,,NC,Charlotte,$1100 Weekly,Home Daily,3 Months,Company Driver,Driver Unload,"NC,SC,VA","Regional routes with home time daily"
JB Hunt,OTR Driver,,TX,Dallas,$1400 Weekly,Weekly,12 Months,Company Driver,Drop and Hook,"TX,OK,LA,AR","Over the road position with weekly home time"
```

**Notice:** The 3rd and 4th jobs don't have ZIP codes - that's OK! The system will use the carrier's headquarters ZIP code automatically.

---

## 🎯 What Happens When You Import

### If Job Has ZIP Code:
```
✅ Job: "CDL-A Driver - Phoenix, ZIP: 85001"
→ System geocodes 85001 to Phoenix coordinates
→ Saves as location_source: "job_zip"
→ Drivers see exact distance
```

### If Job Has NO ZIP Code:
```
❌ Job: "Regional Driver, ZIP: (empty)"
✅ Carrier: "Schneider, HQ ZIP: 53711" (Green Bay, WI)
→ System uses carrier HQ coordinates
→ Saves as location_source: "carrier_hq"
→ Drivers see blue badge: "📍 Location based on carrier headquarters"
```

### If Nothing Has ZIP Code:
```
❌ Job: ZIP (empty)
❌ Carrier: HQ ZIP (empty)
✅ Job has state: "NC"
→ System saves as location_source: "state_only"
→ Drivers see amber badge: "⚠️ Regional opportunity - contact for exact location"
```

---

## 📊 Column Descriptions

| Column Name | Required? | Example | Notes |
|------------|-----------|---------|-------|
| **carrier_name** | ✅ Yes | "Swift Transportation" | Company name (will create carrier if doesn't exist) |
| **job_title** | ✅ Yes | "CDL-A Driver - Phoenix" | Job title/description |
| **zip_code** | ⚠️ Recommended | "85001" | 5-digit ZIP code (leave empty if unknown) |
| **state** | ⚠️ Recommended | "AZ" | 2-letter state code (used for fallback) |
| **city** | Optional | "Phoenix" | City name |
| **salary** | ⚠️ Recommended | "$1200 Weekly" | Pay information |
| **home_time** | ⚠️ Recommended | "Daily" or "Weekly" | How often driver goes home |
| **experience_required** | Optional | "6 Months" | Minimum experience |
| **driver_type** | Optional | "Company Driver" | Type of driver position |
| **freight_type** | Optional | "No Touch" | Type of freight handling |
| **equipment_type** | Optional | "Dry Van" | Type of truck/trailer |
| **states_covered** | Optional | "AZ,CA,NV" | States the route covers (comma-separated) |
| **description** | Optional | "Long haul position..." | Detailed job description |
| **benefits** | Optional | "Medical, 401k, PTO" | Benefits offered |
| **orientation** | Optional | "3 days in Phoenix" | Orientation details |

---

## 🏢 Carrier Information (Optional)

If you want to add carrier headquarters information, you can create a separate carriers CSV:

```csv
carrier_name,headquarters_zip,headquarters_city,headquarters_state,benefits
Swift Transportation,85034,Phoenix,AZ,"Medical/Dental/Vision, 401k, Paid Vacation, Stock Purchase"
Walmart,72716,Bentonville,AR,"Medical/Dental/Vision, 401k, Paid Vacation"
Schneider,53711,Green Bay,WI,"Medical/Dental/Vision, 401k"
```

**Or** the system will automatically create carriers from the jobs CSV using just the carrier name.

---

## 🚀 How to Import

### Step 1: Create Your CSV File
1. Open Excel or Google Sheets
2. Copy the example format above
3. Fill in your job data
4. Save as CSV file (e.g., `my_jobs.csv`)

### Step 2: Upload to Backend Folder
Put your CSV file in the `backend` folder:
```
backend/
  ├── my_jobs.csv  ← Your file here
  ├── import_jobs_from_csv.py
  └── manage.py
```

### Step 3: Run the Import Script
Open terminal in the `backend` folder and run:
```bash
python import_jobs_from_csv.py
```

The script will:
- ✅ Create carriers automatically
- ✅ Create jobs with all details
- ✅ Geocode ZIP codes automatically
- ✅ Use carrier HQ as fallback
- ✅ Show you a summary of what was imported

---

## 💡 Pro Tips

### Tip 1: Leave ZIP Code Empty If Unknown
```csv
carrier_name,job_title,zip_code,state
Swift,Regional Driver,,AZ
```
The system will use Swift's headquarters ZIP automatically!

### Tip 2: Use Commas for Multiple States
```csv
states_covered
"AZ,CA,NV,UT"
```
Put quotes around it if it has commas.

### Tip 3: Add Detailed Descriptions
```csv
description
"This is a great job with:
- Weekly home time
- $1200 average pay
- No touch freight
- Modern equipment"
```
Use quotes for multi-line descriptions.

### Tip 4: Import Carriers First (Optional)
If you want to set up carrier headquarters before importing jobs:
1. Create `carriers.csv` with HQ information
2. Import carriers first
3. Then import jobs

---

## ⚠️ Common Mistakes to Avoid

❌ **Don't use fake ZIP codes**
```csv
zip_code
99999  ← BAD! Leave empty instead
```

❌ **Don't forget quotes for comma-separated values**
```csv
states_covered
AZ,CA,NV  ← BAD! Will split into separate columns
"AZ,CA,NV"  ← GOOD!
```

❌ **Don't use special characters in carrier names**
```csv
carrier_name
Swift & Co.  ← OK, but be consistent
Swift & Co   ← Different! Will create 2 carriers
```

---

## 📞 Need Help?

If you get errors during import:
1. Check that all required columns are present
2. Make sure ZIP codes are 5 digits (or empty)
3. Make sure state codes are 2 letters (or empty)
4. Check for extra commas or quotes

The import script will show you exactly which row has an error!

---

## 🎉 That's It!

Your CSV format is simple:
1. **carrier_name** - Who's hiring
2. **job_title** - What's the job
3. **zip_code** - Where (or leave empty)
4. **Everything else** - Optional details

The system handles the rest automatically! 🚛✨
