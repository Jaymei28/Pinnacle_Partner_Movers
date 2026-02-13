# 📋 Complete CSV Template Reference

## 🎯 Available Templates

I've created **4 different CSV templates** for you to choose from:

### 1. **TEMPLATE_MINIMAL.csv** (4 columns)
**Use when:** You just want to get started quickly
```
carrier_name, title, state, zip_code
```

### 2. **TEMPLATE_RECOMMENDED.csv** (11 columns)
**Use when:** You want the most common fields
```
carrier_name, title, state, zip_code, salary, home_time, experience_levels, 
driver_types, freight_types, states, description
```

### 3. **TEMPLATE_WITH_BENEFITS.csv** (17 columns)
**Use when:** You want to include carrier benefits
```
All recommended fields PLUS:
headquarters_zip, headquarters_city, headquarters_state,
benefit_401k, benefit_medical_dental_vision, benefit_paid_vacation
```

### 4. **TEMPLATE_COMPLETE.csv** (50 columns) ⭐ NEW!
**Use when:** You want EVERY available field
```
ALL carrier fields + ALL job fields including:
- All pay details (pay_range, bonus_offer, stop_pay, etc.)
- All benefits (401k, medical, vacation, etc.)
- Orientation details
- Job requirements (cameras, transmissions, drug test, etc.)
- Administrative details
- And more!
```

---

## 📊 Complete Field List (50 Fields Total)

### 🏢 CARRIER FIELDS (13 fields)

#### Basic Information
1. `carrier_name` ✅ REQUIRED
2. `headquarters_zip`
3. `headquarters_city`
4. `headquarters_state`
5. `website`
6. `contact_email`
7. `contact_phone`
8. `carrier_description`

#### Benefits
9. `benefit_401k`
10. `benefit_disability_life`
11. `benefit_stock_purchase`
12. `benefit_medical_dental_vision`
13. `benefit_paid_vacation`
14. `benefit_prescription_drug`
15. `benefit_weekly_paycheck`
16. `benefit_driver_ranking_bonus`
17. `benefit_military_program`
18. `benefit_tuition_program`
19. `benefit_other`

### 🚛 JOB FIELDS (37 fields)

#### Basic Information
20. `title` ✅ REQUIRED
21. `state` ✅ REQUIRED
22. `zip_code` ⚠️ RECOMMENDED
23. `hiring_radius_miles`

#### Pay Details
24. `pay_range`
25. `average_weekly_pay`
26. `salary`
27. `pay_type`
28. `short_haul_pay`
29. `stop_pay`
30. `bonus_offer`
31. `unload_pay`

#### Home Time & Schedule
32. `exact_home_time`
33. `home_time`

#### Load/Unload
34. `load_unload_type`

#### Lane Information
35. `job_details`
36. `account_overview`
37. `administrative_details`
38. `description`

#### Orientation
39. `orientation_details`
40. `orientation_table`

#### Job Requirements (Multi-Select)
41. `trainees_accepted`
42. `account_type`
43. `cameras`
44. `driver_types`
45. `drug_test_type`
46. `experience_levels`
47. `freight_types`
48. `sap_required`
49. `transmissions`
50. `states`

---

## 🎨 How to Use Each Template

### For TEMPLATE_COMPLETE.csv:

**Pros:**
- ✅ Includes every possible field
- ✅ No need to add columns later
- ✅ Perfect for comprehensive data entry

**Cons:**
- ⚠️ Many columns (50 total)
- ⚠️ Can be overwhelming
- ⚠️ Most fields are optional

**Best for:** 
- Detailed job postings
- When you have complete carrier information
- Large-scale data imports

### For TEMPLATE_WITH_BENEFITS.csv:

**Pros:**
- ✅ Includes carrier benefits
- ✅ Manageable number of columns (17)
- ✅ Shows carrier HQ information

**Cons:**
- ⚠️ Missing some detailed fields

**Best for:**
- When you want to highlight carrier benefits
- Balanced between simple and complete

### For TEMPLATE_RECOMMENDED.csv:

**Pros:**
- ✅ Just the essentials (11 columns)
- ✅ Easy to fill out
- ✅ Covers 90% of use cases

**Cons:**
- ⚠️ No carrier benefits
- ⚠️ No detailed orientation info

**Best for:**
- Quick job imports
- When you don't have detailed carrier info
- Getting started fast

### For TEMPLATE_MINIMAL.csv:

**Pros:**
- ✅ Fastest to fill out (4 columns)
- ✅ Only required fields
- ✅ Perfect for testing

**Cons:**
- ⚠️ Very basic
- ⚠️ Missing most details

**Best for:**
- Testing the import system
- Placeholder data
- Absolute minimum

---

## 💡 Pro Tips

### Tip 1: Start Small, Grow Later
1. Start with **TEMPLATE_RECOMMENDED.csv**
2. Import a few test jobs
3. Later, switch to **TEMPLATE_COMPLETE.csv** for full details

### Tip 2: Mix and Match
- You don't need to fill EVERY column in TEMPLATE_COMPLETE
- Leave columns empty if you don't have the data
- The system handles missing data gracefully

### Tip 3: Copy the Headers
For Google Sheets, copy the entire first row from any template and paste it into Row 1.

### Tip 4: Use TEMPLATE_COMPLETE as Reference
Even if you use a smaller template, keep TEMPLATE_COMPLETE open to see what fields are available.

---

## 📁 Template Files

All templates are in your `backend` folder:

1. [TEMPLATE_MINIMAL.csv](file:///c:/Users/Jaymei/.gemini/antigravity/scratch/job-portal/backend/TEMPLATE_MINIMAL.csv) - 4 columns
2. [TEMPLATE_RECOMMENDED.csv](file:///c:/Users/Jaymei/.gemini/antigravity/scratch/job-portal/backend/TEMPLATE_RECOMMENDED.csv) - 11 columns
3. [TEMPLATE_WITH_BENEFITS.csv](file:///c:/Users/Jaymei/.gemini/antigravity/scratch/job-portal/backend/TEMPLATE_WITH_BENEFITS.csv) - 17 columns
4. [TEMPLATE_COMPLETE.csv](file:///c:/Users/Jaymei/.gemini/antigravity/scratch/job-portal/backend/TEMPLATE_COMPLETE.csv) - 50 columns ⭐ NEW!

---

## ✅ Which Template Should I Use?

**Choose based on your needs:**

- 🏃 **Need it fast?** → TEMPLATE_MINIMAL
- 📊 **Most common use?** → TEMPLATE_RECOMMENDED
- 🎁 **Want to show benefits?** → TEMPLATE_WITH_BENEFITS
- 🎯 **Want everything?** → TEMPLATE_COMPLETE

**My recommendation:** Start with **TEMPLATE_RECOMMENDED** or **TEMPLATE_WITH_BENEFITS**!

---

## 🚀 Next Steps

1. Choose your template
2. Open it in Excel or Google Sheets
3. Fill in your job data
4. Export as CSV
5. Run: `python manage.py import_jobs your_file.csv`

Done! 🎉
