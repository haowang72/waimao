// Cloudflare Pages Function: receive contact/inquiry form posts and forward to
// a WeCom (企业微信) group robot webhook. No external server required.
//
// Required environment variable (set in Cloudflare Pages dashboard ->
// Settings -> Environment variables, Production):
//   WECOM_WEBHOOK = https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=XXXX
//
// If the variable is not set (or the push fails), the function returns a
// non-2xx status so the front-end automatically falls back to mailto.

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function buildMessage(d) {
  const lines = ['### 📩 New enquiry · Baizly website'];
  if (d.name) lines.push(`**Name:** ${esc(d.name)}`);
  if (d.company) lines.push(`**Company:** ${esc(d.company)}`);
  if (d.country) lines.push(`**Country / port:** ${esc(d.country)}`);
  if (d.email) lines.push(`**Email:** ${esc(d.email)}`);
  if (d.contact) lines.push(`**WhatsApp / phone:** ${esc(d.contact)}`);
  if (d.model) lines.push(`**Model:** ${esc(d.model)}`);
  if (d.quantity) lines.push(`**Quantity:** ${esc(d.quantity)}`);
  if (d.list) lines.push(`**List:**\n${esc(d.list)}`);
  if (d.notes) lines.push(`**Notes:** ${esc(d.notes)}`);
  lines.push(`\n> Received: ${new Date().toISOString()}`);
  return lines.join('\n');
}

export async function onRequest(context) {
  const { request, env } = context;

  if (request.method !== 'POST') {
    return new Response('Method Not Allowed', { status: 405 });
  }

  let data;
  try {
    data = await request.json();
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, error: 'bad_json' }), {
      status: 400,
      headers: { 'content-type': 'application/json' },
    });
  }

  // Honeypot: hidden field real users never fill. Pretend success to the bot.
  if (data.website && String(data.website).trim() !== '') {
    return new Response(JSON.stringify({ ok: true }), {
      status: 200,
      headers: { 'content-type': 'application/json' },
    });
  }

  // Need at least one reply channel.
  const hasContact = (data.email && String(data.email).trim()) ||
    (data.contact && String(data.contact).trim());
  if (!hasContact) {
    return new Response(JSON.stringify({ ok: false, error: 'missing_contact' }), {
      status: 422,
      headers: { 'content-type': 'application/json' },
    });
  }

  const webhook = env.WECOM_WEBHOOK;
  if (!webhook) {
    // Not configured yet -> front-end falls back to mailto.
    return new Response(JSON.stringify({ ok: false, error: 'not_configured' }), {
      status: 503,
      headers: { 'content-type': 'application/json' },
    });
  }

  const payload = {
    msgtype: 'markdown',
    markdown: { content: buildMessage(data) },
  };

  try {
    const resp = await fetch(webhook, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const j = await resp.json().catch(() => ({}));
    if (j.errcode && j.errcode !== 0) {
      return new Response(
        JSON.stringify({ ok: false, error: 'wecom_error', detail: j.errmsg }),
        { status: 502, headers: { 'content-type': 'application/json' } }
      );
    }
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, error: 'wecom_unreachable' }), {
      status: 502,
      headers: { 'content-type': 'application/json' },
    });
  }

  return new Response(JSON.stringify({ ok: true }), {
    status: 200,
    headers: { 'content-type': 'application/json' },
  });
}
