const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require('@whiskeysockets/baileys');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

function escaparArg(str) {
    if (!str) return '';
    return String(str).replace(/"/g, '\\"');
}

async function iniciarBot() {
    const { state, saveCreds } = await useMultiFileAuthState('Qrcode_Sesion');

    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: false
    });

    sock.ev.on('creds.update', saveCreds);

    // --- BLOQUE DE CÓDIGO DE VINCULACIÓN ---
    if (!sock.authState.creds.registered) {
        const numeroLimpio = "5595984017858"; // Tu número sin + ni espacios
        console.log('🔄 Solicitando código de vinculación...');
        setTimeout(async () => {
            try {
                const code = await sock.requestPairingCode(numeroLimpio);
                console.log(`\n========================================`);
                console.log(`🔑 TU CÓDIGO DE VINCULACIÓN ES: ${code}`);
                console.log(`========================================\n`);
            } catch (err) {
                console.error('Error al generar código:', err.message);
            }
        }, 3000);
    }
    // ----------------------------------------

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect } = update;
        if (connection === 'close') {
            const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
            console.log(`⚠️ Conexión cerrada. ¿Reconectar?: ${shouldReconnect}`);
            if (shouldReconnect) iniciarBot();
        } else if (connection === 'open') {
            console.log('✅ ¡Bot Jasper conectado con éxito a WhatsApp!');
        }
    });

    sock.ev.on('messages.upsert', async ({ messages, type }) => {
        if (type !== 'notify') return;

        for (const msg of messages) {
            try {
                if (!msg.message || msg.key.fromMe) continue;

                const body = msg.message.conversation || 
                             msg.message.extendedTextMessage?.text || 
                             msg.message.imageMessage?.caption || '';
                
                const remoteJid = msg.key.remoteJid;
                const participant = msg.key.participant || remoteJid;

                if (!body || !body.startsWith('.')) continue;

                console.log(`📩 [IN] De: ${remoteJid} | User: ${participant} | Msg: ${body}`);

                const partes = body.trim().split(/\s+/);
                const comando = partes[0].toLowerCase();
                const parametro = partes.slice(1).join(' ');

                // Manejo de administración de grupos seguro
                if (remoteJid.endsWith('@g.us') && (comando === '.close' || comando === '.open')) {
                    try {
                        const groupMetadata = await sock.groupMetadata(remoteJid);
                        const participantes = groupMetadata.participants || [];
                        const esAdmin = participantes.some(p => p.id === participant && (p.admin === 'admin' || p.admin === 'superadmin'));

                        if (!esAdmin) {
                            await sock.sendMessage(remoteJid, { text: '⚠️ Solo los administradores pueden usar esto.' });
                            continue;
                        }
                        const estado = comando === '.close' ? 'announcement' : 'not_announcement';
                        await sock.groupSettingUpdate(remoteJid, estado);
                        await sock.sendMessage(remoteJid, { text: comando === '.close' ? '🔒 Grupo cerrado.' : '🔓 Grupo abierto.' });
                        continue;
                    } catch (err) {
                        console.error('Error admin group:', err.message);
                    }
                }

                // Ejecución protegida de Python con timeout de 10s
                const safeUser = escaparArg(participant);
                const safeCmd = escaparArg(comando);
                const safeParam = escaparArg(parametro);
                const comandoPython = `python3 bot.py "${safeUser}" "${safeCmd}" "${safeParam}"`;

                console.log(`🐍 [EXEC]: ${comandoPython}`);
                const { stdout, stderr } = await execPromise(comandoPython, { 
                    encoding: 'utf-8', 
                    timeout: 10000 
                });

                if (stderr) {
                    console.warn(`⚠️ [STDERR]: ${stderr.trim()}`);
                }

                const respuesta = stdout ? stdout.trim() : '';
                if (respuesta) {
                    console.log(`🚀 [RESPUESTA]: "${respuesta}"`);
                    await sock.sendMessage(remoteJid, { text: respuesta });
                } else {
                    console.log(`ℹ️ [INFO]: Python no devolvió texto.`);
                }

            } catch (loopErr) {
                console.error('❌ Error procesando mensaje individual:', loopErr.message);
            }
        }
    });
}

iniciarBot().catch(err => console.error('Error fatal al iniciar bot:', err));
