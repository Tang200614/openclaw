'use strict';

/**
 * Temporary compatibility shim for openclaw-lark versions that construct the
 * Feishu WSClient without wsConfig.pingTimeout.  The upstream SDK watchdog is
 * disabled when pingTimeout is omitted, so a silently half-open connection can
 * remain "connected" while no events are delivered.  This preload wraps the
 * SDK constructor and supplies a 150-second timeout unless the plugin already
 * provides one.
 *
 * Remove this shim after the upstream openclaw-lark liveness fix is included in
 * the installed plugin version.
 */

const fs = require('node:fs');
const path = require('node:path');
const { createRequire } = require('node:module');

const PING_TIMEOUT_SECONDS = 150;
const home = process.env.HOME || process.env.USERPROFILE || 'C:\\Users\\Administrator';
const openClawHome = path.join(home, '.openclaw');

const pluginCandidates = [
  path.join(openClawHome, 'extensions', 'openclaw-lark'),
  path.join(home, 'AppData', 'Local', 'Programs', 'nodejs', 'node_modules', 'openclaw', 'extensions', 'openclaw-lark'),
  path.join(home, 'AppData', 'Roaming', 'npm', 'node_modules', 'openclaw', 'extensions', 'openclaw-lark'),
];

let patchedCount = 0;

for (const pluginDirectory of [...new Set(pluginCandidates)]) {
  const packageJsonPath = path.join(pluginDirectory, 'package.json');
  if (!fs.existsSync(packageJsonPath)) continue;

  try {
    const localRequire = createRequire(packageJsonPath);
    const sdk = localRequire('@larksuiteoapi/node-sdk');
    const OriginalWSClient = sdk.WSClient;

    if (typeof OriginalWSClient !== 'function') continue;
    if (OriginalWSClient.__openclawLivenessWrapped) {
      patchedCount += 1;
      continue;
    }

    class LivenessWSClient extends OriginalWSClient {
      constructor(options = {}) {
        const existingWsConfig = options.wsConfig || {};
        super({
          ...options,
          wsConfig: {
            ...existingWsConfig,
            pingTimeout: existingWsConfig.pingTimeout || PING_TIMEOUT_SECONDS,
          },
        });
      }
    }

    Object.defineProperty(LivenessWSClient, '__openclawLivenessWrapped', {
      value: true,
      enumerable: false,
    });

    Object.defineProperty(sdk, 'WSClient', {
      value: LivenessWSClient,
      writable: true,
      enumerable: true,
      configurable: true,
    });

    patchedCount += 1;
  } catch (error) {
    process.stderr.write(
      `[feishu-liveness] Could not patch ${pluginDirectory}: ${error instanceof Error ? error.message : String(error)}\n`,
    );
  }
}

if (patchedCount > 0) {
  process.stderr.write(
    `[feishu-liveness] WSClient watchdog active (${PING_TIMEOUT_SECONDS}s) for ${patchedCount} installation(s).\n`,
  );
}
