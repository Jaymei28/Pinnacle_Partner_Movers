# 📋 EXACT Database Fields - Simplified Structure

## ✅ CARRIER FIELDS (20 fields total)
(No changes requested for Carriers - Benefits and Process remain granular)

## ✅ JOB FIELDS (10 fields total)

### Basic Identification & Location (5 fields)
1. `carrier` ✅ REQUIRED - Linked to Carrier name
2. `title` ✅ REQUIRED - Job title
3. `state` ✅ REQUIRED - Primary state
4. `zip_code` - Job zip code
5. `hiring_radius_miles` - Default 50

### Consolidated Sections (5 fields - Text/Bullets)
6. `job_details` - All job highlights, account overview, and description.
7. `pay_details` - All compensation, bonuses, and pay structure info.
8. `equipment_details` - All truck specs, engine, bunk, and transmission info.
9. `key_disqualifiers` - Critical reasons for disqualification.
10. `requirements_details` - Experience, drug tests, SAP, and other qualifications.

---

## 🎯 Import Strategy
For each section, paste the entire block of text from your source sheet into the single corresponding field. Use line breaks or bullets for readability!
