'use strict'
const chai = require('chai');
const expect = chai.expect;
const request = require('request');
const sinon = require('sinon');
const token_util = require('../index');

const key1 = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0m59l2u9iDnMbrXHfqkO\nrn2dVQ3vfBJqcDuFUK03d+1PZGbVlNCqnkpIJ8syFppW8ljnWweP7+LiWpRoz0I7\nfYb3d8TjhV86Y997Fl4DBrxgM6KTJOuE/uxnoDhZQ14LgOU2ckXjOzOdTsnGMKQB\nLCl0vpcXBtFLMaSbpv1ozi8h7DJyVZ6EnFQZUWGdgTMhDrmqevfx95U/16c5WBDO\nkqwIn7Glry9n9Suxygbf8g5AzpWcusZgDLIIZ7JTUldBb8qU2a0Dl4mvLZOn4wPo\njfj9Cw2QICsc5+Pwf21fP+hzf+1WSRHbnYv8uanRO0gZ8ekGaghM/2H6gqJbo2nI\nJwIDAQAB\n-----END PUBLIC KEY-----\n";
const key2 = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5VXMZBf2fUqNViwhkaKC\ntpnKX4MgKAcFA8KGiFYgChss8v/yB41wA8f+UfJmCOMIswRELKjHOp4tm9XtkCqy\nO/09RHqkrxG33za5tUhXSLaYX9MyMJcvbAXJ8cE9uu5Hv6Q4Gs65q/brwchh87Yb\nlCCvqGQ7QggEjqt2+bWGgjHDw9pKBXXRkA8t3fsH+sh2YgGCoRHH5Dd5QKpVkIGW\nnXlNIjRTd4g7rjE4Y3F1TaAhHpCoMOdviR++RIs3PdCi8ZUoS7V+mCWwOr61D7At\nxBjdnDDu/PZgLxlt1JEXt07V0xTzjztJ4r8qz5PkBZJeuZpHmiZoDNEquOhMQPhB\nIQIDAQAB\n-----END PUBLIC KEY-----\n"

