import sys, logging, time, os
import mysql.connector
from mysql.connector import Error
from MetaSingleton import MetaSingleton

class LocalDBConnection(metaclass=MetaSingleton):
    connection = None
    # ts stores the time in seconds
    connection_timestamp = None
    connection_age = None
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    secure_path = os.path.join(current_dir, "../../../secure")
    sys.path.append(secure_path)
    import credentials
    database_credentials = credentials.database_credentials
    
    def disconnect(self):
        if self.connection is not None:
            self.connection.disconnect()
            self.connection = None
            
    def connect(self):
        if self.connection is None:

            try:
                self.connection = mysql.connector.connect(**self.database_credentials)
                if self.connection.is_connected():
                    self.connection_timestamp = time.time()
                    db_Info = self.connection.get_server_info()
                    cursor = self.connection.cursor(dictionary=True)
                    cursor.execute("SET wait_timeout = 31536000;")
                    cursor.execute("SET interactive_timeout = 31536000;")
                    cursor.execute("SET net_read_timeout = 31536000;")
                    cursor.execute("SET wait_timeout = 31536000;")
                    logging.debug("timeouts set")            

                    
            except Error as e:
                print("Error connecting to the LOCAL datalake Database")
                print(e)
                sys.exit(1)

        else:
            self.connection_age = time.time() - self.connection_timestamp

            #logging.debug('the datalake connection is this many seconds old: ' + str(self.connection_age))
            if self.connection_age > 900:
              
                self.connection.disconnect()
                self.connection = None
                try:
                    self.connection = mysql.connector.connect(**self.database_credentials)
                    if self.connection.is_connected():
                        self.connection_timestamp = time.time()
                        self.connection_age = time.time() - self.connection_timestamp
                        db_Info = self.connection.get_server_info()
                        cursor = self.connection.cursor()
                        cursor.execute("SET wait_timeout = 31536000;")
                        cursor.execute("SET interactive_timeout = 31536000;")
                        cursor.execute("SET net_read_timeout = 31536000;")
                        cursor.execute("SET wait_timeout = 31536000;")
                        logging.debug("timeouts set")                          
                  
                except Error as e:
                    print("Error connecting to the LOCAL datalake Database")
                    print(e)
                    sys.exit(1)
                  
        return self.connection
    
        
         