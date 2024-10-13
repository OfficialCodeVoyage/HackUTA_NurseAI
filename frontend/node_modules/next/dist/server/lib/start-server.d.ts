import '../next';
import '../require-hook';
import type { SelfSignedCertificate } from '../../lib/mkcert';
import { initialize } from './router-server';
export interface StartServerOptions {
    dir: string;
    port: number;
    isDev: boolean;
    hostname?: string;
    allowRetry?: boolean;
    customServer?: boolean;
    minimalMode?: boolean;
    keepAliveTimeout?: number;
    selfSignedCertificate?: SelfSignedCertificate;
}
export declare function getRequestHandlers({ dir, port, isDev, onCleanup, server, hostname, minimalMode, keepAliveTimeout, experimentalHttpsServer, quiet, }: {
    dir: string;
    port: number;
    isDev: boolean;
    onCleanup: (listener: () => Promise<void>) => void;
    server?: import('http').Server;
    hostname?: string;
    minimalMode?: boolean;
    keepAliveTimeout?: number;
    experimentalHttpsServer?: boolean;
    quiet?: boolean;
}): ReturnType<typeof initialize>;
export declare function startServer(serverOptions: StartServerOptions): Promise<void>;
