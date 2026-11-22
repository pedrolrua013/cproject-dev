// Recebe o formulário de diagnóstico e envia por e-mail para contato@cproject.com.br.
// Variáveis de ambiente (Vercel > Settings > Environment Variables):
//   SMTP_HOST (padrão smtp.hostinger.com), SMTP_PORT (padrão 465),
//   SMTP_USER (ex.: contato@cproject.com.br), SMTP_PASS, CONTACT_TO (padrão contato@cproject.com.br)
const nodemailer = require('nodemailer');

const LIMITES = {nome: 120, empresa: 120, segmento: 80, whatsapp: 20, busca: 2000};
const limpa = (v, max) => String(v ?? '').replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').trim().slice(0, max);

module.exports = async (req, res) => {
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return res.status(405).json({ok: false}); }
  const host = req.headers.host || '';
  const origem = req.headers.origin;
  if (origem && new URL(origem).host !== host) return res.status(403).json({ok: false});

  let b = req.body;
  if (typeof b === 'string') { try { b = JSON.parse(b); } catch { b = {}; } }
  b = b || {};
  if (b.site) return res.status(200).json({ok: true}); // honeypot: finge sucesso para robôs

  const d = Object.fromEntries(Object.entries(LIMITES).map(([k, max]) => [k, limpa(b[k], max)]));
  const digitos = d.whatsapp.replace(/\D/g, '');
  if (d.nome.length < 2 || d.empresa.length < 2 || !d.segmento || digitos.length < 10 || d.busca.length < 2) {
    return res.status(422).json({ok: false, erro: 'campos'});
  }
  if (!process.env.SMTP_USER || !process.env.SMTP_PASS) {
    console.error('diagnostico: SMTP_USER/SMTP_PASS não configurados');
    return res.status(500).json({ok: false});
  }

  const port = Number(process.env.SMTP_PORT || 465);
  const tx = nodemailer.createTransport({
    host: process.env.SMTP_HOST || 'smtp.hostinger.com', port, secure: port === 465,
    auth: {user: process.env.SMTP_USER, pass: process.env.SMTP_PASS},
  });
  const wa = 'https://wa.me/55' + digitos.replace(/^55(?=\d{10,11}$)/, '');
  const texto = [
    'Nova solicitação de diagnóstico gratuito pelo site:', '',
    `Nome: ${d.nome}`, `Empresa: ${d.empresa}`, `Segmento: ${d.segmento}`, `WhatsApp: ${d.whatsapp} (${wa})`, '',
    'O que busca:', d.busca,
  ].join('\n');

  try {
    await tx.sendMail({
      from: `"Site CProject Lab" <${process.env.SMTP_USER}>`,
      to: process.env.CONTACT_TO || 'contato@cproject.com.br',
      subject: `Diagnóstico gratuito · ${d.empresa} (${d.segmento})`.replace(/[\r\n]/g, ' '),
      text: texto,
    });
    return res.status(200).json({ok: true});
  } catch (e) {
    console.error('diagnostico: falha no envio', e.code || e.message);
    return res.status(502).json({ok: false});
  }
};
