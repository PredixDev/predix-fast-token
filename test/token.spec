'use strict'
const chai = require('chai');
const expect = chai.expect;
const request = require('request');
const sinon = require('sinon');
const token_util = require('../index');

const key1 = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0m59l2u9iDnMbrXHfqkO\nrn2dVQ3vfBJqcDuFUK03d+1PZGbVlNCqnkpIJ8syFppW8ljnWweP7+LiWpRoz0I7\nfYb3d8TjhV86Y997Fl4DBrxgM6KTJOuE/uxnoDhZQ14LgOU2ckXjOzOdTsnGMKQB\nLCl0vpcXBtFLMaSbpv1ozi8h7DJyVZ6EnFQZUWGdgTMhDrmqevfx95U/16c5WBDO\nkqwIn7Glry9n9Suxygbf8g5AzpWcusZgDLIIZ7JTUldBb8qU2a0Dl4mvLZOn4wPo\njfj9Cw2QICsc5+Pwf21fP+hzf+1WSRHbnYv8uanRO0gZ8ekGaghM/2H6gqJbo2nI\nJwIDAQAB\n-----END PUBLIC KEY-----\n";
const key2 = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5VXMZBf2fUqNViwhkaKC\ntpnKX4MgKAcFA8KGiFYgChss8v/yB41wA8f+UfJmCOMIswRELKjHOp4tm9XtkCqy\nO/09RHqkrxG33za5tUhXSLaYX9MyMJcvbAXJ8cE9uu5Hv6Q4Gs65q/brwchh87Yb\nlCCvqGQ7QggEjqt2+bWGgjHDw9pKBXXRkA8t3fsH+sh2YgGCoRHH5Dd5QKpVkIGW\nnXlNIjRTd4g7rjE4Y3F1TaAhHpCoMOdviR++RIs3PdCi8ZUoS7V+mCWwOr61D7At\nxBjdnDDu/PZgLxlt1JEXt07V0xTzjztJ4r8qz5PkBZJeuZpHmiZoDNEquOhMQPhB\nIQIDAQAB\n-----END PUBLIC KEY-----\n"

