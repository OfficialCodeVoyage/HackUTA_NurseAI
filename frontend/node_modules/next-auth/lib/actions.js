import { Auth, raw, skipCSRFCheck, createActionURL } from "@auth/core";
import { headers as nextHeaders, cookies } from "next/headers.js";
import { redirect } from "next/navigation.js";
export async function signIn(provider, options = {}, authorizationParams, config) {
    const headers = new Headers(nextHeaders());
    const { redirect: shouldRedirect = true, redirectTo, ...rest } = options instanceof FormData ? Object.fromEntries(options) : options;
    const callbackUrl = redirectTo?.toString() ?? headers.get("Referer") ?? "/";
    const signInURL = createActionURL("signin", 
    // @ts-expect-error `x-forwarded-proto` is not nullable, next.js sets it by default
    headers.get("x-forwarded-proto"), headers, process.env, config.basePath);
    if (!provider) {
        signInURL.searchParams.append("callbackUrl", callbackUrl);
        if (shouldRedirect)
            redirect(signInURL.toString());
        return signInURL.toString();
    }
    let url = `${signInURL}/${provider}?${new URLSearchParams(authorizationParams)}`;
    let foundProvider = {};
    for (const providerConfig of config.providers) {
        const { options, ...defaults } = typeof providerConfig === "function" ? providerConfig() : providerConfig;
        const id = options?.id ?? defaults.id;
        if (id === provider) {
            foundProvider = {
                id,
                type: options?.type ?? defaults.type,
            };
            break;
        }
    }
    if (!foundProvider.id) {
        const url = `${signInURL}?${new URLSearchParams({ callbackUrl })}`;
        if (shouldRedirect)
            redirect(url);
        return url;
    }
    if (foundProvider.type === "credentials") {
        url = url.replace("signin", "callback");
    }
    headers.set("Content-Type", "application/x-www-form-urlencoded");
    const body = new URLSearchParams({ ...rest, callbackUrl });
    const req = new Request(url, { method: "POST", headers, body });
    const res = await Auth(req, { ...config, raw, skipCSRFCheck });
    for (const c of res?.cookies ?? [])
        cookies().set(c.name, c.value, c.options);
    const responseUrl = res instanceof Response ? res.headers.get("Location") : res.redirect;
    // NOTE: if for some unexpected reason the responseUrl is not set,
    // we redirect to the original url
    const redirectUrl = responseUrl ?? url;
    if (shouldRedirect)
        return redirect(redirectUrl);
    return redirectUrl;
}
export async function signOut(options, config) {
    const headers = new Headers(nextHeaders());
    headers.set("Content-Type", "application/x-www-form-urlencoded");
    const url = createActionURL("signout", 
    // @ts-expect-error `x-forwarded-proto` is not nullable, next.js sets it by default
    headers.get("x-forwarded-proto"), headers, process.env, config.basePath);
    const callbackUrl = options?.redirectTo ?? headers.get("Referer") ?? "/";
    const body = new URLSearchParams({ callbackUrl });
    const req = new Request(url, { method: "POST", headers, body });
    const res = await Auth(req, { ...config, raw, skipCSRFCheck });
    for (const c of res?.cookies ?? [])
        cookies().set(c.name, c.value, c.options);
    if (options?.redirect ?? true)
        return redirect(res.redirect);
    return res;
}
export async function update(data, config) {
    const headers = new Headers(nextHeaders());
    headers.set("Content-Type", "application/json");
    const url = createActionURL("session", 
    // @ts-expect-error `x-forwarded-proto` is not nullable, next.js sets it by default
    headers.get("x-forwarded-proto"), headers, process.env, config.basePath);
    const body = JSON.stringify({ data });
    const req = new Request(url, { method: "POST", headers, body });
    const res = await Auth(req, { ...config, raw, skipCSRFCheck });
    for (const c of res?.cookies ?? [])
        cookies().set(c.name, c.value, c.options);
    return res.body;
}
