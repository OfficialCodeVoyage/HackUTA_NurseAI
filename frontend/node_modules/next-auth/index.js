/**
 * _If you are looking to migrate from v4, visit the [Upgrade Guide (v5)](https://authjs.dev/getting-started/migrating-to-v5)._
 *
 * ## Installation
 *
 * ```bash npm2yarn
 * npm install next-auth@beta
 * ```
 *
 * ## Environment variable inference
 *
 * `NEXTAUTH_URL` and `NEXTAUTH_SECRET` have been inferred since v4.
 *
 * Since NextAuth.js v5 can also automatically infer environment variables that are prefixed with `AUTH_`.
 *
 * For example `AUTH_GITHUB_ID` and `AUTH_GITHUB_SECRET` will be used as the `clientId` and `clientSecret` options for the GitHub provider.
 *
 * :::tip
 * The environment variable name inferring has the following format for OAuth providers: `AUTH_{PROVIDER}_{ID|SECRET}`.
 *
 * `PROVIDER` is the uppercase snake case version of the provider's id, followed by either `ID` or `SECRET` respectively.
 * :::
 *
 * `AUTH_SECRET` and `AUTH_URL` are also aliased for `NEXTAUTH_SECRET` and `NEXTAUTH_URL` for consistency.
 *
 * To add social login to your app, the configuration becomes:
 *
 * ```ts title="auth.ts"
 * import NextAuth from "next-auth"
 * import GitHub from "next-auth/providers/github"
 * export const { handlers, auth } = NextAuth({ providers: [ GitHub ] })
 * ```
 *
 * And the `.env.local` file:
 *
 * ```sh title=".env.local"
 * AUTH_GITHUB_ID=...
 * AUTH_GITHUB_SECRET=...
 * AUTH_SECRET=...
 * ```
 *
 * :::tip
 * In production, `AUTH_SECRET` is a required environment variable - if not set, NextAuth.js will throw an error. See [MissingSecretError](https://authjs.dev/reference/core/errors#missingsecret) for more details.
 * :::
 *
 * If you need to override the default values for a provider, you can still call it as a function `GitHub({...})` as before.
 *
 * ## Lazy initialization
 * You can also initialize NextAuth.js lazily (previously known as advanced intialization), which allows you to access the request context in the configuration in some cases, like Route Handlers, Middleware, API Routes or `getServerSideProps`.
 * The above example becomes:
 *
 * ```ts title="auth.ts"
 * import NextAuth from "next-auth"
 * import GitHub from "next-auth/providers/github"
 * export const { handlers, auth } = NextAuth(req => {
 *  if (req) {
 *   console.log(req) // do something with the request
 *  }
 *  return { providers: [ GitHub ] }
 * })
 * ```
 *
 * :::tip
 * This is useful if you want to customize the configuration based on the request, for example, to add a different provider in staging/dev environments.
 * :::
 *
 * @module next-auth
 */
import { Auth } from "@auth/core";
import { reqWithEnvURL, setEnvDefaults } from "./lib/env.js";
import { initAuth } from "./lib/index.js";
import { signIn, signOut, update } from "./lib/actions.js";
export { AuthError, CredentialsSignin } from "@auth/core/errors";
/**
 *  Initialize NextAuth.js.
 *
 *  @example
 * ```ts title="auth.ts"
 * import NextAuth from "next-auth"
 * import GitHub from "@auth/core/providers/github"
 *
 * export const { handlers, auth } = NextAuth({ providers: [GitHub] })
 * ```
 *
 * Lazy initialization:
 *
 * @example
 * ```ts title="auth.ts"
 * import NextAuth from "next-auth"
 * import GitHub from "@auth/core/providers/github"
 *
 * export const { handlers, auth } = NextAuth((req) => {
 *   console.log(req) // do something with the request
 *   return {
 *     providers: [GitHub],
 *   },
 * })
 * ```
 */
export default function NextAuth(config) {
    if (typeof config === "function") {
        const httpHandler = (req) => {
            const _config = config(req);
            setEnvDefaults(_config);
            return Auth(reqWithEnvURL(req), _config);
        };
        return {
            handlers: { GET: httpHandler, POST: httpHandler },
            // @ts-expect-error
            auth: initAuth(config, (c) => setEnvDefaults(c)),
            signIn: (provider, options, authorizationParams) => {
                const _config = config(undefined);
                setEnvDefaults(_config);
                return signIn(provider, options, authorizationParams, _config);
            },
            signOut: (options) => {
                const _config = config(undefined);
                setEnvDefaults(_config);
                return signOut(options, _config);
            },
            unstable_update: (data) => {
                const _config = config(undefined);
                setEnvDefaults(_config);
                return update(data, _config);
            },
        };
    }
    setEnvDefaults(config);
    const httpHandler = (req) => Auth(reqWithEnvURL(req), config);
    return {
        handlers: { GET: httpHandler, POST: httpHandler },
        // @ts-expect-error
        auth: initAuth(config),
        signIn: (provider, options, authorizationParams) => {
            return signIn(provider, options, authorizationParams, config);
        },
        signOut: (options) => {
            return signOut(options, config);
        },
        unstable_update: (data) => {
            return update(data, config);
        },
    };
}
