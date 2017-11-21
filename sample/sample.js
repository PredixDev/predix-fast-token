'use strict';
const express = require('express');
const bearerToken = require('express-bearer-token');
const predixFastToken = require('../');
const app = express();

const trusted_issuers = ['https://95e4a01d-0fa4-4bcf-bbe2-76c504322360.predix-uaa.run.aws-usw02-pr.ice.predix.io/oauth/token'];

app.get('/hello', (req, res, next) => {
    res.send('Howdy my unsecured friend!');
});

// Ensure Authorization header has a bearer token
app.get('/fast', bearerToken(), function(req, res, next) {
    console.log('Req Headers', req.headers);
    if(req.token) {
        predixFastToken.verify(req.token, trusted_issuers).then((decoded) => {
            req.decoded = decoded;
            console.log('Looks good');
            res.send('Hello ' + req.decoded.user_name + ', my fast-token authenticated chum!');
        }).catch((err) => {
            console.log('Nope', err);
            res.status(403).send('Unauthorized');
        });
    } else {
		console.log('Nope, no token');
        res.status(401).send('Authentication Required');
    }
});

// Ensure Authorization header has a bearer token
app.get('/remote', bearerToken(), function(req, res, next) {
    console.log('Req Headers', req.headers);
    if(req.token) {
        predixFastToken.remoteVerify(req.token, trusted_issuers[0], 'token_check_user', '4751a79c-de03-4b1a-a573-0980cce4b4ca', { ttl: 5, useCache: true }).then((decoded) => {
            req.decoded = decoded;
            console.log('Looks good');
            res.send('Hello ' + req.decoded.user_name + ', my remote authenticated chum!');
        }).catch((err) => {
            console.log('Nope', err);
            res.status(403).send('Unauthorized');
        });
    } else {
		console.log('Nope, no token');
        res.status(401).send('Authentication Required');
    }
});

// Need to let CF set the port if we're deploying there.
const port = process.env.PORT || 9001;
app.listen(port);
console.log('Started on port ' + port);
