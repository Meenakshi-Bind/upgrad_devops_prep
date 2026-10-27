mystr = 'HEllo World'
newUppercaseStr = mystr.upper()
print(f'coverted touppercasse {newUppercaseStr}')

newLowerCase = mystr.lower()
print(f'coverted to lowercase {newLowerCase}')

newsplit = mystr.split()
print(f'my splitted string {newsplit}')


email = 'alice.johnson@company.com'
print(f'Email: {email}')

at_position = email.find('@')
print(f'Position of @: {at_position}')

username = email[:at_position]
print(f'Username: {username}')

has_at = '@' in email
print(f'Has @ symbol: {has_at}')

has_com = '.com' in email
print(f'Has .com: {has_com}')

messy_name = '  sARaH dAVis  '
print(f"Original name: '{messy_name}'")

clean_name = messy_name.strip().title()
print(f"Cleaned name: '{clean_name}'")

messy_email = '  SARAH.DAVIS@COMPANY.COM  '
clean_email = messy_email.strip().lower()
print(f"Original email: '{messy_email}'")
print(f"Cleaned email: '{clean_email}'")

name_badge = clean_name.upper()
print(f'Name badge: {name_badge}')

at_pos = clean_email.find('@')
email_user = clean_email[:at_pos]

print(f'Email: {clean_email}')
print(f'Username: {email_user}')

display_name = email_user.replace('.', ' ').title()
print(f'Display name: {display_name}')

phone = '123-456-7890'
phone_clean = phone.replace('-', '')
print(f'Phone with dashes: {phone}')
print(f'Phone without dashes: {phone_clean}')

full_address = '123 Main Street, Springfield, IL'
address_parts = full_address.split(', ')
print(f'Address parts: {address_parts}')

rejoined = ' | '.join(address_parts)
print(f'Rejoined: {rejoined}')

employee_code = 'EMP-2024-SD'
starts_with_emp = employee_code.startswith('EMP')
ends_with_com = clean_email.endswith('.com')

print(f'Code: {employee_code}')
print(f'Starts with EMP: {starts_with_emp}')
print(f'Clean email: {clean_email}')
print(f'Ends with .com: {ends_with_com}')

dot_count = clean_email.count('.')
dash_count = employee_code.count('-')

print(f'Dots in email: {dot_count}')
print(f'Dashes in code: {dash_count}')

##output
# Email: alice.johnson@company.com
# Position of @: 13
# Username: alice.johnson
# Has @ symbol: True
# Has .com: True
# Original name: '  sARaH dAVis  '
# Cleaned name: 'Sarah Davis'
# Original email: '  SARAH.DAVIS@COMPANY.COM  '
# Cleaned email: 'sarah.davis@company.com'
# Name badge: SARAH DAVIS
# Email: sarah.davis@company.com
# Username: sarah.davis
# Display name: Sarah Davis
# Phone with dashes: 123-456-7890
# Phone without dashes: 1234567890
# Address parts: ['123 Main Street', 'Springfield', 'IL']
# Rejoined: 123 Main Street | Springfield | IL
# Code: EMP-2024-SD
# Starts with EMP: True
# Clean email: sarah.davis@company.com
# Ends with .com: True
# Dots in email: 2
# Dashes in code: 2