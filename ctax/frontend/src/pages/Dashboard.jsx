import { useMemo, useState } from 'react'
import SectionCard from '../components/SectionCard'

import en from '../locales/en/translation.json'
import fr from '../locales/fr/translation.json'
import pa from '../locales/pa/translation.json'
import hi from '../locales/hi/translation.json'
import es from '../locales/es/translation.json'
import tl from '../locales/tl/translation.json'
import sw from '../locales/sw/translation.json'
import ti from '../locales/ti/translation.json'

const dictionary = { en, fr, pa, hi, es, tl, sw, ti }

const celebrationThemes = {
  global: '⭐ Stars + confetti',
  south_asian: '🎇 Diwali sparkles',
  east_asian: '🏮 Lantern glow',
  muslim: '🌙 Crescent stars',
}

const connectedPlatforms = ['CRA My Account', 'TurboTax', 'BetterTax', 'H&R Block', 'UFile', 'NETFILE Tools']

export default function Dashboard() {
  const [lang, setLang] = useState('en')
  const [theme, setTheme] = useState('global')
  const t = useMemo(() => dictionary[lang] ?? dictionary.en, [lang])

  return (
    <main className="min-h-screen bg-gradient-to-br from-sky-50 via-white to-violet-50 p-6 md:p-10">
      <header className="mb-6 rounded-2xl bg-indigo-600 p-6 text-white shadow-lg">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h1 className="text-2xl font-bold">{t.title}</h1>
          <div className="flex gap-3">
            <label className="text-sm font-semibold">
              {t.language}
              <select className="ml-2 rounded bg-white px-2 py-1 text-slate-800" value={lang} onChange={(e) => setLang(e.target.value)}>
                {Object.keys(dictionary).map((code) => (
                  <option key={code} value={code}>{code.toUpperCase()}</option>
                ))}
              </select>
            </label>
            <label className="text-sm font-semibold">
              {t.culture}
              <select className="ml-2 rounded bg-white px-2 py-1 text-slate-800" value={theme} onChange={(e) => setTheme(e.target.value)}>
                {Object.keys(celebrationThemes).map((key) => (
                  <option key={key} value={key}>{key}</option>
                ))}
              </select>
            </label>
          </div>
        </div>
        <p className="mt-2 text-indigo-100">{t.disclaimer}</p>
      </header>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <SectionCard title={t.syncHub || 'Software Sync Hub'}>
          <p className="mb-2 text-sm">OAuth-linked integrations with explicit approval before export.</p>
          <ul className="space-y-1 text-sm">
            {connectedPlatforms.map((provider) => (
              <li key={provider} className="rounded bg-sky-50 px-2 py-1">🔗 {provider}</li>
            ))}
          </ul>
          <div className="mt-2 text-xs text-slate-500">Import: CSV/PDF/XML • Export: user-approved only</div>
        </SectionCard>

        <SectionCard title={t.avatar}>
          <p>Layered avatar builder: skin tone, hair texture, attire, accessories, gestures.</p>
          <p className="mt-2 rounded bg-violet-50 p-2">Current celebration: {celebrationThemes[theme]}</p>
        </SectionCard>

        <SectionCard title={t.familyTree}>
          <ul className="space-y-2">
            <li className="rounded-lg bg-emerald-50 p-2">🧕🏽 Amina (guardian) · 220 pts</li>
            <li className="rounded-lg bg-emerald-50 p-2">🧔🏾 Raj (guardian) · 150 pts</li>
            <li className="rounded-lg bg-emerald-50 p-2">🧒🏽 Zara (student) · 120 pts</li>
          </ul>
        </SectionCard>

        <SectionCard title={t.adventureMap}>
          <ul className="space-y-2 text-sm">
            <li className="rounded bg-indigo-50 p-2">1) Profile Setup</li>
            <li className="rounded bg-indigo-50 p-2">2) Import/Upload Documents</li>
            <li className="rounded bg-indigo-50 p-2">3) Find Deductions</li>
            <li className="rounded bg-indigo-50 p-2">4) Risk Scan</li>
            <li className="rounded bg-indigo-50 p-2">5) Tax Questions</li>
          </ul>
        </SectionCard>

        <SectionCard title={t.tipsFeed}>
          <ul className="space-y-2">
            <li className="animate-pulse rounded-lg bg-amber-50 p-2">⭐ Connect CRA/TurboTax to pre-fill forms and reduce manual errors.</li>
            <li className="animate-pulse rounded-lg bg-amber-50 p-2">📁 Imported documents can auto-complete upload milestones.</li>
            <li className="animate-pulse rounded-lg bg-amber-50 p-2">🛡️ Exports require explicit approval before any platform push.</li>
          </ul>
        </SectionCard>

        <SectionCard title={t.inclusive}>
          Supports diverse family structures, identity preferences, and culturally respectful interactions.
        </SectionCard>
      </div>
    </main>
  )
}
