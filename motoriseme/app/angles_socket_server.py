import socketserver
import MySQLdb


class MyTCPHandler(socketserver.BaseRequestHandler):
    rider_id = 1

    def handle(self):
        self.data = self.request.recv(1024).strip()

        db = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="abcd1234",
                             db="chepec")
        cur = db.cursor()
        cur.execute("SELECT COUNT(*) FROM app_leanangle")
    
        pk_id = cur.fetchall()[0][0] + 1
        angle = self.data.decode("utf-8")
        query = 'INSERT INTO app_leanangle (id, user_id, angle) VALUES(' + str(pk_id) + ',' + ' (SELECT user_id FROM app_rider WHERE user_id = ' + str(self.rider_id) + '),' + str(angle) + ')'

        try:
            cur.execute(query)
            db.commit()
        except:
            db.rollback()
        db.close()


        print("{} wrote:".format(self.client_address[0]))
        print(self.data)

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 55666
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
