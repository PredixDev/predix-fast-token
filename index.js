'use strict'
const jwt = require('jsonwebtoken');
const request = require('request');
const url = require('url');
const debug = require('debug')('predix-fast-token');

let token_utils = {};
let oauthKeyCache = {};

// This will fetch and cache the public key of the UAA used for this tenant.
// This key can them be used to verify the JWT token presented so that the
// details contained within the token can be trusted.  Such as the user, expiry and scopes.
const getKey = (keyURL) => {
    // URL for the token is <UAA_Server>/token_key
    return new Promise((resolve, reject) => {
        // Check the cache
        if(oauthKeyCache[keyURL]) {
            // Already have it.
            resolve(oauthKeyCache[keyURL]);
        } else {
            // Fetch it and cache it for later
            debug('Fetching key from:', keyURL);
            request.get(keyURL, (err, resp, body) => {
                const statusCode = (resp) ? resp.statusCode : 502;
                if(err || statusCode !== 200) {
                    err = err || 'Error reading key: ' + statusCode;
                    debug('Error reading token key from', keyURL, err);
                    reject(err);
                } else {
                    debug('Fetched key');
                    const data = JSON.parse(body);
                    // Cache it
                    oauthKeyCache[keyURL] = data.value;
                    resolve(data.value);
                }
            });
        }
    });
}

token_utils.clearCache = () => {
    debug('Clearing key cache');
    oauthKeyCache = {};
}

/**
 * Verifies that a token was signed by a trusted UAA server and that it's still valid.
 *
 * @param {string} token - The access token.
 * @param {string} trusted_issuers - A list of trusted issuer URIs
 * @returns {promise} - A promise to verify the token.
 *                      Resolves with the decoded token if valid.
 *                      Rejected with an error if invalid or an error occurs.
 */
token_utils.verify = (token, trusted_issuers) => {
    return new Promise((resolve, reject) => {
        // Decode the token to get the issuer
        let prelim = null;
        try {
            prelim = jwt.decode(token);
        } catch(err) {
            debug('Error decoding token', err);
        }
        // Is this token claiming to be from a trusted issuer.
        if(prelim && trusted_issuers.indexOf(prelim.iss) > -1) {
            const issuer = url.parse(prelim.iss);
            // Just want the protocol and host, and any path before '/oauth/token'.
            const uaa_path = issuer.pathname.replace('/oauth/token', '');
            const uaa_server = url.format({ protocol: issuer.protocol, host: issuer.host, pathname: uaa_path+'/token_key'});
            // Grab the key for this UAA server and check.
            getKey(uaa_server).then((key) => {
                jwt.verify(token, key, (err, decoded) => {
                    if(err) {
                        debug('Invalid', err);
                        reject(err);
                    } else {
                        resolve(decoded);
                    }
                });
            }).catch((error) => {
                debug('get UAA key error', error);
                reject(error);
            });

        } else if(prelim) {
            // The decoded issuer is not in the trusted list.
            // No need to check that it's signed correctly
            reject(new Error('Not a trusted issuer'));
        } else {
            // The token is not a valid JWT token
            reject(new Error('Not a valid token'));
        }
    });
}

module.exports = token_utils;
