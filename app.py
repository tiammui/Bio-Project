from flask import Flask, render_template, request
from zk import ZK, const
from datetime import datetime

zk = ZK(
    "192.168.1.201", port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False
)

app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/users")
def users():
    # connect to device
    conn = zk.connect()
    # disable device, this method ensures no activity on the device while the process is run
    conn.disable_device()
    # another commands will be here!
    # Example: Get All Users
    users = conn.get_users()
    userList = []
    for user in users:
        privilege = False
        if user.privilege == const.USER_ADMIN:
            privilege = True

        userList.append(
            {
                "name": user.name,
                "uid": user.uid,
                "userID": user.user_id,
                "department": user.group_id,
                "isAdmin": privilege,
            }
        )

    # re-enable device after all commands already executed
    conn.enable_device()

    print(userList)

    return userList


@app.route("/attendances")
def attendances():
    # connect to device
    conn = zk.connect()
    # disable device, this method ensures no activity on the device while the process is run
    conn.disable_device()
    # another commands will be here!
    # Example: Get All Users
    attends = conn.get_attendance()
    attList = []
    for att in attends:
        attList.append(
            {
                "status": att.status,
                "timestamp": datetime.timestamp(att.timestamp),
                "userID": att.user_id,
            }
        )

    conn.clear_attendance()
    # re-enable device after all commands already executed
    conn.enable_device()

    print(attList)

    return attList


@app.post("/enroll")
def enroll():
    # connect to device
    conn = zk.connect()
    # disable device, this method ensures no activity on the device while the process is run
    conn.disable_device()

    body = request.json

    conn.enroll_user(user_id=body["userID"], temp_id=body["tempID"])

    # re-enable device after all commands already executed
    conn.enable_device()


@app.post("/user/<userid>")
def user(userid):
    # connect to device
    conn = zk.connect()
    # disable device, this method ensures no activity on the device while the process is run
    conn.disable_device()

    body = request.json
    print(body)
    conn.set_user(name=body["name"], user_id=body["userID"], group_id=body["department"])

    # re-enable device after all commands already executed
    conn.enable_device()

    return "success"


@app.post("/newuser")
def add_user():
    # connect to device
    conn = zk.connect()
    # disable device, this method ensures no activity on the device while the process is run
    conn.disable_device()

    body = request.json
    print(body)
    # conn.set_user(name=body['name'],user_id=body['userID'],group_id=body['department'])
    conn.set_user(
        uid=body["uid"],
        name=body["name"],
        user_id=body["userID"],
        group_id=body["department"],
    )

    # re-enable device after all commands already executed
    conn.enable_device()

    return "success"


@app.route("/connectstatus")
def connect_status():
    # connect to device
    conn = zk.connect()
    # re-enable device after all commands already executed
    conn.enable_device()

    if conn:
        conn.set_time(datetime.now())
        sn = conn.get_serialnumber()
        name = conn.get_device_name()

        conn.read_sizes()
        users = conn.users
        fingers = conn.fingers
        return {
            "serialnumber": sn,
            "devicename": name,
            "users": users,
            "fingers": fingers,
        }
    else:
        return "lost"


app.run(host="127.0.0.1",port=5000)