const token1_valid = 'eyJhbGciOiJSUzI1NiJ9.eyJqdGkiOiI3ZDE0ZDVmMS0xMmVhLTQyNGItODE5Yi1iNWViNTk2NTVhOWEiLCJzdWIiOiIxNmVjMTk0OC02ZTBiLTQzMGUtYmE4Yi1kMzQ1ZDI3MzQ0YzciLCJzY29wZSI6WyJleGFtcGxlLndyaXRlIiwiZXhhbXBsZS5yZWFkIiwib3BlbmlkIl0sImNsaWVudF9pZCI6ImV4YW1wbGUiLCJjaWQiOiJleGFtcGxlIiwiYXpwIjoiZXhhbXBsZSIsImdyYW50X3R5cGUiOiJhdXRob3JpemF0aW9uX2NvZGUiLCJ1c2VyX2lkIjoiMTZlYzE5NDgtNmUwYi00MzBlLWJhOGItZDM0NWQyNzM0NGM3Iiwib3JpZ2luIjoidWFhIiwidXNlcl9uYW1lIjoiZGVtbyIsImVtYWlsIjoiZGVtb0Bsb2NhbCIsImF1dGhfdGltZSI6MTQ2MTAzODI1OSwicmV2X3NpZyI6IjU2YjJiNGZiIiwiaWF0IjoxNDYxMDM4Mjg0LCJleHAiOjM2MDg1MjE5MzEsImlzcyI6Imh0dHBzOi8vMDkwZTc1NjgtZWMxMS00MzE4LWIwMGEtMDQxNTc3NzgwZGZkLnByZWRpeC11YWEtc3RhZ2luZy5ncmMtYXBwcy5zdmMuaWNlLmdlLmNvbS9vYXV0aC90b2tlbiIsInppZCI6IjA5MGU3NTY4LWVjMTEtNDMxOC1iMDBhLTA0MTU3Nzc4MGRmZCIsImF1ZCI6WyJvcGVuaWQiLCJleGFtcGxlIl19.dK7S1sVmpc6-x3DASt22HXqw2BE_mqrr78xmznl-B7Yp4m0BJwpXi4YQes3zz-JpbZJ1mqdSz7utDskpZ6EUUVO5z9ftvxPfb3LvAOGsGUvL2no9I_2XD8vUrGqck3H9jOZhdv6iRbb-2HckozIAqUT-o1Bg4CYSP-OGtzCYPere0c7dCktxArlwMQ_6A7ydvSGUFnnj0PVlYhV98JPbw3JuC7XSv21vo5LSSAbXGefuKIQ6N9EoIzYnpNWenwe0Du2s7MwdDXSSOtrv2heIduf70LyaK-36N1kuVsah8-r0AWuHhv3KOVPEWfmB4nKLg2Klhn0h7WESXvLgh4rnEA';
const token1_expired = 'eyJhbGciOiJSUzI1NiJ9.eyJqdGkiOiIxM2I5ZTM0NC1iYzNiLTQwMTctYmQ4OC0wMWM5YjkwNTlhMzMiLCJzdWIiOiIxNmVjMTk0OC02ZTBiLTQzMGUtYmE4Yi1kMzQ1ZDI3MzQ0YzciLCJzY29wZSI6WyJleGFtcGxlLndyaXRlIiwiZXhhbXBsZS5yZWFkIiwib3BlbmlkIl0sImNsaWVudF9pZCI6ImV4YW1wbGUiLCJjaWQiOiJleGFtcGxlIiwiYXpwIjoiZXhhbXBsZSIsImdyYW50X3R5cGUiOiJhdXRob3JpemF0aW9uX2NvZGUiLCJ1c2VyX2lkIjoiMTZlYzE5NDgtNmUwYi00MzBlLWJhOGItZDM0NWQyNzM0NGM3Iiwib3JpZ2luIjoidWFhIiwidXNlcl9uYW1lIjoiZGVtbyIsImVtYWlsIjoiZGVtb0Bsb2NhbCIsImF1dGhfdGltZSI6MTQ2MTAzODQyNCwicmV2X3NpZyI6IjU2YjJiNGZiIiwiaWF0IjoxNDYxMDM4NDMzLCJleHAiOjE0NjEwMzg0MzQsImlzcyI6Imh0dHBzOi8vMDkwZTc1NjgtZWMxMS00MzE4LWIwMGEtMDQxNTc3NzgwZGZkLnByZWRpeC11YWEtc3RhZ2luZy5ncmMtYXBwcy5zdmMuaWNlLmdlLmNvbS9vYXV0aC90b2tlbiIsInppZCI6IjA5MGU3NTY4LWVjMTEtNDMxOC1iMDBhLTA0MTU3Nzc4MGRmZCIsImF1ZCI6WyJvcGVuaWQiLCJleGFtcGxlIl19.qHzUF9c3ws0DxEYsjEYpr0jV_qcxOC0I-Nyj_D8pl1_QOSvzVgx4aNjutcpxg5h9ZrSfErkDoWfR1W6qTh_vxoXDHmeSdSoWi4rciFQXn7iHcERAtT_Wj1rWMkvzpsx47qIjVuZAUXuNPEFT8myEePC2vJhgp1fsQHwB0N-mhQAADDdPnNeh5KhdFoqGmxRi8fJ1F9QcYV6FXHWdtnJAC-_RYgTw4NbrKPfYf3tzone0INxVsJr7xDhS3PeOP-lFywUJshwD-uqknydX7W-zRaD2Pxor95IjKTN9W8bbmcO5XPNJT-UGgL700h5wlnuUlUU4sG4zfgDc3iL_ugPuFQ';
const token1_tampered = 'eyJhbGciOiJSUzI1NiJ9.eyJqdGkiOiI3ZDE0ZDVmMS0xMmVhLTQyNGItODE5Yi1iNWViNTk2NTVhOWEiLCJzdWIiOiIxNmVjMTk0OC02ZTBiLTQzMGUtYmE4Yi1kMzQ1ZDI3MzQ0YzciLCJzY29wZSI6WyJleGFtcGxlLndyaXRlIiwiZXhhbXBsZS5yZWFkIiwiYWRtaW4iLCJvcGVuaWQiXSwiY2xpZW50X2lkIjoiZXhhbXBsZSIsImNpZCI6ImV4YW1wbGUiLCJhenAiOiJleGFtcGxlIiwiZ3JhbnRfdHlwZSI6ImF1dGhvcml6YXRpb25fY29kZSIsInVzZXJfaWQiOiIxNmVjMTk0OC02ZTBiLTQzMGUtYmE4Yi1kMzQ1ZDI3MzQ0YzciLCJvcmlnaW4iOiJ1YWEiLCJ1c2VyX25hbWUiOiJkZW1vIiwiZW1haWwiOiJkZW1vQGxvY2FsIiwiYXV0aF90aW1lIjoxNDYxMDM4MjU5LCJyZXZfc2lnIjoiNTZiMmI0ZmIiLCJpYXQiOjE0NjEwMzgyODQsImV4cCI6MzYwODUyMTkzMSwiaXNzIjoiaHR0cHM6Ly8wOTBlNzU2OC1lYzExLTQzMTgtYjAwYS0wNDE1Nzc3ODBkZmQucHJlZGl4LXVhYS1zdGFnaW5nLmdyYy1hcHBzLnN2Yy5pY2UuZ2UuY29tL29hdXRoL3Rva2VuIiwiemlkIjoiMDkwZTc1NjgtZWMxMS00MzE4LWIwMGEtMDQxNTc3NzgwZGZkIiwiYXVkIjpbIm9wZW5pZCIsImV4YW1wbGUiXX0.dK7S1sVmpc6-x3DASt22HXqw2BE_mqrr78xmznl-B7Yp4m0BJwpXi4YQes3zz-JpbZJ1mqdSz7utDskpZ6EUUVO5z9ftvxPfb3LvAOGsGUvL2no9I_2XD8vUrGqck3H9jOZhdv6iRbb-2HckozIAqUT-o1Bg4CYSP-OGtzCYPere0c7dCktxArlwMQ_6A7ydvSGUFnnj0PVlYhV98JPbw3JuC7XSv21vo5LSSAbXGefuKIQ6N9EoIzYnpNWenwe0Du2s7MwdDXSSOtrv2heIduf70LyaK-36N1kuVsah8-r0AWuHhv3KOVPEWfmB4nKLg2Klhn0h7WESXvLgh4rnEA';
const token_malformed = 'This is not a JWT';

