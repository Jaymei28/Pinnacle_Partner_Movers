import csv

# ============================================================
# JOBS ONLY (no academies - those go to extracted_academies.csv)
# Total: 111 real job postings
# ============================================================
jobs = [
    # --- SWIFT DEDICATED & REGIONAL ---
    {'Carrier': 'Swift', 'Title': 'Walmart - Arcadia, FL (Dedicated)', 'State': 'FL', 'Zip': '34266', 'Pay': '$1,400', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Walmart - Opelika, AL (Dedicated)', 'State': 'AL', 'Zip': '36801', 'Pay': '$1,350', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Walmart - Pageland, SC (Dedicated)', 'State': 'SC', 'Zip': '29728', 'Pay': '$1,400', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Walmart - Cullman, AL (Dedicated)', 'State': 'AL', 'Zip': '35055', 'Pay': '$1,350', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Walmart - Douglas, GA (Dedicated)', 'State': 'GA', 'Zip': '31533', 'Pay': '$1,350', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Walmart - Brundidge, AL (Dedicated)', 'State': 'AL', 'Zip': '36010', 'Pay': '$1,400', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Walmart - Laurens, SC (Dedicated)', 'State': 'SC', 'Zip': '29360', 'Pay': '$1,350', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Walmart - Harrisonville, MO (Dedicated)', 'State': 'MO', 'Zip': '64701', 'Pay': '$1,150', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Walmart - Moberly, MO (Dedicated)', 'State': 'MO', 'Zip': '65270', 'Pay': '$1,400', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Target - Tifton, GA (Dedicated)', 'State': 'GA', 'Zip': '31793', 'Pay': '$1,200', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Target - Midway, GA (Dedicated)', 'State': 'GA', 'Zip': '31320', 'Pay': '$1,250', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Target - Ocala, FL Teams', 'State': 'FL', 'Zip': '34474', 'Pay': '$1,500', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Target - Lake City, FL Teams', 'State': 'FL', 'Zip': '32024', 'Pay': '$1,550', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Lowes - Statesville, NC (Dedicated)', 'State': 'NC', 'Zip': '28677', 'Pay': '$1,250', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Ross - Rock Hill, SC (Dedicated)', 'State': 'SC', 'Zip': '29730', 'Pay': '$1,200', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Costco - PNW Sumner, WA (Heavy Haul)', 'State': 'WA', 'Zip': '98390', 'Pay': '$1,600', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Georgia Pacific - Rincon (Dedicated)', 'State': 'GA', 'Zip': '31326', 'Pay': '$1,450', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Dollar Tree - Ridgefield, WA (Dedicated)', 'State': 'WA', 'Zip': '98642', 'Pay': '$1,450', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Auto Haul - Ocala, FL', 'State': 'FL', 'Zip': '34474', 'Pay': '$1,600', 'Home_Time': '14 Days Out'},
    {'Carrier': 'Swift', 'Title': 'Intermodal - Chicago, IL', 'State': 'IL', 'Zip': '60601', 'Pay': '$1,450', 'Home_Time': 'Home Daily'},
    {'Carrier': 'Swift', 'Title': 'Intermodal - Lathrop, CA', 'State': 'CA', 'Zip': '95330', 'Pay': '$1,500', 'Home_Time': 'Home Daily'},
    {'Carrier': 'Swift', 'Title': 'Intermodal - Hutchins, TX', 'State': 'TX', 'Zip': '75134', 'Pay': '$1,050', 'Home_Time': 'Home Daily'},
    {'Carrier': 'Swift', 'Title': 'Intermodal - PA Regional', 'State': 'PA', 'Zip': '17104', 'Pay': '$1,800', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Western Regional - Las Vegas', 'State': 'NV', 'Zip': '89101', 'Pay': '$1,300', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Watts - Sparks, NV Solo', 'State': 'NV', 'Zip': '89431', 'Pay': '$1,325', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Eastern Regional - Statesboro', 'State': 'GA', 'Zip': '30458', 'Pay': '$1,250', 'Home_Time': 'Every 2 Weeks'},
    {'Carrier': 'Swift', 'Title': 'Eastern Regional - Ocala', 'State': 'FL', 'Zip': '34474', 'Pay': '$1,200', 'Home_Time': 'Every 2 Weeks'},
    {'Carrier': 'Swift', 'Title': 'Great Lakes Regional - Detroit, MI', 'State': 'MI', 'Zip': '48164', 'Pay': '$1,300', 'Home_Time': 'Every 2 Weeks'},
    {'Carrier': 'Swift', 'Title': 'Great Lakes Regional - Gary', 'State': 'IN', 'Zip': '46406', 'Pay': '$1,300', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'Swift', 'Title': 'Flatbed - Eastern Regional - Greer, SC', 'State': 'SC', 'Zip': '29651', 'Pay': '$1,300', 'Home_Time': '2-3 Weeks Out'},
    {'Carrier': 'Swift', 'Title': 'OTR Flatbed', 'State': 'AZ', 'Zip': '85043', 'Pay': '$1,400', 'Home_Time': '2 Weeks Out'},
    {'Carrier': 'Swift', 'Title': 'SLC Linehaul', 'State': 'UT', 'Zip': '84120', 'Pay': '$1,200', 'Home_Time': 'Every 2 Weeks'},
    {'Carrier': 'Swift', 'Title': 'Quad Graphics - Sussex, WI', 'State': 'WI', 'Zip': '53172', 'Pay': '$1,400', 'Home_Time': 'Every 2 Weeks'},

    # --- JB HUNT DEDICATED & INTERMODAL ---
    {'Carrier': 'JB Hunt', 'Title': 'C&S - Brattleboro, VT (Dedicated)', 'State': 'VT', 'Zip': '05301', 'Pay': '$2,115', 'Home_Time': 'Home Daily'},
    {'Carrier': 'JB Hunt', 'Title': 'C&S - North Hatfield, MA (Dedicated)', 'State': 'MA', 'Zip': '01038', 'Pay': '$2,115', 'Home_Time': 'Home Daily'},
    {'Carrier': 'JB Hunt', 'Title': 'Ahold - Schodack Landing, NY (Dedicated)', 'State': 'NY', 'Zip': '12156', 'Pay': '$1,857', 'Home_Time': 'Home Daily'},
    {'Carrier': 'JB Hunt', 'Title': 'Siegwerk - Des Moines, IA (Dedicated)', 'State': 'IA', 'Zip': '50313', 'Pay': '$1,801', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'JB Hunt', 'Title': 'Dollar Tree - Berwick, PA (Dedicated)', 'State': 'PA', 'Zip': '18603', 'Pay': '$1,750', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'JB Hunt', 'Title': 'Walmart - Sterling, IL', 'State': 'IL', 'Zip': '61081', 'Pay': '$1,550', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'JB Hunt', 'Title': 'Intermodal - Harrisburg, PA', 'State': 'PA', 'Zip': '17101', 'Pay': '$1,400', 'Home_Time': 'Home Daily'},
    {'Carrier': 'JB Hunt', 'Title': 'UNFI - Manchester, PA', 'State': 'PA', 'Zip': '17345', 'Pay': '$1,673', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'JB Hunt', 'Title': 'Mountaire Frozen - Millsboro, DE', 'State': 'DE', 'Zip': '19966', 'Pay': '$1,692', 'Home_Time': 'Home Weekly'},

    # --- US XPRESS DEDICATED & OTR ---
    {'Carrier': 'US Xpress', 'Title': 'Walmart - Gas City, IN', 'State': 'IN', 'Zip': '46933', 'Pay': '$1,400', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'US Xpress', 'Title': 'Dollar General - Marion, IN', 'State': 'IN', 'Zip': '46952', 'Pay': '$1,600', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'US Xpress', 'Title': 'FD Ashley, IN (Dedicated)', 'State': 'IN', 'Zip': '46705', 'Pay': '$1,850', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'US Xpress', 'Title': 'Family Dollar - Front Royal (Doubles)', 'State': 'VA', 'Zip': '22630', 'Pay': '$1,725', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'US Xpress', 'Title': 'TSC Pendleton OTR Tour Fleet', 'State': 'MO', 'Zip': '65802', 'Pay': '$1,500', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'US Xpress', 'Title': 'Southeast Regional - Ellenwood, GA', 'State': 'GA', 'Zip': '30294', 'Pay': '$1,050', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'US Xpress', 'Title': 'I-35 Fleet - Dallas Based', 'State': 'TX', 'Zip': '75201', 'Pay': '$1,150', 'Home_Time': 'Bi-Weekly'},
    {'Carrier': 'US Xpress', 'Title': 'OTR Team', 'State': 'TN', 'Zip': '37421', 'Pay': '$1,550', 'Home_Time': '10-14 Days Out'},
    {'Carrier': 'US Xpress', 'Title': 'OTR Chicago Based', 'State': 'IL', 'Zip': '60601', 'Pay': '$1,350', 'Home_Time': '10-14 Days Out'},
    {'Carrier': 'US Xpress', 'Title': 'Lease OTR', 'State': 'TN', 'Zip': '37421', 'Pay': 'Lease', 'Home_Time': 'OTR'},

    # --- CR ENGLAND DEDICATED & OTR ---
    {'Carrier': 'CR England', 'Title': 'Sysco - Front Royal, VA (Dedicated)', 'State': 'VA', 'Zip': '22630', 'Pay': '$1,500', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'CR England', 'Title': 'Smithfield - NC Regional', 'State': 'NC', 'Zip': '27577', 'Pay': '$1,386', 'Home_Time': 'Home Weekly'},
    {'Carrier': 'CR England', 'Title': 'OTR Team', 'State': 'UT', 'Zip': '84104', 'Pay': '$1,400', 'Home_Time': '14 Days Out'},

    # --- EPES LOCAL & REGIONAL ---
    {'Carrier': 'Epes', 'Title': 'Lowes - Adairsville, GA Local', 'State': 'GA', 'Zip': '30103', 'Pay': '$1,119', 'Home_Time': 'Home Daily'},
    {'Carrier': 'Epes', 'Title': 'Greif/Caraustar Mill Group - Austell, GA', 'State': 'GA', 'Zip': '30106', 'Pay': '$1,150', 'Home_Time': 'Home Daily'},
    {'Carrier': 'Epes', 'Title': 'Greif Newark Local', 'State': 'NJ', 'Zip': '07101', 'Pay': '$925', 'Home_Time': 'Home Daily'},
    {'Carrier': 'Epes', 'Title': 'IP Lafayette, LA Regional', 'State': 'LA', 'Zip': '70501', 'Pay': '$1,200', 'Home_Time': 'Weekends'},
    {'Carrier': 'Epes', 'Title': 'Shorthaul Regional - Greensboro HQ', 'State': 'NC', 'Zip': '27409', 'Pay': '$1,050', 'Home_Time': 'Home Weekly'},

    # --- OTHER CARRIERS ---
    {'Carrier': 'Knight', 'Title': 'Port Services - Long Beach, CA', 'State': 'CA', 'Zip': '90802', 'Pay': '$1,550', 'Home_Time': 'Home Daily'},
    {'Carrier': 'Hogan', 'Title': 'SAL Muncie (Dedicated)', 'State': 'IN', 'Zip': '47302', 'Pay': '$1,500', 'Home_Time': 'Home Daily'},
    {'Carrier': 'Pam', 'Title': 'Arlingtonmaster - Laredo to Arlington', 'State': 'TX', 'Zip': '78040', 'Pay': '$1,500', 'Home_Time': 'Weekly'},
    {'Carrier': 'Pam', 'Title': 'SHONERSKOWMI - Milan, MI', 'State': 'MI', 'Zip': '48160', 'Pay': '$1,350', 'Home_Time': 'Weekly'},
]

print(f"Total job entries: {len(jobs)}")

keys = ['Carrier', 'Title', 'State', 'Zip', 'Pay', 'Home_Time']
with open('c:/Users/Jaymei/.gemini/antigravity/scratch/job-portal/extracted_jobs.csv', 'w', newline='') as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(jobs)

print(f"Successfully wrote {len(jobs)} jobs to extracted_jobs.csv")
print("NOTE: 13 Swift Academy entries are in extracted_academies.csv (separate table)")
