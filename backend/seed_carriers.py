"""
Seed all 8 carriers into the database with benefits pre-filled from PDF.
App process / presentation / pre_qualifications are left blank for manual entry.

Run: py seed_carriers.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobstream_backend.settings')
django.setup()

from jobs.models import Carrier

carriers = [
    {
        'name': 'Swift Transportation',
        'website': 'https://www.swifttrans.com',
        'contact_email': 'recruiting@swifttrans.com',
        'contact_phone': '1-800-800-2200',
        'description': (
            'Swift Transportation is one of the largest full-truckload carriers in North America, '
            'offering dedicated, regional, OTR, intermodal, and flatbed positions. '
            'Known for strong driver programs, training academies, and nationwide coverage.'
        ),
        'headquarters_city': 'Phoenix',
        'headquarters_state': 'AZ',
        'headquarters_zip': '85043',
        'benefit_401k': (
            'Company-sponsored retirement savings plan with contribution matching options.'
        ),
        'benefit_disability_life': (
            'Disability, Life, Accident & Critical Illness Coverage.\n'
            'Comprehensive protection including disability income, life insurance, and accident and critical illness plans.'
        ),
        'benefit_stock_purchase': (
            'Employees can invest in company stock through an employee stock purchase program.'
        ),
        'benefit_medical_dental_vision': (
            'Full health coverage with medical, dental, and vision insurance options.\n'
            'Benefits eligibility starts after 30 days.\n'
            'Insurance provider: Aetna.'
        ),
        'benefit_paid_vacation': (
            'Drivers earn paid vacation time based on tenure and employment status.'
        ),
        'benefit_prescription_drug': (
            'Coverage for prescription medications through available health insurance options.'
        ),
        'benefit_weekly_paycheck': (
            'Drivers receive consistent weekly paychecks.'
        ),
        'benefit_driver_ranking_bonus': (
            'Bonuses based on miles driven.\n'
            'Rewarded for commitment to safety.\n'
            'On-time delivery performance.\n'
            'Customer service record.\n'
            'Total employment duration.'
        ),
        'benefit_military_program': (
            'Eligible for the Military Apprenticeship Program.\n'
            'Approved for GI Bill use.\n'
            'Veterans can earn pay while completing on-the-job CDL training.'
        ),
        'benefit_tuition_program': (
            'Debt-Free Tuition Program:\n'
            '- Eligible Knight-Swift employees can eliminate the cost of college.\n'
            '- Online study options available while working.\n'
            '- Access to over 50 carrier-focused degree programs.'
        ),
        'benefit_other': (
            'Swift Academy CDL training available at 13+ locations nationwide.\n'
            'Single occupancy lodging provided during orientation.\n'
            'Bus transportation or Greyhound reimbursement for travel to orientation.'
        ),
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'JB Hunt',
        'website': 'https://www.jbhunt.com',
        'contact_email': 'DTW.support@jbhunt.com',
        'contact_phone': '1-833-272-7504',
        'description': (
            'JB Hunt Transport Services is a Fortune 500 transportation and logistics company. '
            'Known for dedicated, intermodal, and local operations with industry-leading technology '
            'and driver support through their Direct To Work orientation program.'
        ),
        'headquarters_city': 'Lowell',
        'headquarters_state': 'AR',
        'headquarters_zip': '72745',
        'benefit_401k': (
            '401(k) with company match.\n'
            'PTO accrues from day one.'
        ),
        'benefit_disability_life': (
            'Access to life insurance options.\n'
            'Access to mental health and disability benefits.'
        ),
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': (
            'Eligible for medical, dental and vision coverage after just 30 days.'
        ),
        'benefit_paid_vacation': (
            'PTO accrues from day one.\n'
            'Paid online training - $125 total.'
        ),
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': (
            'Weekly pay. Direct deposit.'
        ),
        'benefit_driver_ranking_bonus': (
            'Activity-based pay plan.\n'
            'Safety bonus opportunities.\n'
            'New hire transition bonus available on select accounts.'
        ),
        'benefit_military_program': '',
        'benefit_tuition_program': '',
        'benefit_other': (
            'Direct To Work Orientation:\n'
            '- No travel to a JB Hunt terminal for orientation.\n'
            '- No overnight hotel stays.\n'
            '- Local drug screen testing in your city of residency for convenience.\n'
            '- Paid online training – $125 total.\n'
            '- Drivers can schedule screenings and complete the online training at their convenience.\n\n'
            'Driver Expectations on Assignment:\n'
            '- Send images of front and back of CDL and most recent DOT medical card to DTW.Support@jbhunt.com WITHIN 24 HOURS.\n'
            '- Electronically sign Disclosures and Authorization forms for background check initiation WITHIN 24 HOURS.\n'
            '- Complete online training WITHIN 72 HOURS OF ASSIGNMENT.\n'
            '- Electronically sign completed background check WITHIN 24 HOURS OF REQUEST.\n'
            '- Does not include Truckload orientation.'
        ),
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'US Xpress',
        'website': 'https://www.usxpress.com',
        'contact_email': '',
        'contact_phone': '',
        'description': (
            'US Xpress is one of the largest asset-based truckload carriers in North America, '
            'offering dedicated, OTR, regional, and lease-to-own options. Strong presence in the Southeast, '
            'Midwest, and Southwest with competitive sign-on bonuses and flexible schedules.'
        ),
        'headquarters_city': 'Chattanooga',
        'headquarters_state': 'TN',
        'headquarters_zip': '37421',
        'benefit_401k': (
            '401(k) available.\n'
            'Will match up to 5%.'
        ),
        'benefit_disability_life': (
            'Benefits start after 30 days.\n'
            'See Benefit Guide in the info sheet for full details.'
        ),
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': (
            'Benefits start after 30 days.\n'
            'Medical, dental, and vision available.'
        ),
        'benefit_paid_vacation': (
            'Vacation Pay:\n'
            '- 1 week after 1 year\n'
            '- 2 weeks after 2 years\n'
            '- 3 weeks after 7 years\n'
            '- 4 weeks after 12 years\n'
            '(Note: Fleet includes Internationals, Freightliners, and Kenworths.)'
        ),
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': (
            'Weekly pay. Direct deposit.'
        ),
        'benefit_driver_ranking_bonus': (
            'Sign-On Bonus: $1000 total ($500 after the first load, $500 after 30 days) — must be active and seated at time of bonus (payout to qualify).\n'
            'US Xpress reserves the right to modify or cancel the Sign-On bonus at any time with appropriate notice under applicable law.'
        ),
        'benefit_military_program': '',
        'benefit_tuition_program': '',
        'benefit_other': (
            'Rider Policy:\n'
            '- Rider must be at least 10 years of age (if under 18, driver must have legal custody of child).\n'
            '- Riders cannot possess a valid CDL license.\n'
            '- $21.00 per month for insurance.\n'
            '- Only one rider allowed at any given time.\n'
            '- Teams may not have a rider in the truck.\n'
            '- Once a driver is solo, they may have a rider.\n'
            '- Drivers can have riders as long as the account is not local.\n\n'
            'Pet Policy:\n'
            '- $100 non-refundable maintenance fee and $10 per week charge.\n'
            '- Deducted from driver\'s check — $60 per week for 10 weeks.\n'
            '- Limited to one dog or one cat per truck (max 60 lbs).\n'
            '- Cats must be declawed.\n'
            '- Dog owners must sign paperwork; dogs showing aggression are not permitted.\n'
            '- Service animals require HR review of ADA accommodation form, medical paperwork, and health records.\n'
            '- Recruiter can provide paperwork for driver to start the process.\n\n'
            'Orientation (3 Days):\n'
            '- Starts Mondays & Wednesdays, Ends Wednesdays & Fridays.\n'
            '- Lodging: US Xpress (single occupancy rooms).\n'
            '- Meals: Breakfast (Hotel), Lunch, Dinner.\n'
            '- Travel: US Xpress or Bus.'
        ),
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'CR England',
        'website': 'https://www.crengland.com',
        'contact_email': '',
        'contact_phone': '',
        'description': (
            'CR England is one of the largest refrigerated carriers in North America. '
            'Offers OTR, dedicated, regional, and team driving positions. '
            'Known for dedicated Sysco routes and training academies.'
        ),
        'headquarters_city': 'Salt Lake City',
        'headquarters_state': 'UT',
        'headquarters_zip': '84104',
        'benefit_401k': (
            '401(k) participation available.'
        ),
        'benefit_disability_life': (
            'Life Insurance coverage available.'
        ),
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': (
            'Medical, HBA, Dental, Life Insurance, AD&D, PTO, and 40(k) available.\n'
            'Additional voluntary benefits.'
        ),
        'benefit_paid_vacation': (
            'PTO and bonus incentives available.'
        ),
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': (
            'Weekly pay. Direct deposit.'
        ),
        'benefit_driver_ranking_bonus': (
            'Performance bonus available.\n'
            'Unlimited Cash Referral Program.'
        ),
        'benefit_military_program': '',
        'benefit_tuition_program': (
            'CR England offers CDL training through their academy program.\n'
            'Tuition financing options available.'
        ),
        'benefit_other': (
            'Orientation Details:\n'
            '- 4-5 days long.\n'
            '- Monday - Thursday/Friday.\n'
            '- Paid minimum wage for the actual orientation (about 4-5 hours), not for the entire waiting period.\n\n'
            'Orientation Locations: Burns Harbor IN, Fontana CA, Dallas TX, Salt Lake City UT.\n'
            'Remote orientation for most lanes.\n'
            'Lodging Provided: Dorm style rooms.\n'
            'Travel: Bus, Plane, or Car Rental.\n'
            'Insurance starts the first of the month following 60 days of employment.\n'
            'See Benefit Information in attachments.'
        ),
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'Epes',
        'website': 'https://www.epestransport.com',
        'contact_email': '',
        'contact_phone': '',
        'description': (
            'Epes Transport System is a regional trucking company headquartered in Greensboro, NC. '
            'Specializes in local, regional, and dedicated routes primarily in the Southeast and Mid-Atlantic. '
            'Known for home daily and weekly routes for accounts like Lowes, Greif, and International Paper.'
        ),
        'headquarters_city': 'Greensboro',
        'headquarters_state': 'NC',
        'headquarters_zip': '27409',
        'benefit_401k': '',
        'benefit_disability_life': '',
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': '',
        'benefit_paid_vacation': '',
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': 'Weekly pay.',
        'benefit_driver_ranking_bonus': '',
        'benefit_military_program': '',
        'benefit_tuition_program': '',
        'benefit_other': (
            'Regional carrier based in Greensboro, NC.\n'
            'Specializes in local, regional, and dedicated routes in the Southeast and Mid-Atlantic.\n'
            'Accounts include Lowes (Adairsville local), Greif/Caraustar (Austell GA & Newark NJ), '
            'and International Paper (Lafayette LA).\n'
            'Drivers on local routes are typically home daily.\n'
            'Regional routes offer weekend home time.\n'
            'No touch and labor-intensive freight available depending on account.'
        ),
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'Knight Transportation',
        'website': 'https://www.knighttransport.com',
        'contact_email': '',
        'contact_phone': '',
        'description': (
            'Knight Transportation (a Knight-Swift company) is a major dry van truckload carrier '
            'offering OTR, regional, and dedicated positions nationwide. '
            'Part of the Knight-Swift family, one of the largest trucking companies in North America.'
        ),
        'headquarters_city': 'Phoenix',
        'headquarters_state': 'AZ',
        'headquarters_zip': '85043',
        'benefit_401k': '',
        'benefit_disability_life': '',
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': '',
        'benefit_paid_vacation': '',
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': 'Weekly pay.',
        'benefit_driver_ranking_bonus': '',
        'benefit_military_program': '',
        'benefit_tuition_program': '',
        'benefit_other': (
            'Knight Transportation is part of the Knight-Swift family of companies, '
            'one of the largest trucking conglomerates in North America.\n'
            'Offers dry van OTR, regional, and dedicated positions.\n'
            'Port services available (e.g., Long Beach, CA — home daily).\n'
            'Drivers benefit from the resources and scale of the Knight-Swift network including:\n'
            '- Swift Academy CDL training pathway for new drivers.\n'
            '- Debt-Free Tuition Program (Knight-Swift eligible employees).\n'
            '- Military Apprenticeship Program.\n'
            '- 401(k) with company match.\n'
            '- Medical, dental, and vision insurance.\n'
            '- Paid vacation based on tenure.\n'
            '- Weekly paychecks.\n'
            '- Driver Ranking Bonus program.'
        ),
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'Hogan',
        'website': 'https://www.hogantrucks.com',
        'contact_email': 'ops@hogan1.com',
        'contact_phone': '937-214-1664',
        'description': (
            'Hogan Transportation is a privately-held carrier offering dedicated, local, and regional positions. '
            'Known for the SAL Muncie account and strong driver support programs including the Hogan Learning Center.'
        ),
        'headquarters_city': 'St. Louis',
        'headquarters_state': 'MO',
        'headquarters_zip': '63101',
        'benefit_401k': (
            '401(k) available.'
        ),
        'benefit_disability_life': (
            'Health Benefits: Medical, Dental, Vision, Life Insurance.'
        ),
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': (
            'Health Benefits: Medical, Dental, Vision, Life Insurance.'
        ),
        'benefit_paid_vacation': (
            'Vacation Pay: 1/52 of Weekly Average annually.\n'
            'Holiday Pay: 8 days. Holiday Pay $80 (On Top of Pay Earned).'
        ),
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': (
            'Weekly pay.'
        ),
        'benefit_driver_ranking_bonus': (
            'Account Benefits:\n'
            '- Top 20% drivers earn W2 $70,000+\n'
            '- Home throughout the week based on load timing.\n'
            '- Drivers get an annual .01 pay increase up to $0.78 per mile.\n\n'
            'Company Benefits:\n'
            '- Top Notch Road Rescues.\n'
            '- Driver no touch.\n'
            '- Steady, non-seasonal freight.\n'
            '- Over 100 years strong.\n'
            '- Referral Program.\n'
            '- EAP – Employee Assistance Program.\n'
            '- Drivewyze toll passes.\n'
            '- Bestpass toll passes.'
        ),
        'benefit_military_program': '',
        'benefit_tuition_program': '',
        'benefit_other': (
            'Orientation:\n'
            '- Paid: Paid 8 hours at the state\'s minimum wage.\n'
            '- Normally 2 days.\n'
            '- Length: 1.5-2 weeks of training after orientation.\n'
            '- Locations: Online, St. Louis MO (Best Western), Columbus OH (Marriott Courtyard), Atlanta GA (Best Western Plus N&W), Waco TX.\n'
            '- Lodging: Mostly single occupancy; double occupancy if hotels are full.\n'
            '- Travel: Bus, Plane (for Car Hauling Accounts). Fuel reimbursement provided with valid receipts.\n'
            '- Insurance: Available after 60 days of employment. United Health Care. PTO and vacation after 1 year.\n\n'
            'Training (TN/TT):\n'
            '- TN Accepted: YES. $150/Day during training; expect 4 weeks of training (5-6 days per week). After Training will be Paid Starting Pay Rate.\n'
            '- TT Accepted: YES. $175/Day during training; expect 2 weeks of training (5-6 days per week). After Training will be Paid Starting Pay Rate.'
        ),
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'Pam Transport',
        'website': 'https://www.pamtransport.com',
        'contact_email': '',
        'contact_phone': '',
        'description': (
            'PAM Transport is a publicly-traded carrier specializing in truckload transportation. '
            'Offers OTR and dedicated routes with a tiered pay system. '
            'Known for Northeast regional operations and stable freight mix including Walmart and Sam\'s Club.'
        ),
        'headquarters_city': 'Tontitown',
        'headquarters_state': 'AR',
        'headquarters_zip': '72770',
        'benefit_401k': (
            '401(k) retirement plan that can be adjusted at any time.\n'
            'Driver may contribute up to 10% monthly. Company matches up to 3%.'
        ),
        'benefit_disability_life': (
            'Voluntary Benefits:\n'
            '- Voluntary group life insurance.\n'
            '- Voluntary AD&D.\n'
            '- Accident insurance.\n'
            '- Critical illness insurance.\n'
            '- Hospital indemnity.\n'
            '- Permanent life insurance.\n'
            '- Disability income insurance.'
        ),
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': (
            'Medical, prescription, dental, and vision benefits available with multiple coverage levels.\n\n'
            'Blue Cross Blue Shield Monthly Cost:\n'
            '- Employee: $35.00\n'
            '- Employee + Spouse: $93.00\n'
            '- Employee + Child(ren): $60.00\n'
            '- Employee + Family: $175.00\n\n'
            'Vision Insurance:\n'
            '- Employee: $1.82\n'
            '- Employee + Spouse: $3.60\n'
            '- Employee + Child(ren): $3.71\n'
            '- Employee + Family: $5.97\n\n'
            'Dental Insurance:\n'
            '- Employee: $8.25\n'
            '- Employee + Spouse: $19.00\n'
            '- Employee + Child(ren): $13.00\n'
            '- Employee + Family: $24.50\n\n'
            'Life Insurance:\n'
            '- $15 per month. Covers driver up to a $100,000 benefit.'
        ),
        'benefit_paid_vacation': (
            'Paid Time Off (PTO):\n'
            '- Drivers begin earning PTO on their first day of employment.\n'
            '- PTO accrual rate increases with tenure at PAM.'
        ),
        'benefit_prescription_drug': (
            'Prescription drug coverage included in medical plan.'
        ),
        'benefit_weekly_paycheck': (
            'Weekly pay. Direct deposit.'
        ),
        'benefit_driver_ranking_bonus': (
            'Tiered Pay System (CPM based on freight mix):\n'
            '- 0-50 miles: $40 flat rate (1% of freight mix)\n'
            '- 51-90 miles: $1.25 per mile (2% of freight mix)\n'
            '- 91-200 miles: $0.80 per mile (28% of freight mix)\n'
            '- 201+ miles: $0.65 per mile (68% of freight mix)\n\n'
            'Detention Pay: $21 per hour after the second hour.\n'
            '5-Day Monitor Pay: $175 per day.'
        ),
        'benefit_military_program': '',
        'benefit_tuition_program': '',
        'benefit_other': (
            'Insurance Starts When:\n'
            '- Company drivers become eligible the first day of the month following 60 days of service.\n'
            '- Must be actively employed on the effective date.\n'
            '- Weekly payroll deductions begin the first pay period after eligibility.\n\n'
            'Orientation:\n'
            '- $200 orientation pay, paid only if hired.\n'
            '- Company Drivers: 2.5 days.\n'
            '- Lease Purchase: 2.5 days plus an additional day for truck inspection and contracts.\n'
            '- Owner Operators: 2.5 days plus an extra day for Qualcomm installation and decals.\n'
            '- Owners must complete onboarding at a terminal, including a road test and safety training before dispatch approval.\n\n'
            'Onboarding Locations include:\n'
            'Baltimore MD, Bloomsburg PA, Cheshire CT, Pittsburgh PA, Secaucus NJ, West Deptford NJ,\n'
            'Atlanta GA, Charlotte NC, Greer SC, Jacksonville FL, Louisville KY, Nashville TN,\n'
            'Orlando FL, Raleigh NC, Ft Wayne IN, Dallas TX, Houston TX, Laredo TX, Detroit MI,\n'
            'Hammond IN, Indianapolis IN, Cleveland OH, Columbus OH, Toledo OH, St Louis MO,\n'
            'Kansas City MO, Birmingham AL, Little Rock AR, Memphis TN, Springfield MO, Tontitown AR.\n\n'
            'Travel Provided:\n'
            '- Reimbursement (preferred): 0-50 miles: $100 | 51-200 miles: $300 | 201-400 miles: $600 | 401+ miles: $800.\n'
            '- Reimbursement is paid upon first dispatch in addition to $200 onboarding pay.\n'
            '- Flights over $100 require recruiting manager approval.\n'
            '- North Little Rock onboarding requires reimbursement or flight only.'
        ),
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'TA Dedicated',
        'website': 'https://www.transportamerica.com',
        'contact_email': '',
        'contact_phone': '',
        'description': 'Transport America (TA Dedicated) is a leading truckload carrier providing dedicated and regional services across North America. Part of the TFI International family.',
        'headquarters_city': 'Eagan',
        'headquarters_state': 'MN',
        'headquarters_zip': '55121',
        'benefit_401k': '401(k) retirement plan with company match.',
        'benefit_disability_life': 'Life and disability insurance options available.',
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': 'Comprehensive health, dental, and vision insurance.',
        'benefit_paid_vacation': 'Paid vacation time based on years of service.',
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': 'Consistent weekly pay.',
        'benefit_driver_ranking_bonus': '',
        'benefit_military_program': 'Strong support for veteran drivers.',
        'benefit_tuition_program': '',
        'benefit_other': '',
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'Schneider',
        'website': 'https://www.schneider.com',
        'contact_email': '',
        'contact_phone': '',
        'description': 'Schneider National is one of the largest and oldest trucking companies in the US, known for its orange trucks and extensive logistics network.',
        'headquarters_city': 'Green Bay',
        'headquarters_state': 'WI',
        'headquarters_zip': '54303',
        'benefit_401k': '401(k) with company match.',
        'benefit_disability_life': 'Life and disability insurance.',
        'benefit_stock_purchase': 'Employee stock purchase plan.',
        'benefit_medical_dental_vision': 'Full health benefits package.',
        'benefit_paid_vacation': 'Accrued vacation time.',
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': 'Weekly pay.',
        'benefit_driver_ranking_bonus': '',
        'benefit_military_program': 'Extensive military support programs.',
        'benefit_tuition_program': 'Tuition reimbursement available.',
        'benefit_other': '',
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'Bulk Transport',
        'website': 'https://www.bulktransport.com',
        'contact_email': '',
        'contact_phone': '',
        'description': 'Bulk Transport Inc (BTI) specialized in high-quality dedicated and regional transport services, particularly for bulk materials.',
        'headquarters_city': 'Birmingham',
        'headquarters_state': 'AL',
        'headquarters_zip': '35201',
        'benefit_401k': '',
        'benefit_disability_life': '',
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': 'Comprehensive health insurance.',
        'benefit_paid_vacation': '',
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': 'Weekly pay.',
        'benefit_driver_ranking_bonus': '',
        'benefit_military_program': '',
        'benefit_tuition_program': '',
        'benefit_other': '',
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'USA Truck',
        'website': 'https://www.usa-truck.com',
        'contact_email': '',
        'contact_phone': '',
        'description': 'USA Truck (now part of DB Schenker) is a capacity solutions provider that offers dry van truckload, dedicated, and intermodal services.',
        'headquarters_city': 'Van Buren',
        'headquarters_state': 'AR',
        'headquarters_zip': '72956',
        'benefit_401k': '401(k) available.',
        'benefit_disability_life': 'Life insurance and disability coverage.',
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': 'Comprehensive health, vision, and dental.',
        'benefit_paid_vacation': 'Paid vacation time.',
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': 'Weekly pay.',
        'benefit_driver_ranking_bonus': '',
        'benefit_military_program': '',
        'benefit_tuition_program': '',
        'benefit_other': 'Orientation pay and travel provided.',
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'National Carriers',
        'website': 'https://www.nationalcarriers.com',
        'contact_email': '',
        'contact_phone': '',
        'description': 'National Carriers is a diversified motor carrier providing refrigerated and livestock transportation services.',
        'headquarters_city': 'Irving',
        'headquarters_state': 'TX',
        'headquarters_zip': '75039',
        'benefit_401k': '401(k) with match.',
        'benefit_disability_life': '',
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': 'Full health insurance package.',
        'benefit_paid_vacation': 'Paid vacation.',
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': 'Weekly pay.',
        'benefit_driver_ranking_bonus': '',
        'benefit_military_program': '',
        'benefit_tuition_program': '',
        'benefit_other': '',
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'Sharkey',
        'website': 'https://www.sharkeys.com',
        'contact_email': '',
        'contact_phone': '',
        'description': 'Sharkey Transportation is a Midwestern carrier known for its driver-friendly policies and family-oriented culture.',
        'headquarters_city': 'Quincy',
        'headquarters_state': 'IL',
        'headquarters_zip': '62301',
        'benefit_401k': '401(k) available.',
        'benefit_disability_life': '',
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': 'Premium-free family health insurance.',
        'benefit_paid_vacation': 'Paid vacation.',
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': 'Consistent weekly pay.',
        'benefit_driver_ranking_bonus': '',
        'benefit_military_program': '',
        'benefit_tuition_program': '',
        'benefit_other': '',
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'Trimac',
        'website': 'https://www.trimac.com',
        'contact_email': '',
        'contact_phone': '',
        'description': 'Trimac Transportation is a North American leader in the transport of bulk products, specializing in liquid and dry bulk chemical and petroleum products.',
        'headquarters_city': 'Houston',
        'headquarters_state': 'TX',
        'headquarters_zip': '77002',
        'benefit_401k': '401(k) with company contribution.',
        'benefit_disability_life': 'Full insurance coverage.',
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': 'Comprehensive health, dental, and vision.',
        'benefit_paid_vacation': 'Paid vacation and holidays.',
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': 'Weekly pay.',
        'benefit_driver_ranking_bonus': '',
        'benefit_military_program': '',
        'benefit_tuition_program': '',
        'benefit_other': '',
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'Nussbaum',
        'website': 'https://www.nussbaum.com',
        'contact_email': '',
        'contact_phone': '',
        'description': 'Nussbaum Transportation is an award-winning carrier based in Illinois, known for its innovation, high-quality equipment, and commitment to driver success.',
        'headquarters_city': 'Hudson',
        'headquarters_state': 'IL',
        'headquarters_zip': '61748',
        'benefit_401k': '401(k) with match.',
        'benefit_disability_life': 'Full benefits package.',
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': 'Comprehensive health insurance.',
        'benefit_paid_vacation': 'Accrued vacation time.',
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': 'Weekly pay.',
        'benefit_driver_ranking_bonus': 'Excellence program and performance bonuses.',
        'benefit_military_program': '',
        'benefit_tuition_program': '',
        'benefit_other': '',
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'Pitt Ohio',
        'website': 'https://www.pittohio.com',
        'contact_email': '',
        'contact_phone': '',
        'description': 'Pitt Ohio is a leading regional carrier in the Mid-Atlantic and Midwest, specializing in LTL, truckload, and supply chain solutions.',
        'headquarters_city': 'Pittsburgh',
        'headquarters_state': 'PA',
        'headquarters_zip': '15201',
        'benefit_401k': '401(k) available.',
        'benefit_disability_life': 'Full insurance coverage.',
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': 'Comprehensive health benefits.',
        'benefit_paid_vacation': 'Paid time off.',
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': 'Weekly pay.',
        'benefit_driver_ranking_bonus': '',
        'benefit_military_program': '',
        'benefit_tuition_program': '',
        'benefit_other': '',
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'Gateway Distribution',
        'website': 'https://www.gatewaydistribution.com',
        'contact_email': '',
        'contact_phone': '',
        'description': 'Gateway Distribution provides regional and dedicated trucking services, known for their reliable service in the Ohio Valley and Midwest.',
        'headquarters_city': 'Cincinnati',
        'headquarters_state': 'OH',
        'headquarters_zip': '45201',
        'benefit_401k': '',
        'benefit_disability_life': '',
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': 'Health insurance available.',
        'benefit_paid_vacation': '',
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': 'Weekly pay.',
        'benefit_driver_ranking_bonus': '',
        'benefit_military_program': '',
        'benefit_tuition_program': '',
        'benefit_other': '',
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'Maxim',
        'website': 'https://www.maximhealth.com',
        'contact_email': '',
        'contact_phone': '',
        'description': 'Maxim (Healthcare/Services) provides specialized transportation and staffing services, often in the medical or healthcare logistics fields.',
        'headquarters_city': 'Philadelphia',
        'headquarters_state': 'PA',
        'headquarters_zip': '19101',
        'benefit_401k': '401(k) available.',
        'benefit_disability_life': '',
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': 'Comprehensive benefits for eligible employees.',
        'benefit_paid_vacation': '',
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': 'Weekly pay.',
        'benefit_driver_ranking_bonus': '',
        'benefit_military_program': '',
        'benefit_tuition_program': '',
        'benefit_other': '',
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'Barr-Nunn',
        'website': 'https://www.barr-nunn.com',
        'contact_email': '',
        'contact_phone': '',
        'description': 'Barr-Nunn Transportation is a premier dry van carrier headquartered in Granger, IA, known for high driver pay, late-model equipment, and home time flexibility.',
        'headquarters_city': 'Granger',
        'headquarters_state': 'IA',
        'headquarters_zip': '50109',
        'benefit_401k': '401(k) with company match.',
        'benefit_disability_life': 'Life insurance and short-term disability.',
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': 'Full health, dental, and vision insurance.',
        'benefit_paid_vacation': 'Paid vacation and holidays.',
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': 'Consistent weekly pay.',
        'benefit_driver_ranking_bonus': 'Safety and performance bonuses.',
        'benefit_military_program': '',
        'benefit_tuition_program': '',
        'benefit_other': 'CSA safety bonuses and 401k match from day one.',
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
    {
        'name': 'Mast Trucking',
        'website': 'https://www.masttruckinginc.com',
        'contact_email': '',
        'contact_phone': '',
        'description': 'Mast Trucking is a family-owned carrier based in Ohio, offering OTR and regional refrigerated services with a focus on driver safety and quality equipment.',
        'headquarters_city': 'Millersburg',
        'headquarters_state': 'OH',
        'headquarters_zip': '44663',
        'benefit_401k': '401(k) plan with employer matching contributions.',
        'benefit_disability_life': 'Vision & Dental insurance available after 90 days.',
        'benefit_stock_purchase': '',
        'benefit_medical_dental_vision': 'Medical, dental, and vision eligibility after 90 days. Comprehensive medical coverage through the company provider.',
        'benefit_paid_vacation': 'Paid vacation available after 1 year of continuous employment.',
        'benefit_prescription_drug': '',
        'benefit_weekly_paycheck': 'Weekly pay.',
        'benefit_driver_ranking_bonus': 'Performance pay and incentives based on scorecard results.',
        'benefit_military_program': '',
        'benefit_tuition_program': 'Training programs (Mast 1.0 and 2.0) available for new drivers.',
        'benefit_other': 'Passenger policy after 1 year of employment. Performance bonus up to $150 every 4 weeks.',
        'presentation': '',
        'pre_qualifications': '',
        'app_process': '',
    },
]

created = 0
updated = 0

for data in carriers:
    obj, is_new = Carrier.objects.update_or_create(
        name=data['name'],
        defaults={k: v for k, v in data.items() if k != 'name'}
    )
    if is_new:
        created += 1
        print(f"  ✅ Created: {obj.name}")
    else:
        updated += 1
        print(f"  ♻️  Updated: {obj.name}")

print(f"\nDone! {created} created, {updated} updated.")
print(f"Total carriers in DB: {Carrier.objects.count()}")
print("\n⚠️  Remember to fill in 'presentation', 'pre_qualifications', and 'app_process' in the admin panel.")
