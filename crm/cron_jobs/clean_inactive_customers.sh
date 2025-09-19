#!/bin/bash
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

OUTPUT=$(python manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer
count=Customer.objects.filter(order__isnull=True).count()
Customer.objects.filter(order__isnull=True).delete()
print(f'Deleted {count} customers without orders in 365+ days . ')
)

echo "$TIMESTAMP - $OUTPUT" >> /tmp/customer_cleanup_log.txt