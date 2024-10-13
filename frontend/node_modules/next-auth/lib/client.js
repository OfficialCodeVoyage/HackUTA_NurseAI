"use client";
import * as React from "react";
import { AuthError } from "@auth/core/errors";
/** @todo */
class ClientFetchError extends AuthError {
}
/** @todo */
export class ClientSessionError extends AuthError {
}
// ------------------------ Internal ------------------------
/**
 * If passed 'appContext' via getInitialProps() in _app.js
 * then get the req object from ctx and use that for the
 * req value to allow `fetchData` to
 * work seemlessly in getInitialProps() on server side
 * pages *and* in _app.js.
 * @internal
 */
export async function fetchData(path, __NEXTAUTH, logger, req = {}) {
    const url = `${apiBaseUrl(__NEXTAUTH)}/${path}`;
    try {
        const options = {
            headers: {
                "Content-Type": "application/json",
                ...(req?.headers?.cookie ? { cookie: req.headers.cookie } : {}),
            },
        };
        if (req?.body) {
            options.body = JSON.stringify(req.body);
            options.method = "POST";
        }
        const res = await fetch(url, options);
        const data = await res.json();
        if (!res.ok)
            throw data;
        return data;
    }
    catch (error) {
        logger.error(new ClientFetchError(error.message, error));
        return null;
    }
}
/** @internal */
export function apiBaseUrl(__NEXTAUTH) {
    if (typeof window === "undefined") {
        // Return absolute path when called server side
        return `${__NEXTAUTH.baseUrlServer}${__NEXTAUTH.basePathServer}`;
    }
    // Return relative path when called client side
    return __NEXTAUTH.basePath;
}
/** @internal  */
export function useOnline() {
    const [isOnline, setIsOnline] = React.useState(typeof navigator !== "undefined" ? navigator.onLine : false);
    const setOnline = () => setIsOnline(true);
    const setOffline = () => setIsOnline(false);
    React.useEffect(() => {
        window.addEventListener("online", setOnline);
        window.addEventListener("offline", setOffline);
        return () => {
            window.removeEventListener("online", setOnline);
            window.removeEventListener("offline", setOffline);
        };
    }, []);
    return isOnline;
}
/**
 * Returns the number of seconds elapsed since January 1, 1970 00:00:00 UTC.
 * @internal
 */
export function now() {
    return Math.floor(Date.now() / 1000);
}
/**
 * Returns an `URL` like object to make requests/redirects from server-side
 * @internal
 */
export function parseUrl(url) {
    const defaultUrl = new URL("http://localhost:3000/api/auth");
    if (url && !url.startsWith("http")) {
        url = `https://${url}`;
    }
    const _url = new URL(url || defaultUrl);
    const path = (_url.pathname === "/" ? defaultUrl.pathname : _url.pathname)
        // Remove trailing slash
        .replace(/\/$/, "");
    const base = `${_url.origin}${path}`;
    return {
        origin: _url.origin,
        host: _url.host,
        path,
        base,
        toString: () => base,
    };
}