const trusted_issuers = ['https://f1615979-2469-4402-9a6e-3699caa34987.predix-uaa-staging.grc-apps.svc.ice.ge.com/oauth/token', 'https://090e7568-ec11-4318-b00a-041577780dfd.predix-uaa-staging.grc-apps.svc.ice.ge.com/oauth/token'];
const trusted_issuers2 = ['https://30c5ac6b-20f2-4630-8889-5fbe75c0afea.predix-uaa-staging.grc-apps.svc.ice.ge.com/oauth/token'];

let reqStub;

// ====================================================
// MOCKS

beforeEach((done) => {
    // Mock out the get call for fetching the key
    reqStub = sinon.stub(request, 'get');
    reqStub.yields(null, { statusCode: 200 }, JSON.stringify({ value: key1 }));
    // Clean out any cached keys
    token_util.clearCache();
    done();
});

afterEach((done) => {
    request.get.restore();
    done();
});
 
// ====================================================
// TESTS

describe('#verify', () => {
    it('verify a token', (done) => {
        // Use a token that expires 68 years in future
        // It is valid and signed by the correct key
        token_util.verify(token1_valid, trusted_issuers).then((decoded) => {
            try {
                expect(reqStub.calledOnce, '/token_key called once').to.be.true;
                expect(reqStub.calledWith('https://090e7568-ec11-4318-b00a-041577780dfd.predix-uaa-staging.grc-apps.svc.ice.ge.com/token_key'), '/token_key at right URI').to.be.true;
                expect(decoded).to.exist;
                expect(decoded.user_name).to.equal('demo');
                done();
            } catch(e) {
                return done(e);
            }
        });
    });

    it('cache the key', (done) => {
        // Call verify twice.  It should not call request on the second attempt
        token_util.verify(token1_valid, trusted_issuers).then((decoded) => {
            try {
                expect(reqStub.calledOnce, '/token_key called only once').to.be.true;
                expect(decoded).to.exist;
                expect(decoded.user_name).to.equal('demo');
            } catch(e) {
                return done(e);
            }

            token_util.verify(token1_valid, trusted_issuers).then((decoded) => {
                try {
                    expect(reqStub.calledOnce, '/token_key called only once').to.be.true;
                    expect(decoded).to.exist;
                    expect(decoded.user_name).to.equal('demo');
                    done();
                } catch(e) {
                    return done(e);
                }
            });
        });
    });

    it('fail if unable to get the key', (done) => {
        // Mock out the get call for fetching the key to give an error
        request.get.restore();
        reqStub = sinon.stub(request, 'get');
        reqStub.yields(null, { statusCode: 404 }, JSON.stringify({ msg: 'nope' }));

        token_util.verify(token1_valid, trusted_issuers).then((decoded) => {
            done(new Error('Should fail if unable to get the key'));
        }).catch((err) => {
            // We expect an error here
            done();
        });
    });

    it('fail if no response getting the key', (done) => {
        // Mock out the get call for fetching the key to give an error
        request.get.restore();
        reqStub = sinon.stub(request, 'get');
        reqStub.yields(null, null, null);

        token_util.verify(token1_valid, trusted_issuers).then((decoded) => {
            done(new Error('Should fail no response getting the key'));
        }).catch((err) => {
            // We expect an error here
            done();
        });
    });

    it('fail expired token', (done) => {
        // Use a token that has already expired
        // Although it is valid and signed by the correct key, verify should fail
        token_util.verify(token1_expired, trusted_issuers).then((decoded) => {
            done(new Error('Should fail if token is expired'));
        }).catch((err) => {
            // We expect an error here
            try {
                expect(err.name).to.equal('TokenExpiredError');
                expect(err.message).to.equal('jwt expired');
                done();
            } catch(e) {
                return done(e);
            }
        });
    });

    it('fail a tampered token', (done) => {
        // Use a token that has been modified, verification should fail
        token_util.verify(token1_tampered, trusted_issuers).then((decoded) => {
            done(new Error('Should fail if token has been tampered with'));
        }).catch((err) => {
            // We expect an error here
            try {
                expect(err.name).to.equal('JsonWebTokenError');
                expect(err.message).to.equal('invalid signature');
                done();
            } catch(e) {
                return done(e);
            }
        });
    });

    it('fail a malformed token', (done) => {
        // Use something that is not a token, verification should fail
        token_util.verify(token_malformed, trusted_issuers).then((decoded) => {
            done(new Error('Should fail if token is not a token'));
        }).catch((err) => {
            // We expect an error here
            try {
                expect(err.name).to.equal('Error');
                expect(err.message).to.equal('Not a valid token');
                done();
            } catch(e) {
                return done(e);
            }
        });
    });

    it('fail a null token', (done) => {
        // Pass no token, verification should fail
        token_util.verify(null, trusted_issuers).then((decoded) => {
            done(new Error('Should fail if token is not supplied'));
        }).catch((err) => {
            // We expect an error here
            try {
                expect(err.name).to.equal('Error');
                expect(err.message).to.equal('Not a valid token');
                done();
            } catch(e) {
                return done(e);
            }
        });
    });

    it('fail signed with a different key', (done) => {
        // Mock out the get call for fetching the key to give an error
        request.get.restore();
        reqStub = sinon.stub(request, 'get');
        reqStub.yields(null, { statusCode: 200 }, JSON.stringify({ value: key2 }));

        // Using a key from another server, verification should fail
        token_util.verify(token1_valid, trusted_issuers).then((decoded) => {
            done(new Error('Should fail if token and key mismatch'));
        }).catch((err) => {
            // We expect an error here
            try {
                expect(err.name).to.equal('JsonWebTokenError');
                expect(err.message).to.equal('invalid signature');
                done();
            } catch(e) {
                return done(e);
            }
        });
    });

    it('fail if not a trusted issuer', (done) => {
        // If the issuer is not trusted, verification should fail
        token_util.verify(token1_valid, trusted_issuers2).then((decoded) => {
            done(new Error('Should fail if issuer is not trusted'));
        }).catch((err) => {
            // We expect an error here
            try {
                expect(err.name).to.equal('Error');
                expect(err.message).to.equal('Not a trusted issuer');
                done();
            } catch(e) {
                return done(e);
            }
        });
    });
});
