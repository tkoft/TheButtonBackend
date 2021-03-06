'''
bottle_app.py

For HackSmith 2017.  Backend for The Button.
To run on a pythonanywhere bottle instance.

(c) gary chen 2017
'''
from bottle import default_app, request, route
from hashids import Hashids
hashids = Hashids("salt lolololol")
import json, uuid, os.path

users = {}

groups = {}

### LOAD JSON FILES ###
if os.path.isfile("userlist.json"):
    usersFile = open("userlist.json", 'r')
    users = json.load(usersFile)
    usersFile.close()

for filename in os.listdir(os.getcwd()+"/groupsJSON"):
    if os.path.isfile(os.getcwd()+"/groupsJSON/"+filename):
        myfile = open(os.getcwd()+"/groupsJSON/"+filename, 'r')
        groups[str.split(filename, '.')[0]] = json.load(myfile)
        myfile.close()


### JSON WRITING HELPERS ###
def saveGroupJSON(group):
    # save group to json, or delete json if group doesn't exist
    if group in groups:
        myfile = open("groupsJSON/"+group+".json", 'w')
        #print(groups[group])
        myfile.write(json.dumps(groups[group]))
        myfile.close()
    else:
        if os.path.isfile("groupsJSON/"+group+".json"):
            os.remove("groupsJSON/"+group+".json")

def saveUsersJSON():
    myfile = open("userlist.json", 'w')
    myfile.write(json.dumps(users))
    myfile.close()


### OTHER HELPERS ###

def newGroupId():
    u = str(uuid.uuid4()).replace('-','')
    h1 = int(u[:len(u)/2], 16)
    h2 = int(u[len(u)/2:], 16)
    return hashids.encode(h1 ^ h2)



### BOTTLE REQUEST ROUTES ###

@route('/')
def init():
    return "Oh no you're not supposed to see this!!!"

@route('/new-user')
def newUserHandler():
    return newUser(request.query.name)
def newUser(name):
    id = str(uuid.uuid4())
    users[id] = name
    saveUsersJSON()
    return id

@route('/new-group')
def newGroupHandler():
    return newGroup(request.query.name, request.query.creator)
def newGroup(name, creator):
    id = newGroupId()
    groups[id] = {"name":name, "members":{creator:users[creator]}, "buttons":{}}
    saveGroupJSON(id)
    return id

@route('/new-button')
def newButtonHandler():
    return newButton(request.query.label, request.query.group, request.query.timeout)
def newButton(label, group, timeout):
    if group in groups:
        id = str(uuid.uuid4())
        groups[group]['buttons'][id] = {"label":label, "timeout":timeout, "pushes":[]}
        saveGroupJSON(group)
        return id
    return "error_group_not_found"

@route('/new-push')
def newPushHandler():
    return newPush(request.query.group, request.query.button, request.query.user, request.query.time)
def newPush(group, button, user, time):
    if group in groups:
        if button in groups[group]['buttons']:
            groups[group]['buttons'][button]['pushes'].append({"user":user, "time":time})
            saveGroupJSON(group)
            return "push_success"
        return "error_button_not_found"
    return "error_group_not_found"

@route('/delete-button')
def deleteButtonHandler():
    return deleteButton(request.query.group, request.query.button)
def deleteButton(group, button):
    if group in groups:
        if button in groups[group]['buttons']:
            del groups[group]['buttons'][button]
            saveGroupJSON(group)
            return "delete_button_success"
        return "error_button_not_found"
    return "error_group_not_found"

@route('join-group')
def joinGroupHandler():
    return joinGroup(request.query.group, request.query.user)
def joinGroup(group, user):
    if group in groups:
        groups[group]['members'][user] = users[user]
        saveGroupJSON(group)
        return "join_group_success"
    return "error_group_not_found"


@route('/leave-group')
def leaveGroupHandler():
    return leaveGroup(request.query.group, request.query.user)
def leaveGroup(group, user):
    if group in groups:
        if user in group['members']:
            groups[group].users.remove(user)
            res = "leave_group_success"
            if len(groups[group].users) == 0:
                del groups[group]
                res += ":group_deleted"
            saveGroupJSON(group)
            return res
        return "error_user_not_found"
    return "error_group_not_found"

@route('/get-all-json')
def getAllJSON():
    res = "ALL:  "
    for key in groups:
        res += key + ":  " + json.dumps(groups[key]) + "\n\n"
    return res

@route('/get-group-json')
def getGroupJSONHandler():
    return getGroupJSON(request.query.group)
def getGroupJSON(group):
    if group in groups:
        return json.dumps(groups[group])
    return "error_group_not_found"

@route('/get-users-json')
def getUsersJSON():
    return json.dumps(users)

@route('/get-active-users')
def getActiveUsersHandler():
    return getActiveUsers(request.query.button, request.query.button, request.query.time)
def getActiveUsers(group, button, ctime):
    lastTime = ctime;
    res = {}
    pushesList = groups[group]['buttons'][button]['pushes']
    for i in range(len(pushesList)-1, -1, -1):
        if lastTime - pushesList[i]['time'] >= groups[group]['buttons'][button]['timeout']:
            break
        else:
            res[pushesList[i]['user']] = users[pushesList[i]['user']]
            lastTime = pushesList[i]['time']
    return json.dumps(res)

### TEST CODE ###
if __name__=="__main__":
    garyID = newUser("Gary")
    lalalaID = newGroup("lalala", garyID)
    josephID = newUser("Joseph")
    dinnerID = newButton("dinner", lalalaID, 400)
    newPush(lalalaID, dinnerID, garyID, 1600)

    print(joinGroup(lalalaID, josephID))
    davidID = newUser("David")
    joinGroup(lalalaID, davidID)
    gymID = newButton("gym", lalalaID, 200)
    newPush(lalalaID, dinnerID, davidID, 1700)

    newPush(lalalaID, gymID, davidID, 1400)
    newPush(lalalaID, gymID, garyID, 1600)
    newPush(lalalaID, gymID, josephID, 1700)

    print(getActiveUsers(lalalaID, gymID, 1800))



application = default_app()






