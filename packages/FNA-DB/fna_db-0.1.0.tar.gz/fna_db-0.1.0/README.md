# FNA-DBClient

Client für den FNA-DBServer

## DBClient
Die Klasse DBClient dient als Schnittstelle zwischen dem DBServer und einem Client. Es gibt funktionen, die relevant sind
1. connect - Öffnet eine Verbidnung zum Server
2. get_value('KEY') - ruft den Wert von KEY aus dem DB Server ab
3. set_value('KEY', 'VALUE') - Speichert oder Erstellt den Wert VALUE zum Schlüssel KEY auf dem DB Server ab. Der Server antwortet mit dem gespeicherten Wert
4. close - schließt die Veringun zum Server

### Env Variablen
Die Konfiguration kann auch via ENV Variablen erfolgen
* **FNA_DBSERVER_ADDR** - Adresse des Servers (default 12.0.0.1)
* **FNA_DBSERVER_PORT** - Port des Servers (Default 20002)

### Beispiel
```
# Instanz erstellen
db = DBClient('127.0.0.1', 20002)

db.connect()

val1 = db.set_value('test', 'Ich bin ein String')
print(val1) # $: 'Ich bin ein String'
val2 = db.get_value('test')
print(val2) # $: 'Ich bin ein String'

db.close()
```