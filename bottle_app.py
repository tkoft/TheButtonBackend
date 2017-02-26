'''
bottle_app.py

For HackSmith 2017.  Backend for The Button.
To run on a pythonanywhere bottle instance.

(c) gary chen 2017
'''
from bottle import default_app, request, route, run
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
        print(filename)
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
        if button in group.buttons:
            groups[group].buttons[button].pushes.append({"user":user, "time":time})
            saveGroupJSON(group)
            return "push_success"
        return "error_button_not_found"
    return "error_group_not_found"

@route('/delete-button')
def deleteButtonHandler():
    return deleteButton(request.query.group, request.query.button)
def deleteButton(group, button):
    if group in groups:
        if button in group.buttons:
            del groups[group].buttons[button]
            saveGroupJSON(group)
            return "delete_button_success"
        return "error_button_not_found"
    return "error_group_not_found"

@route('join-group')
def joinGroupHandler():
    return joinGroup(request.query.group, request.query.user)
def joinGroup(group, user):
    if group in groups:
        if user in group.users:
            groups[group].users.append(user)
            saveGroupJSON(group)
            return "join_group_success"
        return "error_button_not_found"
    return "error_group_not_found"


@route('/leave-group')
def leaveGroupHandler():
    return leaveGroup(request.query.group, request.query.user)
def leaveGroup(group, user):
    if group in groups:
        if user in group.users:
            groups[group].users.remove(user)
            res = "leave_group_success"
            if len(groups[group].users) == 0:
                del groups[group]
                res += ":group_deleted"
            saveGroupJSON(group)
            return res
        return "error_button_not_found"
    return "error_group_not_found"

@route('/get-all-json')
def getAllJSON():
    res = "ALL:"
    for key in groups:
        res += json.dumps(groups[key])
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
    return getActiveUsers(request.query.button, request.query.time)
def getActiveUsers(button, ctime):
    lastTime = ctime;
    res = {}
    for i in range(len(button.pushes), -1, -1):
        if lastTime - button.pushes[i] >= button.timeout:
            break
        else:
            res[button.pushes[i].user] = users[button.pushes[i].user]
    return res

### TEST CODE ###
if __name__=="__main__":
    garyID = newUser("Gary")
    lalalaID = newGroup("lalala", garyID)
    newButton("dinnertime!", lalalaID, 300)
    print(getAllJSON())

    #run(host='localhost', port=8080, debug=True)

application = default_app()






