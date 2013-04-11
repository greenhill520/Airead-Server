Airead-Server
=============

The Server of Airead

Airead, Your final RSS reader.

#Dependences:

- [Flask][1]: an awesome web framework

- [Flask-SQLAlchemy][2]: adds SQLAlchemy support to Flask. Quick and easy.

- [Flask-Script][3]: provides support for writing external scripts in Flask

- [Flask-Admin][4]: provides an admin interface

- [Flask-Login][5]: provides user session management for Flask
 
- [APScheduler][6], [Python-RQ][7]: message queuing and task schedule utilities

- [feedparser][8]: and universal feed parser

#Getting Start

```bash
$ virtualenv venv
$ source venv/bin/active
$ pip install -r requirements.txt
$ python syncdb.py
$ python manager.py runserver
```



[1]: http://flask.pocoo.org/
[2]: http://pythonhosted.org/Flask-SQLAlchemy/
[3]: http://flask-script.readthedocs.org/en/latest/
[4]: http://flask-admin.readthedocs.org/en/latest/index.html
[5]: http://pythonhosted.org/Flask-Login/
[6]: https://apscheduler.readthedocs.org/
[7]: http://python-rq.org/
[8]: http://pythonhosted.org/feedparser/
