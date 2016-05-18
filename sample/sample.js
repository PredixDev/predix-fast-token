'use strict';
const express = require('express');
const bearerToken = require('express-bearer-token');
const predixFastToken = require('predix-fast-token');
const app = express();

const trusted_issuers = ['https://f1615979-2469-4402-9a6e-3699caa34987.predix-uaa-staging.grc-apps.svc.ice.ge.com/oauth/token', 'https://090e7568-ec11-4318-b00a-041577780dfd.predix-uaa-staging.grc-apps.svc.ice.ge.com/oauth/token'];

app.get('/hello', (req, res, next) => {
    res.send('Howdy my unsecured friend!');
});

// Ensure Authorization header has a bearer token
app.all('*', bearerToken(), function(req, res, next) {
    console.log('Req Headers', req.headers);
    if(req.token) {
        predixFastToken.verify(req.token, trusted_issuers).then((decoded) => {
            req.decoded = decoded;
            console.log('Looks good');
            next();
        }).catch((err) => {
            console.log('Nope', err);
            res.status(403).send('Unauthorized');
        });
    } else {
		console.log('Nope, no token');
        res.status(401).send('Authentication Required');
    }
});

app.get('/secure', (req, res, next) => {
    res.send('Hello ' + req.decoded.user_name + ', my authenticated chum!');
});

// Need to let CF set the port if we're deploying there.
const port = process.env.PORT || 9001;
app.listen(port);
console.log('Started on port ' + port);

