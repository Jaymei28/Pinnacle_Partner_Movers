# 📋 EXACT Database Fields - No Extras!

## ✅ CARRIER FIELDS (20 fields total)

### Basic Information (6 fields)
1. `name` ✅ REQUIRED - Company name
2. `description` - Company overview
3. `website` - Company website URL
4. `contact_email` - Contact email
5. `contact_phone` - Contact phone
6. `logo` - Company logo (file upload, not in CSV)

### Headquarters Location (3 fields)
7. `headquarters_zip` - HQ ZIP code
8. `headquarters_city` - HQ city
9. `headquarters_state` - HQ state (2-letter)

### Benefits (11 fields)
10. `benefit_401k`
11. `benefit_disability_life`
12. `benefit_stock_purchase`
13. `benefit_medical_dental_vision`
14. `benefit_paid_vacation`
15. `benefit_prescription_drug`
16. `benefit_weekly_paycheck`
17. `benefit_driver_ranking_bonus`
18. `benefit_military_program`
19. `benefit_tuition_program`
20. `benefit_other`

### Auto-Generated (Don't include in CSV)
- `is_active`
- `created_at`
- `updated_at`

---

## ✅ JOB FIELDS (32 fields total)

### Basic Information (4 fields)
1. `title` ✅ REQUIRED
2. `state` ✅ REQUIRED
3. `zip_code` ⚠️ RECOMMENDED
4. `hiring_radius_miles` - Default: 50

### Pay Details (8 fields)
5. `pay_range`
6. `average_weekly_pay`
7. `salary`
8. `pay_type`
9. `short_haul_pay`
10. `stop_pay`
11. `bonus_offer`
12. `unload_pay`

### Home Time (2 fields)
13. `exact_home_time`
14. `home_time`

### Load/Unload (1 field)
15. `load_unload_type`

### Lane Information (4 fields)
16. `job_details`
17. `account_overview`
18. `administrative_details`
19. `description`

### Orientation (2 fields)
20. `orientation_details`
21. `orientation_table`

### Requirements (11 fields - comma-separated)
22. `trainees_accepted`
23. `account_type`
24. `cameras`
25. `driver_types`
26. `drug_test_type`
27. `experience_levels`
28. `freight_types`
29. `sap_required`
30. `transmissions`
31. `states`

### Auto-Generated (Don't include in CSV)
- `latitude`
- `longitude`
- `location_source`
- `zip_source`
- `is_active`
- `created_at`
- `updated_at`
- `source_create_date`
- `source_modified_date`

---

## 📊 CSV Templates Available

### TEMPLATE_MINIMAL.csv (4 columns)
```
carrier_name,title,state,zip_code
```

### TEMPLATE_WITH_BENEFITS.csv (17 columns)
```
carrier_name,title,state,zip_code,salary,home_time,experience_levels,
driver_types,freight_types,states,description,headquarters_zip,
headquarters_city,headquarters_state,benefit_401k,
benefit_medical_dental_vision,benefit_paid_vacation
```

### TEMPLATE_COMPLETE.csv (49 columns)
```
ALL carrier fields + ALL job fields
(Everything listed above except auto-generated fields)
```

---

## ✅ Field Count Summary

**Carrier:** 20 user-editable fields  
**Job:** 32 user-editable fields  
**Total CSV columns:** 49 (carrier_name + 31 job fields + 17 carrier fields)

**Note:** `carrier_name` is used in CSV to link jobs to carriers. The actual carrier `name` field gets populated from this.

---

## 🎯 These Are Your EXACT Database Fields

No extras, no made-up fields - just what's actually in your database! 🎉
