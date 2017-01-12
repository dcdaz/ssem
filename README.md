Server Script Executor Monitor a.k.a **SSEM** it's an app that allows to connect to ssh servers and execute some scripts on it without leave your local console.
**SSEM** uses 4 different parameters to work.

* First Parameter **--remotehost or -r**
    * This parameter allows to connect to ssh server, only if that server was previously saved on your ~/.ssh/config.
    * This parameter receives one or two argumets, first argument is the alias of your ssh server, the second argument is optional and it means execution time in seconds.
    * Examples:
      * python3 ssem.py -r server
      * python3 ssem.py -r server 10
    * Fynally you can choose your previously saved script on sqlite3 data base by enter the id number.


* Second parameter **--remoteexecute -x**
    * This parameter allows to connect to shh server whether it's on your ~/.ssh/config or not.
    * This parameter receives two or three argumets, firts argument is the alias of your ssh server or some another server like server@ip-address, the second argument is a custom script that not exist on sqlite3 DB and the third argument is optional and it means execution time in seconds.
    * Examples:
      * python3 ssem.py -x server 'df -h'
      * python3 ssem.py -x server 'du -h' 10
      * python3 ssem.py -x server@ip-address 'top -n 1'


* Third Parameter **--adscript -a**
    * This parameter allows to add scripts on sqlite3 DB and receives two arguments, first one is script itself and the second argument is a description of the script, if script or description has spaces on it, the use of quotation marks it's required.
    * Examples:
      * python3 ssem.py -a top memory
      * python3 ssem.py -a 'df -h' 'See free space on disk in human-readable way'


* Fourth Parameter **--deletescript -d**
    * This parameter allows to delete script from DB and receives only one argument for the id of the scrip that you want delete.
    * Examples:
      * python3 ssem.py -d 2

**Requirements**

**SSEM** requires python3-paramiko to make the ssh connection, please verify that you have this library install on your GNU/Linux system.
