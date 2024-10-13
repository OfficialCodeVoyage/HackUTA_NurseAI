import type { Env } from '@next/env';
export declare function createEnvDefinitions({ distDir, env, }: {
    distDir: string;
    env: Env;
}): Promise<string | undefined>;
