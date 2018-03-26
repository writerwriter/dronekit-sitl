import folder_transfer as ftransfer

Mission_number = 7
uploader = raw_input("Task is Done,do you want to upload the data ?(Y/n)")
if uploader is 'Y':
	if ftransfer.fileCount(str(Mission_number)) > 0:
		ftransfer.transfer(str(Mission_number))
		print "Finish upload..( %d photos )" % ftransfer.fileCount(str(Mission_number))
	elif uploader is 'n':
		print "Finish..."