[(send, more, money) for send in range(1023,9877) for more in range(1023,9877) for money in [send+more]
	if send + more > 9999
	   and str(send)[1] == str(more)[3]
	   and str(money)[:4] == str(more)[:2] + str(send)[2:0:-1]
	   and len("".join(set(str(money) + str(send) + str(more)))) == 8]