import pyinputplus as pyip

# Get user input for email and SMTP server
email_address = pyip.inputEmail("Email Address: ")
default_smtp = ''
blank_value = False

# Determine the default SMTP server based on the email domain
if email_address.split('@')[1] == 'qq.com':
    default_smtp = 'smtp.qq.com'
elif email_address.split('@')[1] == '163.com':
    default_smtp = 'smtp.163.com'

# Get the SMTP server from the user with the default value based on the domain
smtp_domain = pyip.inputStr(f"smtp server (default {default_smtp}): ", default=default_smtp, blank=True)
smtp_port = pyip.inputInt("smtp server port (default 465): ", default=465, blank=True)

smtp_info = (smtp_domain, smtp_port)
print(smtp_info)
