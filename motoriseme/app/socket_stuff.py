import socketserver
import MySQLdb
import re


class MyTCPHandler(socketserver.BaseRequestHandler):
    rider_id = 1

    def convert(self, data):
        p = re.compile(str(data))
        m = p.match('.*\d*\.\d*')
        print(m.group(0))
        return m.group(0)

    def handle(self):
        self.data = self.request.recv(1024).strip()
        # angle = LeanAngle(user=rider, angle=self.client_address[0])
        # angle.save()


        

        db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                             user="root",         # your username
                             passwd="abcd1234",  # your password
                             db="chepec")        # name of the data base

        # you must create a Cursor object. It will let
        #  you execute all the queries you need
        cur = db.cursor()

        # Use all the SQL you like

        cur.execute("SELECT COUNT(*) FROM app_leanangle")
        for row in cur.fetchall():
            pk_id = row[0] + 1
        print(str(pk_id) + " IDDD")
        print(self.data)

        cur.execute("INSERT INTO app_leanangle (id, user_id, angle) VALUES(" + str(pk_id) + ",1," + self.convert(self.data))

        db.close()


        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 55666
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
