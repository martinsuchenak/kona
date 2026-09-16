import * as path from 'path';
import { ExtensionContext } from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions
} from 'vscode-languageclient/node';

let client: LanguageClient;

export function activate(context: ExtensionContext) {
    // We assume lsp-env/bin/python is available in the workspace root
    // For a production extension, you would package this or use the system python.
    const pythonPath = context.asAbsolutePath(path.join('lsp-env', 'bin', 'python3'));
    const serverScript = context.asAbsolutePath('kona_lsp.py');

    const serverOptions: ServerOptions = {
        run: { command: pythonPath, args: [serverScript] },
        debug: { command: pythonPath, args: [serverScript] }
    };

    const clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'kona' }]
    };

    client = new LanguageClient(
        'konaLanguageServer',
        'Kona Language Server',
        serverOptions,
        clientOptions
    );

    client.start();
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}
