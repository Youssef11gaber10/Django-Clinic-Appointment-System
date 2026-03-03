from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import UserApp, PatientProfile, DoctorProfile
from appointments.models import Appointment
from medical.models import Consultation, PrescriptoinItem, RequestedTest
from scheduling.models import Slot, Availability, DoctorException


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting group and permission setup...'))

        patient_group, _ = Group.objects.get_or_create(name='Patient')
        doctor_group, _ = Group.objects.get_or_create(name='Doctor')
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        receptionist_group, _ = Group.objects.get_or_create(name='Receptionist')

        self.stdout.write(self.style.SUCCESS('Done creating groups.'))

        patient_group.permissions.clear()
        doctor_group.permissions.clear()
        admin_group.permissions.clear()
        receptionist_group.permissions.clear()

        patient_permissions = [
            # View own appointments
            ('view_appointment', Appointment),
            # View own consultations
            ('view_consultation', Consultation),
            # View own test requests
            ('view_requestedtest', RequestedTest),
            # View own prescriptions
            ('view_prescriptoinitem', PrescriptoinItem),
            # View own profile
            ('view_userapp', UserApp),
            ('change_userapp', UserApp),
        ]
        for perm_codename, model in patient_permissions:
            try:
                content_type = ContentType.objects.get_for_model(model)
                perm = Permission.objects.get(content_type=content_type, codename=perm_codename)
                patient_group.permissions.add(perm)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f'Permission {perm_codename} for {model.__name__} not found'
                    )
                )
        self.stdout.write(self.style.SUCCESS('Patient permissions assigned'))

        doctor_permissions = [
            # Manage own availability
            ('add_availability', Availability),
            ('change_availability', Availability),
            ('delete_availability', Availability),
            ('view_availability', Availability),
            # Manage own slots
            ('add_slot', Slot),
            ('change_slot', Slot),
            ('delete_slot', Slot),
            ('view_slot', Slot),
            # View and manage own appointments
            ('view_appointment', Appointment),
            ('change_appointment', Appointment),
            # Create and manage consultations
            ('add_consultation', Consultation),
            ('change_consultation', Consultation),
            ('view_consultation', Consultation),
            # Create and manage prescriptions
            ('add_prescriptoinitem', PrescriptoinItem),
            ('change_prescriptoinitem', PrescriptoinItem),
            ('view_prescriptoinitem', PrescriptoinItem),
            # Request tests
            ('add_requestedtest', RequestedTest),
            ('view_requestedtest', RequestedTest),
            # View own profile
            ('view_userapp', UserApp),
            ('change_userapp', UserApp),
            ('view_doctorprofile', DoctorProfile),
            ('change_doctorprofile', DoctorProfile),
        ]
        for perm_codename, model in doctor_permissions:
            try:
                content_type = ContentType.objects.get_for_model(model)
                perm = Permission.objects.get(content_type=content_type, codename=perm_codename)
                doctor_group.permissions.add(perm)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f'Permission {perm_codename} for {model.__name__} not found'
                    )
                )
        self.stdout.write(self.style.SUCCESS('Doctor permissions assigned'))

        receptionist_permissions = [
            # View all users
            ('view_userapp', UserApp),
            # View all appointments
            ('view_appointment', Appointment),
            ('change_appointment', Appointment),
            # View slots
            ('view_slot', Slot),
            # View consultations (read-only)
            ('view_consultation', Consultation),
        ]

        for perm_codename, model in receptionist_permissions:
            try:
                content_type = ContentType.objects.get_for_model(model)
                perm = Permission.objects.get(content_type=content_type, codename=perm_codename)
                receptionist_group.permissions.add(perm)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f'Permission {perm_codename} for {model.__name__} not found'
                    )
                )
        self.stdout.write(self.style.SUCCESS('Receptionist permissions assigned'))

        all_permissions = Permission.objects.all()
        admin_group.permissions.set(all_permissions)
        self.stdout.write(self.style.SUCCESS('Admin permissions assigned (all permissions)'))

        self.assign_users_to_groups() #assign existing users to groups based on their role

        self.stdout.write(
            self.style.SUCCESS('Setup complete! All groups and permissions configured.')
        )

    def assign_users_to_groups(self):
        patients = UserApp.objects.filter(role='patient')
        doctors = UserApp.objects.filter(role='doctor')
        admins = UserApp.objects.filter(role='admin')
        receptionists = UserApp.objects.filter(role='receptionist')

        patient_group = Group.objects.get(name='Patient')
        doctor_group = Group.objects.get(name='Doctor')
        admin_group = Group.objects.get(name='Admin')
        receptionist_group = Group.objects.get(name='Receptionist')

        for user in patients:
            user.groups.add(patient_group)
        self.stdout.write(self.style.SUCCESS(f'Assigned {patients.count()} patients to Patient group'))

        for user in doctors:
            user.groups.add(doctor_group)
        self.stdout.write(self.style.SUCCESS(f'Assigned {doctors.count()} doctors to Doctor group'))
        for user in admins:
            user.groups.add(admin_group)
        self.stdout.write(self.style.SUCCESS(f'Assigned {admins.count()} admins to Admin group'))

        for user in receptionists:
            user.groups.add(receptionist_group)
        self.stdout.write(self.style.SUCCESS(f'Assigned {receptionists.count()} receptionists to Receptionist group'))