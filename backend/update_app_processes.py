import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobstream_backend.settings')
django.setup()

from jobs.models import Carrier

app_processes = {
    'CR England': """CR England Application Process

Step 1: Recruiter Completes the Application for the Driver
Link: https://intelliapp.driverapponline.com/c/crengland?r=ClassARecruiting&release_signature_screen_submit_without_signing=y
- How did you hear about us: Select "OTHER"
- If "Other", please explain: Enter "CLASS A"

Step 2: Send the Driver the link below to sign the releases
Link: https://intelliapp.driverapponline.com/s/crengland?r=ClassARec

Step 3: Enter Driver into Driver Management and list in "Carrier Notes":
- Driver's Email Address
- Position the Driver was sold on
- Follow Up

IMPORTANT: As soon as the app is complete, have the Driver call Laurie Larsen at 385-313-3126. Driver should leave a message if she's busy.

Weekend Emergency: DRIVER call main recruiting line 800-421-9004 x 93111.
Recruiter Info: Turnaround 24-48 hrs. Hours: 6AM-4PM MST M-F.
Rehire: All applicants considered upon review.
Website: https://www.crengland.com""",

    'Hogan': """Hogan Application Process

Step 1: Recruiter completes application
Link: https://intelliapp.driverapponline.com/c/hogantransport?r=ClassARecruiting-21&release_signature_screen_submit_without_signing=y

Step 2: Enter Driver into Driver Management and list in "Carrier Notes":
- Position applying for
- Potential Start Date
- Recruiter's Email Address
- Upload CDL (Front/Back), Med Card, and ID (Passport/Birth Cert/SS) or via Driver Pulse.
- Forward to Kissa: kkimble@classarecruitinginc.com

Follow Up: Once signed, Kissa calls driver to recap. Hogan on-boarder (Brittany/Kelly/Amanda) calls within 1-2 days.
Approved: Driver MUST sign conditional offer asap. Hogan sets up orientation.
Recruiter Contact: Kissa Kimble (479) 408-2705.
Ownership: 30-day non-recruitment rule.
Website: https://www.hogan1.com/""",

    'Pam Transport': """Pam Application Process

Step 1: Recruiter completes app
- Company Drivers: https://intelliapp.driverapponline.com/c/pamtransport?r=ClassA&cq_315614=Barbara%20Chambers&release_signature_screen_submit_without_signing=y
- O/O & Lease: https://intelliapp.driverapponline.com/c/pamcartagecarrier?r=ClassA&cq_1097086=Barbara%20Chambers&release_signature_screen_submit_without_signing=y
- 10-year work history required.

Step 2: Enter driver into Driver Management and list in "Carrier Notes":
- Driver's email
- Run applied for

Step 3: Pam sends releases to driver's email.
- Give driver Barbara Chambers' number: 479-422-6728.

Follow Up: Barbara reaches out once releases signed. Update via Jessica after 24 hrs.
Approved: Drug test and physical scheduled. Barbara schedules orientation.""",

    'Swift Transportation': """Swift Application Process

Step 1: Recruiter completes partial app
Link: https://intelliapp2.driverapponline.com/c/swiftcompthird
- Select "Matt Hutto" as recruiter. Need proof of self-employment (Uber/Lyft).

Step 2: Send driver link to finish app
Link: https://intelliapp2.driverapponline.com/c/swiftcomp?r=classa
- Select "Matt Hutto" as recruiter.

Step 3: Enter in Driver Management with details:
- Home time, Schedule, Account, Pay, App confirmation #, Driver's SSN.
- Send docs (CDL, certs) directly to Swift admin or Matt Hutto.

Follow Up: Admin (David L, Joey, Devan, etc.) will request RC and full app.
Approved: Tuesdays/Fridays for orientation confirmation.
Glossary: ALS (App Link Sent), DQP (Orientation), RC (Recruiter Change).""",

    'US Xpress': """US Xpress Application Process

Step 1: US Xpress App Link
Link: https://intelliapp2.driverapponline.com/c/usxpress?r=ClassARec&release_signature_screen_submit_without_signing=yn_submit_without_signing=y
- 10-year work history required. Leave "working with recruiter" blank.

Step 2: Enter in Driver Management:
- Run, Pay, Home time, Orientation date.

Follow Up: USX recruiter texts within 24 hrs. Processor assigned in daily/afternoon updates.
Orientation Confirmation Line: 800-900-9318 ext. 7914.
Security Interview: 623-907-7910.
Driver Placement: 877-510-3171.
Approved: Processor schedules orientation/travel/hotel.""",

    'Barr-Nunn': """Barr-Nunn Application Process

Step 1: Recruiter completes app
Link: https://intelliapp2.driverapponline.com/c/barrnunntrans?r=CLASSARECRUITING.COM&release_signature_screen_submit_without_signing=y
- How heard about us: Select "C.A.R." Do NOT enter recruiter name on app.

Step 2: List in "Carrier Notes":
- Target run, Experience details.

Step 3: Send release link to driver
Link: https://intelliapp2.driverapponline.com/s/barrnunntrans?r=CLASSARECRUITING.COM

Step 4: Driver contacted within 24 hrs. If not, call 888-999-7576.
Approved: Physical/drug screen required before scheduling orientation.
Weekend Emergency: Call 515-999-2525.
Website: https://barr-nunntruckingjobs.com/""",

    'Bulk Transport': """Bulk Transport Application Process

Step 1: Recruiter completes app
- Bulk Accounts: https://intelliapp.driverapponline.com/c/schilli?r=Marta&release_signature_screen_submit_without_signing=y
- Sugar Beets: https://intelliapp.driverapponline.com/c/btcwest?r=classadriverssugarbeetdrivers&release_signature_screen_submit_without_signing=y
- Bulk sends releases to driver.

Step 2: Enter in Driver Management:
- Position applied for.

Follow Up: Bulk reaches out within 24 hrs.
Approved: Bulk reaches out to schedule orientation/travel/hotel.""",

    'Gateway Distribution': """Gateway Distribution Application Process

Step 1: Driver completes app
Link: https://intelliapp.driverapponline.com/c/gateway?uri_b=ia_gateway_1479635757
- Signs releases at the end.

Step 2: Enter in Driver Management:
- Driver's city/state, Teammate's name and city/state.

Follow Up: Gateway reaches out within 24 hrs.
Approved: Gateway continues communication for orientation.
Contact: Jessica Silver. Rehire: 1 yr separation. Ownership: 30 days.
Website: https://www.gatewaydistribution.net/""",

    'National Carriers': """National Application Process (No female trainees)

Step 1: https://intelliapp.driverapponline.com/c/classarecruiting?r=National Carriers
- Include 10-year work history.

Step 2: Enter in Driver Management:
- Run applied for. DO NOT enter SSN in notes.

Step 3: Jessica reviews for completeness/qualifications.
Step 4: Jessica transfers app to NCI once 100% complete.

Follow Up: NCI reaches out within 24-48 hrs. Updates every Wednesday.
NCI Contact: (FOR DRIVER ONLY) Carson Wheat 469-586-2525 / Dena Moore 469-586-2596.
Approved: NCI contacts recruiter/driver to schedule orientation.""",

    'Sharkey': """Sharkey Application Process (Not hiring from OK, KY, WI, MI, MN, TN)

Step 1: Recruiter completes app
Link: https://intelliapp2.driverapponline.com/c/sharkey?r=classarec&release_signature_screen_submit_without_signing=y
- 10-year work history required.

Step 2: Driver signs link: https://intelliapp2.driverapponline.com/s/sharkey

Step 3: Enter in Driver Management:
- Pay program, Home time, Insurance opt-out status.

Follow Up: Email Jessica after 48 hrs if no contact.
Approved: Chris reaches out for orientation/travel/lodging.""",

    'TA Dedicated': """TA Dedicated Application Process (No trainees)

Step 1: Recruiter completes app
Link: https://intelliapp.driverapponline.com/c/classarecruiting?r=TADedicated
- Full 10-year work history required.

Step 2: Enter in Driver Management:
- Run, Zip code, Endorsements status.
- Must have 2 personal references. Releases emailed within 1 hr of speaking.

Step 3: Obtain 4-page long form physical and med card (picture perfect).
- Notify driver of urine and hair drug test. Physical within 24 hrs of scheduling.

Contact: Erin Schurman: 651-364-9574.
Approved: Erin schedules orientation. Strong confirmation required Friday prior.""",

    'USA Truck': """USA Truck Application Process

Step 1: Recruiter completes app
Link: https://intelliapp.driverapponline.com/c/classarecruiting?r=DBSchenker
- 10-year work history required.

Step 2: Enter in Driver Management:
- City/State, Run, Pay quoted, Experience, Orientation date preference.

Step 3: Jessica transfers app to USA Truck.
Follow Up: Give driver Brandie's # (479-471-3863). She calls within 24 hrs to review and send releases.
Pre-approved: Interview with Ops Manager for final decision.
Approved: Brandie schedules orientation/travel/hotel. (No candidates from NYC/Philly).""",
}

updated_count = 0
for name, process in app_processes.items():
    try:
        carrier = Carrier.objects.get(name=name)
        carrier.app_process = process
        carrier.save()
        updated_count += 1
        print(f"✅ Updated app_process for {name}")
    except Carrier.DoesNotExist:
        print(f"❌ Carrier '{name}' not found in database.")

print(f"\nDone! Updated {updated_count} carriers.")
