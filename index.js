const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require('@whiskeysockets/baileys');
const { exec } = require('child_process');

async function iniciarBot() {
    const { state, saveCreds } = await useMultiFileAuthState('Qrcode_Sesion');

    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: false
    });

    sock.ev.on('creds.update', saveCreds);

    // --- BLOQUE DE CÓDIGO DE VINCULACIÓN ---
    if (!sock.authState.creds.registered) {
        const numeroLimpio = "TU_NUMERO_AQUI"; // Ej: "573000000000" (sin +, sin espacios)
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
            if (shouldReconnect) iniciarBot();
        } else if (connection === 'open') {
            console.log('✅ ¡Bot Japer conectado con éxito a WhatsApp!');
        }
    });

    sock.ev.on('messages.upsert', async (m) => {
        const msg = m.messages[0];
        if (!msg.message || msg.key.fromMe) return;

        const body = msg.message.conversation || msg.message.extendedTextMessage?.text || '';
        const remitente = msg.key.remoteJid;
        const usuarioId = msg.key.participant || remitente;

        if (!body.startsWith('.')) return;

        const partes = body.trim().split(/\s+/);
        const comando = partes[0].toLowerCase();
        const parametro = partes.slice(1).join(' ') || '';

        if (remitente.endsWith('@g.us') && (comando === '.close' || comando === '.open')) {
            try {
                const groupMetadata = await sock.groupMetadata(remitente);
                const participantes = groupMetadata.participants || [];
                const esAdmin = participantes.some(p => p.id === usuarioId && (p.admin === 'admin' || p.admin === 'superadmin'));

                if (!esAdmin) {
                    await sock.sendMessage(remitente, { text: '⚠️ Solo los administradores pueden usar esto.' }, { quoted: msg });
                    return;
                }
                const estado = comando === '.close' ? 'announcement' : 'not_announcement';
                await sock.groupSettingUpdate(remitente, estado);
                await sock.sendMessage(remitente, { text: comando === '.close' ? '🔒 Grupo cerrado.' : '🔓 Grupo abierto.' }, { quoted: msg });
                return;
            } catch (err) {
                console.error('Error admin:', err.message);
                return;
            }
        }

        const comandoPython = `python3 bot.py "${usuarioId}" "${comando}" "${parametro}"`;

        exec(comandoPython, { encoding: 'utf-8' }, async (error, stdout) => {
            if (error) {
                console.error(`Error ejecutando Python: ${error.message}`);
                return;
            }
            const respuesta = stdout.trim();
            if (respuesta) {
                try {
                    await sock.sendMessage(remitente, { text: respuesta }, { quoted: msg });
                } catch (sendErr) {
                    console.error('Error enviando a WhatsApp:', sendErr.message);
                }
            }
        });
    });
}

iniciarBot();
