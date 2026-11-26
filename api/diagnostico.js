// Recebe o formulário do site e envia por e-mail para contato@cproject.com.br.
// Sem dependências: fala SMTP direto (o .vercelignore deixa o package.json fora da publicação).
// Sem SMTP configurado, envia pelo FormSubmit (formsubmit.co) para o mesmo e-mail. Na primeira vez o
// FormSubmit manda um e-mail de ativação para contato@cproject.com.br: é só clicar em "Activate Form".
// Variáveis de ambiente (Vercel > Settings > Environment Variables):
//   SMTP_USER (ex.: contato@cproject.com.br), SMTP_PASS,
//   opcionais: SMTP_HOST (padrão smtp.hostinger.com), SMTP_PORT (padrão 465), CONTACT_TO (padrão contato@cproject.com.br)
const tls = require('tls');
const net = require('net');

const LIMITES = {interesse: 80, nome: 120, empresa: 120, segmento: 80, whatsapp: 20, busca: 2000};
const limpa = (v, max) => String(v ?? '').replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').trim().slice(0, max);
const b64 = s => Buffer.from(s, 'utf8').toString('base64');

function smtpEnviar({host, port, secure, user, pass, from, to, subject, text}) {
  return new Promise((resolve, reject) => {
    const sock = secure ? tls.connect({host, port, servername: host}) : net.connect({host, port});
    sock.setTimeout(15000, () => { sock.destroy(); reject(new Error('timeout')); });
    sock.on('error', reject);
    let buf = '';
    const fila = [];
    sock.on('data', d => {
      buf += d.toString('utf8');
      let i;
      while ((i = buf.indexOf('\r\n')) >= 0) {
        const linha = buf.slice(0, i); buf = buf.slice(i + 2);
        if (/^\d{3} /.test(linha)) { const f = fila.shift(); if (f) f(linha); }
      }
    });
    const espera = () => new Promise(r => fila.push(r));
    const cmd = async (c, ok) => {
      const p = espera();
      if (c !== null) sock.write(c + '\r\n');
      const r = await p;
      if (!ok.includes(r.slice(0, 3))) throw new Error('SMTP ' + r.slice(0, 3));
      return r;
    };
    (async () => {
      await cmd(null, ['220']);
      await cmd('EHLO cproject.com.br', ['250']);
      await cmd('AUTH LOGIN', ['334']);
      await cmd(b64(user), ['334']);
      await cmd(b64(pass), ['235']);
      await cmd(`MAIL FROM:<${user}>`, ['250']);
      await cmd(`RCPT TO:<${to}>`, ['250', '251']);
      await cmd('DATA', ['354']);
      const corpo = b64(text).replace(/.{1,76}/g, '$&\r\n');
      const msg = [
        `From: ${from}`, `To: <${to}>`, `Subject: =?UTF-8?B?${b64(subject)}?=`,
        `Date: ${new Date().toUTCString()}`, `Message-ID: <${Date.now()}.${Math.random().toString(36).slice(2)}@cproject.com.br>`,
        'MIME-Version: 1.0', 'Content-Type: text/plain; charset=UTF-8', 'Content-Transfer-Encoding: base64', '', corpo,
      ].join('\r\n');
      await cmd(msg + '\r\n.', ['250']);
      sock.write('QUIT\r\n'); sock.end();
      resolve();
    })().catch(e => { sock.destroy(); reject(e); });
  });
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return res.status(405).json({ok: false}); }
  const origem = req.headers.origin;
  try { if (origem && new URL(origem).host !== (req.headers.host || '')) return res.status(403).json({ok: false}); }
  catch { return res.status(403).json({ok: false}); }

  let b = req.body;
  if (typeof b === 'string') { try { b = JSON.parse(b); } catch { b = {}; } }
  b = b || {};
  if (b.site) return res.status(200).json({ok: true}); // honeypot: finge sucesso para robôs

  const d = Object.fromEntries(Object.entries(LIMITES).map(([k, max]) => [k, limpa(b[k], max)]));
  const digitos = d.whatsapp.replace(/\D/g, '');
  if (d.nome.length < 2 || d.empresa.length < 2 || !d.segmento || digitos.length < 10 || d.busca.length < 2) {
    return res.status(422).json({ok: false, erro: 'campos'});
  }
  const user = process.env.SMTP_USER, pass = process.env.SMTP_PASS;
  const para = process.env.CONTACT_TO || 'contato@cproject.com.br';
  const assunto = `Site · ${d.interesse || 'Consultoria gratuita'} · ${d.empresa}`.replace(/[\r\n]/g, ' ');
  if (!user || !pass) {
    const wa0 = 'https://wa.me/55' + digitos.replace(/^55(?=\d{10,11}$)/, '');
    try {
      const r = await fetch('https://formsubmit.co/ajax/' + encodeURIComponent(para), {
        method: 'POST',
        headers: {'Content-Type': 'application/json', Accept: 'application/json', Origin: 'https://cproject.com.br', Referer: 'https://cproject.com.br/'},
        body: JSON.stringify({
          _subject: assunto, _template: 'table', _captcha: 'false',
          Interesse: d.interesse || 'Consultoria gratuita', Nome: d.nome, Empresa: d.empresa, Segmento: d.segmento,
          WhatsApp: `${d.whatsapp} (${wa0})`, 'O que busca': d.busca,
        }),
      });
      const j = await r.json().catch(() => ({}));
      if (r.ok && String(j.success) === 'true') return res.status(200).json({ok: true});
      console.error('diagnostico: formsubmit', r.status, j.message || '');
      return res.status(502).json({ok: false, erro: 'formsubmit', st: r.status, msg: j.message || ''});
    } catch (e) {
      console.error('diagnostico: formsubmit falhou', e.message);
      return res.status(502).json({ok: false});
    }
  }

  const port = Number(process.env.SMTP_PORT || 465);
  const wa = 'https://wa.me/55' + digitos.replace(/^55(?=\d{10,11}$)/, '');
  const texto = [
    'Novo contato pelo site:', '',
    `Interesse: ${d.interesse || 'Consultoria gratuita'}`,
    `Nome: ${d.nome}`, `Empresa: ${d.empresa}`, `Segmento: ${d.segmento}`, `WhatsApp: ${d.whatsapp} (${wa})`, '',
    'O que busca:', d.busca,
  ].join('\n');

  try {
    await smtpEnviar({
      host: process.env.SMTP_HOST || 'smtp.hostinger.com', port, secure: port === 465, user, pass,
      from: `"Site CProject Lab" <${user}>`,
      to: para,
      subject: assunto,
      text: texto,
    });
    return res.status(200).json({ok: true});
  } catch (e) {
    console.error('diagnostico: falha no envio', e.message);
    return res.status(502).json({ok: false});
  }
};
