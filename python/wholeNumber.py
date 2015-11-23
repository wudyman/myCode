theNumber=raw_input("please input the test Number:")
theNumber=int(theNumber)
divider=1
sumofNumber=0
while divider<theNumber:
	if theNumber%divider==0:
		sumofNumber+=divider
	divider+=1
if sumofNumber==theNumber:
	print "is whole number"
else:
	print "not a whole number"
