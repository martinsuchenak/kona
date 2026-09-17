// Bundle the extension for publishing.
//
// package.json declares `vscode-languageclient` as a runtime dependency, but
// the published vsix excludes node_modules, so the client has to be bundled
// into out/extension.js or activation fails with MODULE_NOT_FOUND.
const esbuild = require('esbuild');

const watch = process.argv.includes('--watch');
const production = process.argv.includes('--production');

const options = {
    entryPoints: ['src/extension.ts'],
    bundle: true,
    outfile: 'out/extension.js',
    // 'vscode' is provided by the host at runtime and must never be bundled.
    external: ['vscode'],
    format: 'cjs',
    platform: 'node',
    target: 'node18',
    sourcemap: !production,
    minify: production,
    logLevel: 'info',
};

async function main() {
    if (watch) {
        const ctx = await esbuild.context(options);
        await ctx.watch();
    } else {
        await esbuild.build(options);
    }
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});
