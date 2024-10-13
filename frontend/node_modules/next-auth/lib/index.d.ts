import { type AuthConfig } from "@auth/core";
import { NextResponse } from "next/server.js";
import type { Awaitable, Session } from "@auth/core/types";
import type { GetServerSidePropsContext, NextApiRequest, NextApiResponse } from "next";
import type { AppRouteHandlerFn } from "./types.js";
import type { NextFetchEvent, NextMiddleware, NextRequest } from "next/server.js";
/** Configure NextAuth.js. */
export interface NextAuthConfig extends Omit<AuthConfig, "raw"> {
    /**
     * Callbacks are asynchronous functions you can use to control what happens when an auth-related action is performed.
     * Callbacks **allow you to implement access controls without a database** or to **integrate with external databases or APIs**.
     */
    callbacks?: AuthConfig["callbacks"] & {
        /**
         * Invoked when a user needs authorization, using [Middleware](https://nextjs.org/docs/advanced-features/middleware).
         *
         * You can override this behavior by returning a {@link NextResponse}.
         *
         * @example
         * ```ts title="app/auth.ts"
         * async authorized({ request, auth }) {
         *   const url = request.nextUrl
         *
         *   if(request.method === "POST") {
         *     const { authToken } = (await request.json()) ?? {}
         *     // If the request has a valid auth token, it is authorized
         *     const valid = await validateAuthToken(authToken)
         *     if(valid) return true
         *     return NextResponse.json("Invalid auth token", { status: 401 })
         *   }
         *
         *   // Logged in users are authenticated, otherwise redirect to login page
         *   return !!auth.user
         * }
         * ```
         *
         * :::warning
         * If you are returning a redirect response, make sure that the page you are redirecting to is not protected by this callback,
         * otherwise you could end up in an infinite redirect loop.
         * :::
         */
        authorized?: (params: {
            /** The request to be authorized. */
            request: NextRequest;
            /** The authenticated user or token, if any. */
            auth: Session | null;
        }) => Awaitable<boolean | NextResponse | Response | undefined>;
    };
}
export interface NextAuthRequest extends NextRequest {
    auth: Session | null;
}
export type NextAuthMiddleware = (request: NextAuthRequest, event: NextFetchEvent) => ReturnType<NextMiddleware>;
export type WithAuthArgs = [NextAuthRequest, any] | [NextAuthMiddleware] | [AppRouteHandlerFn] | [NextApiRequest, NextApiResponse] | [GetServerSidePropsContext] | [];
export declare function initAuth(config: NextAuthConfig | ((request: NextRequest | undefined) => NextAuthConfig), onLazyLoad?: (config: NextAuthConfig) => void): (...args: WithAuthArgs) => Promise<any> | ((...args: Parameters<NextAuthMiddleware | AppRouteHandlerFn>) => Promise<Response>);
//# sourceMappingURL=index.d.ts.map