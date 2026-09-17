import * as path from 'path';
import * as fs from 'fs';
import { ExtensionContext, extensions, workspace } from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions
} from 'vscode-languageclient/node';

let client: LanguageClient;

/**
 * Resolve the interpreter used to run the language server.
 *
 * Security: an interpreter found inside the opened workspace is only used when
 * the user has explicitly trusted that workspace. Preferring
 * `<workspaceFolder>/lsp-env/bin/python3` unconditionally meant that merely
 * opening an untrusted repository containing that path executed its binary.
 *
 * Preference order:
 *   1. the `kona.pythonPath` setting, if the user has set one
 *   2. the interpreter chosen in the Python extension
 *   3. the workspace's own lsp-env -- trusted workspaces only
 *   4. `python3` from PATH
 */
async function resolveInterpreter(): Promise<string> {
    const configured = workspace.getConfiguration('kona').get<string>('pythonPath');
    if (configured && configured.trim()) {
        return configured.trim();
    }

    const pythonApi = extensions.getExtension('ms-python.python');
    if (pythonApi) {
        try {
            const api = pythonApi.isActive ? pythonApi.exports : await pythonApi.activate();
            const details = api?.settings?.getExecutionDetails?.();
            const execCommand: string[] | undefined = details?.execCommand;
            if (execCommand && execCommand.length > 0) {
                return execCommand[0];
            }
        } catch {
            // Fall through to the remaining options.
        }
    }

    if (workspace.isTrusted && workspace.workspaceFolders?.length) {
        const wsPath = workspace.workspaceFolders[0].uri.fsPath;
        const localEnv = path.join(wsPath, 'lsp-env', 'bin', 'python3');
        if (fs.existsSync(localEnv)) {
            return localEnv;
        }
    }

    return 'python3';
}

export async function activate(context: ExtensionContext) {
    const pythonPath = await resolveInterpreter();

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
