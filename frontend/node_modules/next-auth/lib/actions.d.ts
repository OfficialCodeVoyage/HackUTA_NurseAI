import type { NextAuthConfig } from "./index.js";
import type { NextAuthResult, Session } from "../index.js";
type SignInParams = Parameters<NextAuthResult["signIn"]>;
export declare function signIn(provider: SignInParams[0], options: FormData | ({
    redirectTo?: string | undefined;
    redirect?: boolean | undefined;
} & Record<string, any>) | undefined, authorizationParams: SignInParams[2], config: NextAuthConfig): Promise<any>;
type SignOutParams = Parameters<NextAuthResult["signOut"]>;
export declare function signOut(options: SignOutParams[0], config: NextAuthConfig): Promise<any>;
type UpdateParams = Parameters<NextAuthResult["unstable_update"]>;
export declare function update(data: UpdateParams[0], config: NextAuthConfig): Promise<Session | null>;
export {};
//# sourceMappingURL=actions.d.ts.map