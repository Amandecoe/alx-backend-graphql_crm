#!/bin/bash
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

OUTPUT=$(python manage.py shell -c "
from crm.models import Customer
count=Customer.objects.filter(order__isnull=True).count()
Customer.objects.filter(order__isnull=True).delete()
print(f'Deleted {count} customers without orders . ')
)

echo "$TIMESTAMP - $OUTPUT" >> /tmp/customer_cleanup_log.txt