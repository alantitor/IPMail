import sys
import time
import urllib2
import smtplib
import socket


# get device ip
def get_current_ip():
	try:
		response = urllib2.urlopen('http://checkip.dyndns.com', timeout = 5)
	except urllib2.URLError as err:
		#print "not connect"
		return ""
	except socket.timeout, e:
		#print "time out"
		return ""


	html = response.read()
	html = html.split('<body>')  # parse content
	html = html[1].split('</body>')
	ip_str = html[0].split(': ')[1]
	
	return ip_str


# send mail
def send_mail(new_ip):
	fromaddr = "from_mail@mail.com"
	toaddr = "to_mail@mail.com"

	# mail content
	msg = "This is the new IP for your server.\n"
	msg = msg + "IP: "
	msg = msg + new_ip
	#print msg

	# read accoun information
	info = list()
	data = open('account_info')
	for line in data:
		info.append(line.rstrip('\n'))
	

	username = info[0].split(':')[1]
	password = info[1].split(':')[1]


	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(username, password)
	server.sendmail(fromaddr, toaddr, msg)
	server.quit()


def main():
	old_ip = ""
	new_ip = ""

	while True:
		new_ip = get_current_ip()

		if (old_ip != new_ip) and (len(new_ip) != 0):
			send_mail(new_ip)
			#print "old ip: %s, new ip: %s" % (old_ip, new_ip)
			old_ip = new_ip
		else:
			#print "old2 ip: %s, new2 ip: %s" % (old_ip, new_ip)
			pass

		time.sleep(2)  # sleep 10 minutes


if __name__ == '__main__':
	main()
