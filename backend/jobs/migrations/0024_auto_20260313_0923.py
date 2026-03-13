from django.db import migrations

def merge_carriers(apps, schema_editor):
    Carrier = apps.get_model('jobs', 'Carrier')
    Job = apps.get_model('jobs', 'Job')
    Academy = apps.get_model('jobs', 'Academy')
    
    # Pairs of (Duplicate Name, Master Name)
    merges = [
        ("National", "National Carriers"),
        ("Pam", "PAM Transport"),
        ("P&S", "P&S Transportation"),
    ]
    
    for duplicate_name, master_name in merges:
        try:
            duplicate = Carrier.objects.get(name=duplicate_name)
            master = Carrier.objects.get(name=master_name)
            
            # 1. Move all jobs to the master carrier
            Job.objects.filter(carrier=duplicate).update(carrier=master)
            
            # 2. Move all academies to the master carrier
            Academy.objects.filter(carrier=duplicate).update(carrier=master)
            
            # 3. If master has empty fields, copy helpful data from duplicate
            fields_to_check = [
                'logo', 'description', 'website', 'contact_email', 'contact_phone',
                'benefit_401k', 'benefit_disability_life', 'benefit_stock_purchase',
                'benefit_medical_dental_vision', 'benefit_paid_vacation',
                'benefit_prescription_drug', 'benefit_weekly_paycheck',
                'benefit_driver_ranking_bonus', 'benefit_military_program',
                'benefit_tuition_program', 'benefit_other', 'benefits',
                'presentation', 'pre_qualifications', 'app_process',
                'headquarters_zip', 'headquarters_city', 'headquarters_state'
            ]
            
            updated = False
            for field in fields_to_check:
                val = getattr(duplicate, field)
                if val and not getattr(master, field):
                    setattr(master, field, val)
                    updated = True
            
            if updated:
                master.save()
                
            # 4. Delete the duplicate carrier record
            duplicate.delete()
            print(f"Successfully merged '{duplicate_name}' into '{master_name}'")
            
        except Carrier.DoesNotExist:
            continue
        except Exception as e:
            print(f"Error merging '{duplicate_name}': {e}")

    # 5. Additional cleanup for stray or whitespace-only names
    try:
        unknown_carrier, _ = Carrier.objects.get_or_create(name="Unknown Carrier")
        for c in Carrier.objects.all():
            name_strip = c.name.strip()
            if not name_strip or name_strip in [".", "Carrier"]:
                if c.id != unknown_carrier.id:
                    Job.objects.filter(carrier=c).update(carrier=unknown_carrier)
                    Academy.objects.filter(carrier=c).update(carrier=unknown_carrier)
                    c.delete()
                    print(f"Cleaned up stray carrier: '{c.name}'")
    except Exception as e:
        print(f"Error during stray cleanup: {e}")

class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0023_carrier_benefits'),
    ]

    operations = [
        migrations.RunPython(merge_carriers),
    ]
