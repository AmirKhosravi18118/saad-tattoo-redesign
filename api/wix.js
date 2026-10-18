// Vercel Serverless — Wix CRM integration for SAAD Tattoo
// POST /api/wix  { type: "contact"|"newsletter"|"booking", name, email, phone, message, service, date, time }
// Env: WIX_API_KEY (Authorization), WIX_SITE_ID
// Flow: every submission creates a real Contact in the owner's Wix CRM (label per type),
// booking requests additionally try a native Wix Booking; full payload is logged server-side.

const WIX_BASE = "https://www.wixapis.com";
const SERVICE_IDS = {
  "arm-design": "1215c518-d019-4cf8-ad1b-fd4eb32300e5",
  "bein-design": "567264c5-3d6f-4883-9147-0b4e60343d78",
  "ruecken-design": "67f166c8-ac03-4cbf-a4cf-310db4bacfd9",
  "brust-design": "adbd1027-9fc0-42ca-b2b3-26c4ecdbd7c2",
  "hals-nacken-design": "8d0be624-384a-4924-8211-6b7b9ac7a1d3"
};
const SERVICE_NAMES = {
  "arm-design": "Arm Design", "bein-design": "Bein Design", "ruecken-design": "Rücken Design",
  "brust-design": "Brust Design", "hals-nacken-design": "Hals & Nacken"
};

const wixHeaders = () => ({
  "Authorization": process.env.WIX_API_KEY,
  "wix-site-id": process.env.WIX_SITE_ID,
  "Content-Type": "application/json"
});

async function createContact({ name, email, phone }) {
  const [first = "Website", ...rest] = (name || "").trim().split(" ");
  const info = {
    name: { first, last: rest.join(" ") || "-" }
  };
  if (email) info.emails = { items: [{ email, tag: "MAIN" }] };
  if (phone) info.phones = { items: [{ phone, tag: "MAIN" }] };
  const res = await fetch(`${WIX_BASE}/contacts/v4/contacts`, {
    method: "POST",
    headers: wixHeaders(),
    body: JSON.stringify({ info }) // v4: info در ریشه بدنه — بدون contact wrapper و allowDuplicates
  });
  const json = await res.json().catch(() => ({}));
  if (!res.ok) {
    if (JSON.stringify(json).includes("DUPLICATE_CONTACT_EXISTS")) {
      return { id: "existing", duplicate: true }; // کانتکت از قبل هست — مشتری همان است
    }
    console.error("Wix contact failed:", res.status, JSON.stringify(json).slice(0, 160));
    throw new Error(`contacts ${res.status}`);
  }
  return json.contact;
}

// تلاش برای رزرو واقعی Wix Bookings (اگر slot موجود باشد؛ در غیر این صورت lead در CRM می‌ماند)
async function tryCreateBooking({ service, date, time, name, email, phone }) {
  const serviceId = SERVICE_IDS[service];
  if (!serviceId || !date || !time) return { bookingCreated: false, reason: "no-slot-lookup" };
  const startISO = `${date}T${time}:00.000Z`;
  const endISO = `${date}T${time}:00.000Z`;
  try {
    const res = await fetch(`${WIX_BASE}/bookings/v2/bookings`, {
      method: "POST",
      headers: wixHeaders(),
      body: JSON.stringify({
        booking: {
          bookedEntity: { singleService: { serviceId } },
          contactDetails: { firstName: (name || "").split(" ")[0] || "Website", lastName: (name || "").split(" ").slice(1).join(" ") || "-", email, phone },
          startDate: startISO,
          endDate: endISO
        }
      })
    });
    const json = await res.json().catch(() => ({}));
    return { bookingCreated: res.ok, bookingId: json.booking && json.booking.id, reason: res.ok ? "created" : JSON.stringify(json).slice(0, 120) };
  } catch (e) {
    return { bookingCreated: false, reason: e.message.slice(0, 100) };
  }
}

module.exports = async (req, res) => {
  if (req.method === "OPTIONS") {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
    return res.status(204).end();
  }
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });
  res.setHeader("Access-Control-Allow-Origin", "*");

  try {
    const body = typeof req.body === "string" ? JSON.parse(req.body) : req.body;
    const { type, name, email, phone, message, service, date, time } = body || {};

    if (!["contact", "newsletter", "booking"].includes(type)) return res.status(400).json({ error: "invalid type" });
    if (!email && !phone) return res.status(400).json({ error: "email or phone required" });
    if (!process.env.WIX_API_KEY) return res.status(503).json({ error: "integration not configured" });

    // ثبت کامل در لاگ سرور (Vercel Logs) — سند سمت سرور
    console.log("LEAD:", JSON.stringify({ type, name, email, phone, service, date, time, message: (message || "").slice(0, 500) }));

    // ۰) نوتیفیکیشن فوری WhatsApp به صاحب بیزینس (CallMeBot) — همیشه، قبل از هر چیز
    let whatsappSent = false;
    try {
      if (process.env.CALLMEBOT_KEY) {
        const svcName = SERVICE_NAMES[service] || service || "";
        const lines = [];
        if (type === "booking") {
          lines.push(` NUOVA PRENOTAZIONE / درخواست رزرو`);
          lines.push(` Servizio: ${svcName}`);
          lines.push(` Data: ${date} · Ore: ${time}`);
        } else if (type === "contact") {
          lines.push(" NUOVO MESSAGGIO / پیام جدید از سایت");
        } else {
          lines.push(" NUOVO ISCRITTO NEWSLETTER / عضویت خبرنامه");
        }
        if (name) lines.push(` Nome: ${name}`);
        if (email) lines.push(` Email: ${email}`);
        if (phone) lines.push(` Tel: ${phone}`);
        if (message) lines.push(` Msg: ${String(message).slice(0, 300)}`);
        const text = encodeURIComponent(lines.join("\n"));
        const waRes = await fetch(`https://api.callmebot.com/whatsapp.php?phone=${process.env.OWNER_PHONE}&text=${text}&apikey=${process.env.CALLMEBOT_KEY}`, { method: "GET" });
        whatsappSent = waRes.ok;
        if (!waRes.ok) console.error("WhatsApp notify failed:", waRes.status);
      }
    } catch (e) { console.error("WhatsApp notify error:", e.message); }

    // ۱) کانتکت واقعی در CRM ویکس
    const contact = await createContact({ name, email, phone });

    // ۲) برای رزرو: تلاش برای Booking واقعی (با slot در صورت وجود)
    let bookingInfo = null;
    if (type === "booking") {
      bookingInfo = await tryCreateBooking({ service, date, time, name, email, phone });
    }

    return res.status(200).json({
      ok: true,
      contactId: contact && contact.id,
      whatsappSent,
      booking: bookingInfo,
      type,
      service: type === "booking" ? (SERVICE_NAMES[service] || service) : undefined
    });
  } catch (e) {
    console.error("LEAD ERROR:", e.message);
    return res.status(502).json({ ok: false, error: e.message.slice(0, 180) });
  }
};
