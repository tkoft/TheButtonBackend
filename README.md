The Button Request Routes

Request from URL with parameters like this.  This example creates a new button with description "MyNewButton" in the group with HashID WkByaXYYXZj7B and a timeout period of 15 minutes.
	
	http://tkoft.pythonanywhere.com/new-button?label=MyNewButton&group=WkByaXYYXZj7B&timeout=900

Note:  groups are identified by a shorter HashID, for ease of sharing.  Buttons and users are identified by 128-bit UUID. 


Routes:

/new-user:			Creates a new user
	name: 			a nickname to give the user
	return: 		UUID string for user 

/new-group:			Creates a new group from a user
	name: 			nickname for group 	
	creator: 		UUID of group creator (first member)
	return: 		HashID string for group

/new-button:		Creates a new button in a group
	label:  		button description string	
	group: 			HashID of group that owns Button
	timeout:  		timeout time for button (how long until active users reset)
	return:			UUID string for button, or failure if group not found

/new-push:			Records a button push instance
	group:			HashID of group button belongs to
	button:			button UUID
	user:			UUID of user
	time:			time of button push, Unix time
	return: 		success or failure message if group or button not found

/delete-button:		removes button from group's button list
	group:			HashID of group button belongs to
	button:			button UUID
	return:			success or failure message if group or button not found

/join-group:		adds a new user to a group's member list
	group:			HashID of group
	user:			UUID of user to add
	return: 		success or failure message if group not found

/leave-group:		removes a user from a group's member list. Also deletes 
					group if no members left.
	group:			HashID of group 
	user:			UUID of user to remove
	return: 		success or failure message if group or user not found

/get-all-json:		returns a somewhat readable list of JSON strings 
					representing each group.  NOT IN JSON FORMAT!!!
	return:			aforementioned

/get-group-json:	returns JSON for group, including all members and buttons 
					and button info and pushes.
	group:			HashID of group
	return:			aforementioned

/get-users-json:	returns JSON of dictionary of users (UUID key -> nickname)
	return:			aforementioned

/get-active-users:	returns JSON of list of users that were active on a button 
					at the specified Unix time
	group:			HashID of group button belongs to
	button:			UUID of button to check
	time:			time to check, in Unix time
	return:			JSON of dict of users (UUID --> nickname) that were in the 
					button event at the specified time	 			
