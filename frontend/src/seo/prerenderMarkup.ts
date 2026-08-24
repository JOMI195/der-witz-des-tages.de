import { landingContent } from "./landingContent";

const FONT_STACK =
  "Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif";

const shell = (inner: string, align: "center" | "left") =>
  `<div style="max-width:760px;margin:0 auto;padding:48px 24px;font-family:${FONT_STACK};text-align:${align}">${inner}</div>`;

const wordmark =
  `<a href="/"><img src="/witz-des-tages-logo-light-full.svg" alt="Der Witz des Tages" width="320" height="80" style="max-width:100%;height:auto" /></a>`;

const footerLinks =
  `<p style="font-size:0.8rem"><a href="/galerie/">Galerie</a> · <a href="/witz-einreichen/">Witz einreichen</a> · <a href="/kontakt/">Kontakt</a> · <a href="/datenschutzerklaerung/">Datenschutzerklärung</a> · <a href="/impressum/">Impressum</a></p>`;

const stub = (heading: string, body: string) =>
  shell(
    [
      `<div style="text-align:center;margin:0 0 40px">${wordmark}</div>`,
      `<h1 style="font-size:1.75rem;margin:0 0 12px">${heading}</h1>`,
      `<p style="margin:0 0 32px">${body}</p>`,
      footerLinks,
    ].join(""),
    "left",
  );

export const prerenderMarkup: Record<string, string> = {
  "/": shell(
    [
      wordmark,
      `<h1 style="font-size:2rem;margin:32px 0 16px">${landingContent.headline}</h1>`,
      `<p style="font-size:1.05rem;line-height:1.6;margin:0 0 32px">${landingContent.lead}</p>`,
      `<p style="margin:0 0 24px"><a href="/galerie/" style="display:inline-block;padding:12px 32px;border-radius:10px;background:#7b3ff2;color:#fff;text-decoration:none">Zur Witze Galerie</a></p>`,
      `<p style="margin:0 0 32px;font-size:0.9rem">${landingContent.submitHint}</p>`,
      footerLinks,
    ].join(""),
    "center",
  ),
  "/galerie/": stub(
    "Witze Galerie",
    "Alle bisherigen Witze des Tages mit ihren Bildern – durchstöbere das Archiv und finde deinen Lieblingswitz.",
  ),
  "/witz-einreichen/": stub(
    "Witz einreichen",
    "Reiche deinen Lieblingsflachwitz ein und werde vielleicht schon morgen als Witz des Tages gefeatured.",
  ),
  "/kontakt/": stub(
    "Kontakt",
    "Fragen, Anregungen oder einen Bug gefunden? Schreib uns über das Kontaktformular – wir melden uns zurück.",
  ),
  "/datenschutzerklaerung/": stub(
    "Datenschutzerklärung",
    "Informationen darüber, welche personenbezogenen Daten Der Witz des Tages zu welchen Zwecken verarbeitet und welche Rechte dir nach DSGVO zustehen.",
  ),
  "/impressum/": stub(
    "Impressum",
    "Anbieterkennzeichnung nach § 5 TMG mit Herausgeber, Kontaktdaten und Urheberrechtshinweisen zu der-witz-des-tages.de.",
  ),
};
