import type { BuiltInProviderType, RedirectableProviderType } from "@auth/core/providers";
import type { LiteralUnion, SignInAuthorizationParams, SignInOptions, SignInResponse } from "./lib/client.js";
/**
 * Initiate a signin flow or send the user to the signin page listing all possible providers.
 * Handles CSRF protection.
 */
export declare function signIn<P extends RedirectableProviderType | undefined = undefined>(provider?: LiteralUnion<P extends RedirectableProviderType ? P | BuiltInProviderType : BuiltInProviderType>, options?: SignInOptions, authorizationParams?: SignInAuthorizationParams): Promise<P extends RedirectableProviderType ? SignInResponse | undefined : undefined>;
//# sourceMappingURL=webauthn.d.ts.map