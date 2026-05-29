from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from clients.models  import Client
from projects.models import Project
from invoices.models import Invoice
from timelogs.models import TimeLog
from datetime import date, timedelta
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # User
        user, created = User.objects.get_or_create(username='user1')
        if created:
            user.set_password('user123')
            user.save()

        # Clients
        c1, _ = Client.objects.get_or_create(user=user, email='maria@santosrealty.com',
            defaults={'name':'Maria Santos','company':'Santos Realty Group','phone':'09171234567'})
        c2, _ = Client.objects.get_or_create(user=user, email='jose@reyestech.ph',
            defaults={'name':'Jose Reyes','company':'Reyes Tech Solutions','phone':'09281234567'})
        c3, _ = Client.objects.get_or_create(user=user, email='ana@cruzfashion.com',
            defaults={'name':'Ana Cruz','company':'Cruz Fashion House','phone':'09391234567'})
        c4, _ = Client.objects.get_or_create(user=user, email='carlo@mendezfoods.com',
            defaults={'name':'Carlo Mendez','company':'Mendez Food Corp','phone':'09451234567'})

        # Projects
        today = date.today()
        p1, _ = Project.objects.get_or_create(client=c1, title='Real Estate Website Redesign',
            defaults={'description':'Full redesign with property listings.','status':'done',
                      'budget':Decimal('35000.00'),'deadline':today - timedelta(days=10)})
        p2, _ = Project.objects.get_or_create(client=c2, title='Company CRM System',
            defaults={'description':'Custom CRM for managing leads and clients.','status':'active',
                      'budget':Decimal('85000.00'),'deadline':today + timedelta(days=45)})
        p3, _ = Project.objects.get_or_create(client=c3, title='Online Fashion Store',
            defaults={'description':'E-commerce with product catalog and checkout.','status':'active',
                      'budget':Decimal('50000.00'),'deadline':today + timedelta(days=30)})
        p4, _ = Project.objects.get_or_create(client=c4, title='Food Delivery Mobile UI',
            defaults={'description':'UI/UX design for food delivery app.','status':'paused',
                      'budget':Decimal('25000.00'),'deadline':today + timedelta(days=60)})
        p5, _ = Project.objects.get_or_create(client=c1, title='Social Media Management',
            defaults={'description':'Monthly social media content.','status':'active',
                      'budget':Decimal('15000.00'),'deadline':today + timedelta(days=15)})

        # Invoices
        Invoice.objects.get_or_create(invoice_no='INV-001',
            defaults={'project':p1,'amount':Decimal('35000.00'),'status':'paid','due_date':today - timedelta(days=5)})
        Invoice.objects.get_or_create(invoice_no='INV-002',
            defaults={'project':p2,'amount':Decimal('42500.00'),'status':'paid','due_date':today - timedelta(days=15)})
        Invoice.objects.get_or_create(invoice_no='INV-003',
            defaults={'project':p2,'amount':Decimal('42500.00'),'status':'sent','due_date':today + timedelta(days=7)})
        Invoice.objects.get_or_create(invoice_no='INV-004',
            defaults={'project':p3,'amount':Decimal('25000.00'),'status':'sent','due_date':today + timedelta(days=14)})
        Invoice.objects.get_or_create(invoice_no='INV-005',
            defaults={'project':p5,'amount':Decimal('15000.00'),'status':'draft','due_date':today + timedelta(days=10)})
        Invoice.objects.get_or_create(invoice_no='INV-006',
            defaults={'project':p4,'amount':Decimal('12500.00'),'status':'draft','due_date':today + timedelta(days=20)})

        # Time Logs
        logs = [
            (p1,'Initial wireframes and mockups',     Decimal('4.0'), today-timedelta(days=20)),
            (p1,'Frontend HTML/CSS development',      Decimal('6.5'), today-timedelta(days=18)),
            (p1,'Backend API integration',            Decimal('5.0'), today-timedelta(days=15)),
            (p1,'Testing and bug fixes',              Decimal('3.0'), today-timedelta(days=12)),
            (p2,'Database schema design',             Decimal('3.5'), today-timedelta(days=10)),
            (p2,'User authentication module',         Decimal('5.0'), today-timedelta(days=8)),
            (p2,'Dashboard and analytics',            Decimal('4.5'), today-timedelta(days=5)),
            (p2,'Client management CRUD',             Decimal('6.0'), today-timedelta(days=3)),
            (p3,'Product catalog design',             Decimal('4.0'), today-timedelta(days=7)),
            (p3,'Shopping cart implementation',       Decimal('5.5'), today-timedelta(days=4)),
            (p5,'Content calendar planning',          Decimal('2.0'), today-timedelta(days=2)),
            (p5,'Designed 10 social media posts',     Decimal('3.5'), today-timedelta(days=1)),
        ]
        for project, desc, hours, log_date in logs:
            TimeLog.objects.get_or_create(
                project=project, description=desc, date=log_date,
                defaults={'hours': hours})

        # Summary
        self.stdout.write(self.style.SUCCESS('\n✅ Seeding complete!'))
        self.stdout.write(f'   Clients:  {Client.objects.filter(user=user).count()}')
        self.stdout.write(f'   Projects: {Project.objects.filter(client__user=user).count()}')
        self.stdout.write(f'   Invoices: {Invoice.objects.filter(project__client__user=user).count()}')
        self.stdout.write(f'   TimeLogs: {TimeLog.objects.filter(project__client__user=user).count()}')
        self.stdout.write('\n   Login → user1 / user123')