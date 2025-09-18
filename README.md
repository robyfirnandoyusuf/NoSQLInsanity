## Quick Setup 

1. Install docker
2. Type in your terminal `docker run -d --name db -p 8091-8096:8091-8096 -p 11210-11211:11210-11211 couchbase`
3. Configure couchbase (username,password)
4. Make a bucket and choose **travel-sample** bucket
5. `mv .env-example .env`
6. Setup your credentials
7. Type in your terminal: `npm install`
8. Type in your terminal: `node app.js`
