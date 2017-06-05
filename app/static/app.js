var auth = new auth0.WebAuth({
    domain: AUTH0_DOMAIN,
    clientID: AUTH0_CLIENT_ID
});

function auth0Login(e) {
    e.preventDefault();
    auth.authorize({
        scope: 'openid profile',
        responseType: 'code',
        redirectUri: AUTH0_CALLBACK_URL,
        state: STATE
    });
};

function auth0Logout(e) {
    window.location = '/?logout';
};

// see https://github.com/morteza/bootstrap-rtl/issues/125
$(function() {
    window.scrollBy(0, 1);
    window.scrollBy(0, -1);
    $("body").show();
});