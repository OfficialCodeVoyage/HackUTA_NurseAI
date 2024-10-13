import { NextRequest } from "next/server.js";
import type { NextAuthConfig } from "./index.js";
/** If `NEXTAUTH_URL` or `AUTH_URL` is defined, override the request's URL. */
export declare function reqWithEnvURL(req: NextRequest): NextRequest;
/**
 * For backwards compatibility, `next-auth` checks for `NEXTAUTH_URL`
 * and the `basePath` by default is `/api/auth` instead of `/auth`
 * (which is the default for all other Auth.js integrations).
 *
 * For the same reason, `NEXTAUTH_SECRET` is also checked.
 */
export declare function setEnvDefaults(config: NextAuthConfig): void;
//# sourceMappingURL=env.d.ts.map