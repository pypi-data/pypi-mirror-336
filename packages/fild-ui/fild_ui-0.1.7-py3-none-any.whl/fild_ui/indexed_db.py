from fild_ui import Browser


class Command:
    GET_ALL = """
        return new Promise((resolve, reject) => {{
            let request = indexedDB.open("{0}");  
            
            request.onsuccess = function(event) {{
                let db = event.target.result;
                let transaction = db.transaction("{1}", "readonly"); 
                let store = transaction.objectStore("{1}");
                let allRecords = store.getAll();
                
                allRecords.onsuccess = function() {{
                    resolve(allRecords.result);
                }};
                allRecords.onerror = function() {{
                    reject("Error reading IndexedDB");
                }};
            }};
            
            request.onerror = function() {{
                reject("IndexedDB open failed");
            }};
        }});
    """
    DELETE_ALL = """
        return new Promise((resolve, reject) => {{
            let request = indexedDB.open("{0}");  

            request.onsuccess = function(event) {{
                let db = event.target.result;
                let transaction = db.transaction("{1}", "readwrite");
                let store = transaction.objectStore("{1}");
                let deleteRequest = store.clear();

                deleteRequest.onsuccess = function() {{
                    resolve("Deletion successful");
                }};
                deleteRequest.onerror = function() {{
                    reject("Error deleting record");
                }};
            }};

            request.onerror = function() {{
                reject("IndexedDB open failed");
            }};
        }});
    """
    CREATE_NEW = """
        return new Promise((resolve, reject) => {{
            let request = indexedDB.open("{0}"); 

            request.onsuccess = function(event) {{
                let db = event.target.result;
                let transaction = db.transaction("{1}", "readwrite");
                let store = transaction.objectStore("{1}");
                let insertRequest = store.add({2});
                
                insertRequest.onsuccess = function() {{
                    resolve("Insertion successful");
                }};
                insertRequest.onerror = function(event) {{
                    reject("Error inserting record: " + event.target.error);
                }};
            }};

            request.onerror = function() {{
                reject("IndexedDB open failed");
            }};
        }});
    """


class IndexedDb:
    def __init__(self, name):
        self.name = name

    def get_all_records(self, table_name):
        return Browser().driver.execute_script(
            Command.GET_ALL.format(self.name, table_name)
        )

    def delete_all_records(self, table_name):
        return Browser().driver.execute_script(
            Command.DELETE_ALL.format(self.name, table_name)
        )

    def insert_record(self, table_name, record_json):
        return Browser().driver.execute_script(
            Command.CREATE_NEW.format(self.name, table_name, record_json)
        )
