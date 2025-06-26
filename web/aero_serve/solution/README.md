# OTP authentication bypass through improper session termination

Goal: is to login as user `admin` to get the flag  
[Solver script](solve.py)

## Understanding the Authentication Flow

When a user starts the authentication process, the username is sent through POST request to `/login` and he revices a session token in the cookie called `session` that if [decoded](https://www.kirsle.net/wizards/flask-session.cgi) contains the user to authenticate with.

```json
{"user":"Reddington"}
```

And after verifying the OTP a new session cookie is returned that now containes:

```json
{"user":"Reddington","autheticated":true}
```

## The Logout Vulnerability

Inspecting the logout functionality we notice that when we request a logout we revice a new sesssion cookie that only contains:

```json
{"autheticated":"true"}
```

Looks like we are still authenticated!!

To veirfy that by visitting `/home` we can see that it says "Welcome to AeroServe, None!" where `None` is supposed to be the username that does not exist anymore in the session.

Now we are **authenticated** but we need to find a way to set the user to admin in the session to trick the app into giving us the flag

## Exploiting the Session for Admin Access

Since we can achieve an "authenticated" state without an associated username, the next step is to inject the desired `admin` username into this authenticated session. This can be achieved by:

1.  **Logging out** to obtain a session cookie with `{"authenticated": true}`.
2.  **Sending a POST request to `/login` with the username `admin`**. Even though we are already "authenticated" (without a user), this request will update the session cookie, merging the newly provided username with the existing `authenticated: true` status.

The resulting session cookie will then be: `{"user": "admin", "authenticated": true}`.

## Obtaining the Flag

With the session now successfully manipulated to reflect an authenticated "admin" user, simply navigating to the `/home` endpoint will grant access to the flag.