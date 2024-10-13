"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "createEnvDefinitions", {
    enumerable: true,
    get: function() {
        return createEnvDefinitions;
    }
});
const _nodepath = require("node:path");
const _promises = require("node:fs/promises");
async function createEnvDefinitions({ distDir, env }) {
    const envKeysStr = Object.keys(env).map((key)=>`      ${key}?: string`).join('\n');
    const definitionStr = `// Type definitions for Next.js environment variables
declare global {
  namespace NodeJS {
    interface ProcessEnv {
${envKeysStr}
    }
  }
}
export {}`;
    if (process.env.NODE_ENV === 'test') {
        return definitionStr;
    }
    try {
        // we expect the types directory to already exist
        const envDtsPath = (0, _nodepath.join)(distDir, 'types', 'env.d.ts');
        // do not await, this is not essential for further process
        (0, _promises.writeFile)(envDtsPath, definitionStr, 'utf-8');
    } catch (e) {
        console.error('Failed to write env.d.ts:', e);
    }
}

//# sourceMappingURL=create-env-definitions.js.map