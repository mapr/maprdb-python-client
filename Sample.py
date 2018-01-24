from entity.document.Document import Document
from entity.document.DocumentStore import DocumentStore
from entity.storage.ConnectionManager import ConnectionManager
from entity.storage.Connection import Connection


"""Example for customer may works with Python client"""
connection = Connection(ConnectionManager.get_connection(url="ojai:mapr:user@password"))

store = DocumentStore(connection.get_store(store_name="/test_name"))


# Json string or json map (probably json object)
json_document = "json string"

new_document = connection.new_document(json_document)

store.insert_or_replace(new_document)

store.close()
