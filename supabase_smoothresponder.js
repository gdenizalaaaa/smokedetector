// supabase/functions/smooth-responder/index.ts
import { serve } from "https://deno.land/std@0.198.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// Secrets
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const DEVICE_KEY = Deno.env.get("DEVICE_KEY")!;
const TELEGRAM_BOT_TOKEN = Deno.env.get("TELEGRAM_BOT_TOKEN")!;
const TELEGRAM_CHAT_ID = Deno.env.get("TELEGRAM_CHAT_ID")!;

// Supabase client
const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);

serve(async (req) => {
  try {
    // ---------------- AUTH ----------------
    if (req.method !== "POST") {
      return new Response("Only POST allowed", { status: 405 });
    }

    const deviceKey = req.headers.get("x-device-key");
    if (!deviceKey || deviceKey !== DEVICE_KEY) {
      return new Response(JSON.stringify({ error: "Unauthorized device" }), { status: 401 });
    }

    // ---------------- BODY ----------------
    const body = await req.json();
    const device_id = body.device_id ?? "unknown";
    const value = Number(body.value ?? -1);
    const threshold = Number(body.threshold ?? 300); // Default 300
    const extra = body.extra ?? {};
   const { data: sensor } = await supabase
  .from("sensors")
  .select("*")
  .eq("device_id", device_id)
  .single();

    // ---------------- COOLDOWN CONTROL ----------------
    const { data: lastAlert } = await supabase
      .from("smoke_alerts")
      .select("created_at")
      .eq("device_id", device_id)
      .order("created_at", { ascending: false })
      .limit(1)
      .single();

    const cooldown = 5 * 60 * 1000; // 5 dakika
    if (lastAlert && new Date().getTime() - new Date(lastAlert.created_at).getTime() < cooldown) {
      return new Response(JSON.stringify({ ok: true, skipped: "Cooldown active" }), { status: 200 });
    }

    // ---------------- DB INSERT ----------------
    const { data, error } = await supabase
      .from("smoke_alerts")
      .insert([{ device_id, value, threshold, extra }])
      .select()
      .single();

    if (error) {
      console.error("DB error:", error);
      return new Response(JSON.stringify({ error: "DB insert failed" }), { status: 500 });
    }

    // ---------------- THRESHOLD CHECK ----------------
    if (value <= threshold) {
      return new Response(
        JSON.stringify({ ok: true, skipped: "Value below threshold, no alert sent" }),
        { status: 200 }
      );
    }

    // ---------------- TELEGRAM ----------------
    const message =
  `🚨 *YANGIN ALGILANDI!*\n\n` +
  `📟 Sensör: ${sensor?.name ?? device_id}\n` +
  `🏢 Kat: ${sensor?.floor ?? "?"}\n` +
  `🔥 Duman Değeri: ${value}\n` +
  `⚠️ Threshold: ${threshold}\n` +
  `🕒 Zaman: ${new Date().toISOString()}\n\n` +
  `👉 En hızlı çıkış rotası:\n` +
  `https://fire-escape-system-9fev313c3-gdenizalaaaas-projects.vercel.app=${device_id}`;

    const { data: chats } = await supabase
      .from("telegram_subscribers")
      .select("chat_id")
      .eq("is_active", true);

    await Promise.all(
      (chats ?? []).map((c) =>
        fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            chat_id: c.chat_id,
            text: message,
            parse_mode: "Markdown",
          }),
        })
      )
    );

    return new Response(JSON.stringify({ ok: true, id: data.id }), { status: 200 });

  } catch (err) {
    console.error("Unhandled crash:", err);
    return new Response(JSON.stringify({ error: "Function crashed" }), { status: 500 });
  }
});
