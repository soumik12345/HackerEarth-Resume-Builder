import urllib3
import re
import os

# Generates the html file to be analyzed
def generate_html(address):
	http=urllib3.PoolManager()
	r=http.request('GET', address)
	f_write=open('test.html', "w")
	f_write.write(str(r.data))
	f_write.close()
	f_open=open('test.html', "r")
	f_output=open('output.html', "w")
	string=str(f_open.read())
	f_open.close()
	i=0
	while i<len(string)-1:
		if string[i]=='\\' and string[i+1]=='n':
			f_output.write("\n")
			i+=2
		elif string[i]=='\\' and string[i+1]=='s':
			f_output.write("\s")
			i+=2
		elif string[i]=='\\' and string[i+1]=='t':
			f_output.write("\t")
			i+=2
		else:
			f_output.write(str(string[i]))
			i+=1
	f_output.close()
	os.remove("test.html")

# Generates an array of lines from the root location of output.html
def generate_lines(address):
	f_open=open(address, 'r')
	sp=str(f_open.read()).split('\n')
	return sp

# Generates the name
def generate_name(line):
	sp=line.strip().split(' ')
	name=""
	for i in range(2, len(line)):
		if sp[i][0]!='(':
			name+=(sp[i]+" ")
		else:
			break
	return name

# Generates the username
def generate_username(line):
	sp=line.strip().split(' ')
	username=""
	for i in range(2, len(line)):
		if sp[i][0]=='(':
			s=sp[i]
			for j in range(1, len(s)-4):
				username+=s[j]
		if len(username)>=1:
			break
	return username

# Generates the current work status
def generate_current_work_status(lines):
	line=""
	for i in lines:
		if i.find("fa fa-briefcase")!=-1 or i.find("fa fa-university")!=-1:
			line=i
			break
	arr=re.findall(r'>([^<]*)<', line)
	work=""
	for i in arr:
		work+=i
	if len(work)<1:
		return "None"
	return work.strip()

# Generates the current location
def generate_location(lines):
	line=""
	for i in lines:
		if i.find("fa fa-map-marker")!=-1:
			line=i
			break
	arr=re.findall(r'>([^<]*)<', line)
	location=""
	for i in arr:
		location+=i
	if len(location)<1:
		return "Unknown"
	return location.strip()

# Driver Code
print("Enter the address of hackerearth profile: ", end="")
address=input()
generate_html(address)
lines=generate_lines('output.html')
print("\nNO OF LINES: "+str(len(lines)))
print("NAME: "+generate_name(lines[62]))
print("USERNAME: "+generate_username(lines[62]))
print("CURRENT WORKING STATUS: "+generate_current_work_status(lines))
print("CURRENT LOCATION: "+generate_location(lines))