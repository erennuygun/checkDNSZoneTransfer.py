import os
import argparse
from colorama import Fore, Back, Style


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url",help="add target")
args = parser.parse_args()

os.system("dig ns "+args.url+" | awk '/NS/ {print $5}' | grep -v 'flags:;' | grep -v 'ra;' |  sed '/^$/d;s/[[:blank:]]//g' > ns.txt")

def check_string(fname, str):
	for line in fname.read().splitlines():
		if str in line:
			return True
	return False

f = open("ns.txt","r")

for line in f.read().splitlines():
	os.popen("dig @"+line+" "+args.url+" axfr > tmpcom").read()
	output = os.popen("head -n -6 tmpcom | tail -n +5").read()
	f2 = open("tmpcom","r")
	if (check_string(f2,"Transfer failed.")):
		print(Fore.RED + "Transfer Failed with this NS Record : " + line)
	else:
		print(Fore.GREEN + " Transfer Completed")
		print(Style.RESET_ALL)
		print(output)

os.remove("tmpcom")
os.remove("ns.txt")
