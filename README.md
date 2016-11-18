# predix-fast-token
Node module to verify UAA tokens used when protecting REST endpoints

## Intro
Security is important, but having to make a POST call to UAA with every request to verify a token adds latency. Predix-fast-token reduces the number of network calls and is ~200+ times faster. We ran a test of 100,000 predix-fast-token calls and it came out to <1 ms. Don't trust us though, try youself and see what improvements you can get compared to your current method.

## Installation
Install via npm

```
npm install --save predix-fast-token
```

## Usage

### Verify (Local)
Validates the token is a valid JWT, isn't expired, and was issued by a trusted issuer.


Basic usage with a JWT token and list of trusted issuers

```javascript
const pft = require('predix-fast-token');
pft.verify(token, trusted_issuers).then((decoded) => {
     // The token is valid, not expired and from a trusted issuer
     // Use the value of the decoded token as you wish.
     console.log('Good token for', decoded.user_name);
}).catch((err) => {
    // Token is not valid, or expired, or from an untrusted issuer.
    console.log('No access for you', err);
});
```

As an expressjs middleware

```javascript
'use strict';
const express = require('express');
const bearerToken = require('express-bearer-token');
const predixFastToken = require('predix-fast-token');
const app = express();

const trusted_issuers = ['https://example.uaa.predix.io/oauth/token', 'https://another.uaa.predix.io/oauth/token'];

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

```
### Remote Verification
Validates a token is valid by sending it against the UAA's `/check_token` endpoint, with optional in-memory caching.
Using remote verification adds network latency to the verification request, compared to local verification,
but is necessary if you need to validate [opaque tokens](https://www.cloudfoundry.org/opaque-access-tokens-cloud-foundry/)
or check if a token has been revoked.

#### Parameters
- `token` - The access token
- `issuer`- The UAA issuer URI to validate against
- `clientId` - Your client ID issued by the UAA service
- `clientSecret` - Your client secret issued by the UAA service
- `opts` 
    - `ttl` - The maximum time to live in cache for a validated token, in seconds. If zero, does not cache. `Default: 0`
    - `useCache` - Whether or not to look for the token in cache. `Default: true`

#### Example
```javascript
const pft = require('predix-fast-token');
const opts = {ttl: 60*60*2, useCache: true}; // Cache tokens for 2 hours
pft.remoteVerify(token, issuer, clientId, clientSecret, opts).then((decoded) => {
     // The token is valid, not expired or revoked, and from the given issuer
     // Use the value of the decoded token as you wish.
     console.log('Good token for', decoded.user_name);
}).catch((err) => {
    // Token is not valid, revoked, expired, or from a different issuer.
    console.log('No access for you', err);
});
```
