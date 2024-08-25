# pyAPIdev
A repository for study of APIs. The repo uses python's HTTPServer library to manually build a CRUD website and back it with an API sidestepping frameworks allowing direct interaction with the socket protocols to understand exactly what the API does.

Stack can be deployed from the docker-compose.yml, it will include the website (yet to be finished), API, MySQL server for database storage and PHPMyAdmin to manage and monitor it through the GUI. Dockerfiles for the individual container builds are in the dockerfiles folder, the compose environment variables are in .env, container environment variables are kept in the environment folder. All the code for the servers are in src, and the website should be kept in web, style and scripts folder beneath this. To manage the MySQL server passwords are needed, I keep these in a secrets folder at the root level of the repo that is not pushed to the repo to ensure everyone must set up their own.

I've silenced the favicon.ico error with a 0-byte response, but this can also be used to send an image with a little bit of tweaking.