const token1_valid = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiIwOTkxNTYzZjVjYTI0YjM5YjAxYzAzZjVlMTBmMTY0YiIsInN1YiI6IjMxZmJjZGU1LTc2NWUtNDA4ZS1hMjhjLTBhMjM0OTQ1YzkxYSIsInNjb3BlIjpbIm9wZW5pZCJdLCJjbGllbnRfaWQiOiJ0ZXN0IiwiY2lkIjoidGVzdCIsImF6cCI6InRlc3QiLCJncmFudF90eXBlIjoiYXV0aG9yaXphdGlvbl9jb2RlIiwidXNlcl9pZCI6IjMxZmJjZGU1LTc2NWUtNDA4ZS1hMjhjLTBhMjM0OTQ1YzkxYSIsIm9yaWdpbiI6InVhYSIsInVzZXJfbmFtZSI6InRlc3RlciIsImVtYWlsIjoidGVzdGVyQGRlbW8ubG9jYWwiLCJhdXRoX3RpbWUiOjE0NjM1ODE1NjQsInJldl9zaWciOiI4YTBkMzVjZSIsImlhdCI6MTQ2MzU4MTYxNSwiZXhwIjozNjExMDY1MjYyLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwODAvdWFhL29hdXRoL3Rva2VuIiwiemlkIjoidWFhIiwiYXVkIjpbInRlc3QiLCJvcGVuaWQiXX0.bG36YmWafz1B7ZH-kMX4Wh_xDRpwGUNYGn2Cizxr3ywmWE7gsupDrIpzmGnlG389IGzMGfqEb_nwtHT8mqhLpxN-IwT1SIz9qWDH4kt07qsJGWnzAIDH_fF6np_iMghz6JQJsLYG5rIKoR7ibNJl4xK6PhoIk4F7Rw2GuLcKuq9ILQRRAJTfuzZEBjVIwqTbDulXgOveCbagjPF455i_QxsxMzpq001nlCN6OfjCbNpPnLjpFUp4eZ3K-gGQfdLTxMEgjnfl7B-U45vtOPBJ0sXIXvfOUXWneSt6BkPka3GCcz3GdqmYDbNvsZD5IRyCDjQ0sZv7IHZHQf-vgLReLg';
const token1_expired = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiIwMzE1ZjFmYTFhOWE0MDFjOTc0Y2U0ZGUyMjA1MDQ5MiIsInN1YiI6IjMxZmJjZGU1LTc2NWUtNDA4ZS1hMjhjLTBhMjM0OTQ1YzkxYSIsInNjb3BlIjpbIm9wZW5pZCJdLCJjbGllbnRfaWQiOiJ0ZXN0IiwiY2lkIjoidGVzdCIsImF6cCI6InRlc3QiLCJncmFudF90eXBlIjoiYXV0aG9yaXphdGlvbl9jb2RlIiwidXNlcl9pZCI6IjMxZmJjZGU1LTc2NWUtNDA4ZS1hMjhjLTBhMjM0OTQ1YzkxYSIsIm9yaWdpbiI6InVhYSIsInVzZXJfbmFtZSI6InRlc3RlciIsImVtYWlsIjoidGVzdGVyQGRlbW8ubG9jYWwiLCJhdXRoX3RpbWUiOjE0NjM1ODE1NjQsInJldl9zaWciOiI4YTBkMzVjZSIsImlhdCI6MTQ2MzU4MTU3NiwiZXhwIjoxNDYzNTgxNTc3LCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwODAvdWFhL29hdXRoL3Rva2VuIiwiemlkIjoidWFhIiwiYXVkIjpbInRlc3QiLCJvcGVuaWQiXX0.pZIIZlKMmNeMz-Rh_np1Rfo3Cj-cFW9M6i5c9U6ZUHy1I2Xz7r6Esan-ED16yxpayYfCTE40s0ukSAFkqpxDO3gtmFjvZqIv-APclZXklIJthR8l8KgBkwZ2I5eGIi__qKl1ydkTmPke9qXyDqIQQnRnqoSzA5aI5rza9XDbT7rJwJCbhvGYpP2GQ2roapSweTkagTmrcgyhKWxf8NA36yQ4eFh_JZ4Qj8zHRWFU3PvdR812a7mvm8o6ECsIPqKwg10kXh61sjASoFsO6bxlw6dGgP8j5PrHfcWO74MYuGa1S1IaaeafHm2i29zJ2iBdNq3PCQuPrvxQdiFW_L7wdg';
const token1_tampered = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiIwOTkxNTYzZjVjYTI0YjM5YjAxYzAzZjVlMTBmMTY0YiIsInN1YiI6IjMxZmJjZGU1LTc2NWUtNDA4ZS1hMjhjLTBhMjM0OTQ1YzkxYSIsInNjb3BlIjpbIm9wZW5pZCIsImFkbWluIl0sImNsaWVudF9pZCI6InRlc3QiLCJjaWQiOiJ0ZXN0IiwiYXpwIjoidGVzdCIsImdyYW50X3R5cGUiOiJhdXRob3JpemF0aW9uX2NvZGUiLCJ1c2VyX2lkIjoiMzFmYmNkZTUtNzY1ZS00MDhlLWEyOGMtMGEyMzQ5NDVjOTFhIiwib3JpZ2luIjoidWFhIiwidXNlcl9uYW1lIjoidGVzdGVyIiwiZW1haWwiOiJ0ZXN0ZXJAZGVtby5sb2NhbCIsImF1dGhfdGltZSI6MTQ2MzU4MTU2NCwicmV2X3NpZyI6IjhhMGQzNWNlIiwiaWF0IjoxNDYzNTgxNjE1LCJleHAiOjM2MTEwNjUyNjIsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4MC91YWEvb2F1dGgvdG9rZW4iLCJ6aWQiOiJ1YWEiLCJhdWQiOlsidGVzdCIsIm9wZW5pZCJdfQ.bG36YmWafz1B7ZH-kMX4Wh_xDRpwGUNYGn2Cizxr3ywmWE7gsupDrIpzmGnlG389IGzMGfqEb_nwtHT8mqhLpxN-IwT1SIz9qWDH4kt07qsJGWnzAIDH_fF6np_iMghz6JQJsLYG5rIKoR7ibNJl4xK6PhoIk4F7Rw2GuLcKuq9ILQRRAJTfuzZEBjVIwqTbDulXgOveCbagjPF455i_QxsxMzpq001nlCN6OfjCbNpPnLjpFUp4eZ3K-gGQfdLTxMEgjnfl7B-U45vtOPBJ0sXIXvfOUXWneSt6BkPka3GCcz3GdqmYDbNvsZD5IRyCDjQ0sZv7IHZHQf-vgLReLg';
const token_malformed = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiIwOTkxNTYzZjVjYTI0YjM5YjAxYzAzZjVlMTBmMTY0YiIsInN1YiI6IjMxZmJjZGU1LTc2NWUtNDA4ZS1hMjhjLTBhMjM0OTQ1YzkxYSIsInNjb3BlIjpbIm9wZW5pZCJdLCJjbGllbnRfaWQiOjJ0ZXN0IiwiY2lkIjoidGVzdCIsImF6cCI6InRlc3QiLCJncmFudF90eXBlIjoiYXV0aG9yaXphdGlvbl9jb2RlIiwidXNlcl9pZCI6IjMxZmJjZGU1LTc2NWUtNDA4ZS1hMjhjLTBhMjM0OTQ1YzkxYSIsIm9yaWdpbiI6InVhYSIsInVzZXJfbmFtZSI6InRlc3RlciIsImVtYWlsIjoidGVzdGVyQGRlbW8ubG9jYWwiLCJhdXRoX3RpbWUiOjE0NjM1ODE1NjQsInJldl9zaWciOiI4YTBkMzVjZSIsImlhdCI6MTQ2MzU4MTYxNSwiZXhwIjozNjExMDY1MjYyLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwODAvdWFhL29hdXRoL3Rva2VuIiwiemlkIjoidWFhIiwiYXVkIjpbInRlc3QiLCJvcGVuaWQiXX0.EmHihs0D2OXg3bilcq0rH2Rd31BunqKDY9etUOZva1jyXhUe7Im79KmOqwFpMujTe4ONyN2rm70m8vhsJjfxBiS-n6-84ZJRKrN4FIIpil8gqQXNRUQSUn513lj0_suZAl5_4jxwrDyk1L00q3hdfHO2IP9hxcKiXp_jtRZlHumUpR0pG411gNMnZYxmrQio08prPGqcUA2LOLFHBtg6QVYF_Ho0jOBl4AAHqVxpMfPHHrOuX5aYhTXbp__3Gefsv44TmfNvzK_LnVtC5LWoCJvuiUhz45agkeMIR5NDsNc_cA7G148-TjwCYIfJFEUut6j2y4qNJSrum-J-1T7IYg';
const token_not_jwt = 'This is not a JWT';

const trusted_issuers = ['http://localhost:8080/uaa/oauth/token', 'https://uaa.example.com/oauth/token'];
const trusted_issuers2 = ['https://uaa.evil.gov/oauth/token'];

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
                expect(reqStub.calledWith('http://localhost:8080/uaa/token_key'), '/token_key at right URI').to.be.true;
                expect(decoded).to.exist;
                expect(decoded.user_name).to.equal('tester');
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
                expect(decoded.user_name).to.equal('tester');
            } catch(e) {
                return done(e);
            }

            token_util.verify(token1_valid, trusted_issuers).then((decoded) => {
                try {
                    expect(reqStub.calledOnce, '/token_key called only once').to.be.true;
                    expect(decoded).to.exist;
                    expect(decoded.user_name).to.equal('tester');
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

    it('fail a non JWT token', (done) => {
        // Use something that is not a token, verification should fail
        token_util.verify(token_not_jwt, trusted_issuers).then((decoded) => {
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
