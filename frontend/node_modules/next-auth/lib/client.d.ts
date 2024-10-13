import * as React from "react";
import type { BuiltInProviderType, ProviderType } from "@auth/core/providers";
import type { Session } from "@auth/core/types";
import { AuthError } from "@auth/core/errors";
/** @todo */
export declare class ClientSessionError extends AuthError {
}
export interface AuthClientConfig {
    baseUrl: string;
    basePath: string;
    baseUrlServer: string;
    basePathServer: string;
    /** Stores last session response */
    _session?: Session | null | undefined;
    /** Used for timestamp since last sycned (in seconds) */
    _lastSync: number;
    /**
     * Stores the `SessionProvider`'s session update method to be able to
     * trigger session updates from places like `signIn` or `signOut`
     */
    _getSession: (...args: any[]) => any;
}
export interface UseSessionOptions<R extends boolean> {
    required: R;
    /** Defaults to `signIn` */
    onUnauthenticated?: () => void;
}
export type LiteralUnion<T extends U, U = string> = T | (U & Record<never, never>);
export interface ClientSafeProvider {
    id: LiteralUnion<BuiltInProviderType>;
    name: string;
    type: ProviderType;
    signinUrl: string;
    callbackUrl: string;
}
export interface SignInOptions extends Record<string, unknown> {
    /**
     * Specify to which URL the user will be redirected after signing in. Defaults to the page URL the sign-in is initiated from.
     *
     * [Documentation](https://next-auth.js.org/getting-started/client#specifying-a-callbackurl)
     */
    callbackUrl?: string;
    /** [Documentation](https://next-auth.js.org/getting-started/client#using-the-redirect-false-option) */
    redirect?: boolean;
}
export interface SignInResponse {
    error: string | undefined;
    code: string | undefined;
    status: number;
    ok: boolean;
    url: string | null;
}
/** [Documentation](https://next-auth.js.org/getting-started/client#using-the-redirect-false-option-1) */
export interface SignOutResponse {
    url: string;
}
export interface SignOutParams<R extends boolean = true> {
    /** [Documentation](https://next-auth.js.org/getting-started/client#specifying-a-callbackurl-1) */
    callbackUrl?: string;
    /** [Documentation](https://next-auth.js.org/getting-started/client#using-the-redirect-false-option-1 */
    redirect?: R;
}
/**
 
 * If you have session expiry times of 30 days (the default) or more, then you probably don't need to change any of the default options.
 *
 * However, if you need to customize the session behavior and/or are using short session expiry times, you can pass options to the provider to customize the behavior of the {@link useSession} hook.
 */
export interface SessionProviderProps {
    children: React.ReactNode;
    session?: Session | null;
    baseUrl?: string;
    basePath?: string;
    /**
     * A time interval (in seconds) after which the session will be re-fetched.
     * If set to `0` (default), the session is not polled.
     */
    refetchInterval?: number;
    /**
     * `SessionProvider` automatically refetches the session when the user switches between windows.
     * This option activates this behaviour if set to `true` (default).
     */
    refetchOnWindowFocus?: boolean;
    /**
     * Set to `false` to stop polling when the device has no internet access offline (determined by `navigator.onLine`)
     *
     * [`navigator.onLine` documentation](https://developer.mozilla.org/en-US/docs/Web/API/NavigatorOnLine/onLine)
     */
    refetchWhenOffline?: false;
}
//# sourceMappingURL=client.d.ts.map