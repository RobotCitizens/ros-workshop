def get_position(self):
	self.listener = tf.TransformListener() 
	rate = rospy.Rate(10.0)
	get_position = False
	while not rospy.is_shutdown() and not get_position:
	    try:
		(trans,rot) = self.listener.lookupTransform("/map","/base_link", rospy.Time(0))
		if trans != None:
		    get_position = True
		    print(trans)

	    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
		continue
	rate.sleep()
	euler = tf.transformations.euler_from_quaternion(rot)
	return trans[0], trans[1], euler[2]

def save_position(self, position_name):
	try:
	    x,y,theta = self.get_position()
	    thisdict = self.read_csv()
	    thisdict[position_name] = [x,y,theta]
	    thislist = []
	    for x in thisdict:    
		thislist.append([x,thisdict.get(x)[0],thisdict.get(x)[1],thisdict.get(x)[2]])
	    
	    with open("file.csv", "w") as csv_file:
		csv_writer = csv.writer(csv_file,delimiter=',')
		for x in thislist:
		    csv_writer.writerow(x)
	    return True
	except:
	    return False   

