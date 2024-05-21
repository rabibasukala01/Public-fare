from django.test import TestCase

# Create your tests here.
import hashlib

password='9841ABcd'
my_bytes = password.encode('utf-8')

print((hashlib.sha256(my_bytes).hexdigest()))
