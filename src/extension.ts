import * as path from 'path';
import * as fs from 'fs';
import { ExtensionContext, workspace } from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions
} from 'vscode-languageclient/node';

let client: LanguageClient;

export function activate(context: ExtensionContext) {
    let pythonPath = 'python3'; // Fallback to system python
    
    // Attempt to use the local workspace lsp-env if it exists
    if (workspace.workspaceFolders && workspace.workspaceFolders.length > 0) {
        const wsPath = workspace.workspaceFolders[0].uri.fsPath;
        const localEnv = path.join(wsPath, 'lsp-env', 'bin', 'python3');
        if (fs.existsSync(localEnv)) {
            pythonPath = localEnv;
        }
    }

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
