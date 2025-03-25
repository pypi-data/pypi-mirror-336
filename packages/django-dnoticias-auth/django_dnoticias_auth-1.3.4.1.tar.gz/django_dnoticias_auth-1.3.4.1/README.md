=====
dnoticias_auth
=====

dnoticias_auth is a Django app to make the authentication in the DNOTICIAS PLATFORMS.

Quick start
-----------

1. Add "dnoticias_auth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'dnoticias_auth',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('auth/', include('dnoticias_auth.urls')),

3. Run ``python manage.py migrate`` to create the dnoticias_auth models.

4. Add the necessary settings variables

5. Add the following middleware:

```
MIDDLEWARE = [
    ...
    'dnoticias_auth.middleware.LoginMiddleware',
    'mozilla_django_oidc.middleware.SessionRefresh',
    'dnoticias_auth.middleware.TokenMiddleware',
]
```
LoginMiddleware is a preprocessor that will see the cookies and simulate an OIDC login action, this needs to be before mozilla SessionRefresh.

TokenMiddleware is a posprocessor that will take the session variables (if the user is logged in) and put them into cookies. This is used in another clients on the LoginMiddleware

## Middleware

### LoginMiddleware
This will check if the keycloak session id match with any key on redis session, if it matches, then
will try to log in the user using the data saved in session.

### TokenMiddleware
The TokenMiddleware have two responsabilities right now.

The first one is to check if the actual session_id matches with any user logged in on the old DCS system, if it matches, then will show a page to update the user password.

The second and last one is to generate the next_url and the keycloak_session_id cookies if they dont exist on cookie but exist on session.

### SessionRefresh
This was extended to overwrite the 'is_refreshable_url' method.

## Redis sessions
To obtain a proper integration between the modules (editions, subscriptions, comments, etc.) our session engine is on redis, and all the modules share the same session engine. This basically allow us to access to the session data in a more easy way and without using cookies for that (only to save the keycloak session id).

The redis integration has the following workflow:

On user login -> LoginCallbackView -> Create session entries on redis

On page load -> Retrieve keycloak_session_id from cookie -> Search the session data on redis using the keycloak_session_id -> Load the session data or do nothing

On user logout -> Delete all the used cookies and session entries on redis database

Each session generates two entries on redis.

**session:XYZ** Contains the current session data for a specific module where XYZ = session id on Django.
**session_dj:ABC** Contains the session data and the matching session django session ids associated to this keycloak session where ABC is the keycloak session id

The session is stored with the following structure:

```js
{
    "sessions": "ABC,DEF,GHI,JKL",  // Comma-separated django sessions associated to this keycloak session
    "payload": {  // Payload used to process the user
        ...
    }
}
```


## Settings variables

| Setting  | Default value | Description |
| ------------- | ------------- | ------------- |
| OIDC_STORE_ACCESS_TOKEN  | True | OIDC store access token in session (TRUE ONLY) |
| OIDC_STORE_ID_TOKEN  | True | OIDC store id token in session (TRUE ONLY) |
| AUTH_COOKIE_EXPIRATION_MINUTES  | 15 | Cookie expiration time |
| AUTH_COOKIE_DOMAIN  | dnoticias.pt | Cookie domain |
| AUTH_COOKIE_SECURE  | True | Secure cookie in HTTPS only |
| AUTH_COOKIE_HTTPONLY  | True | Prevents changes from JS |
