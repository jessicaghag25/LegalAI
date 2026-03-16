export default function SectionCard({ title, children }) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <h2 className="mb-3 text-lg font-semibold text-slate-800">{title}</h2>
      <div className="text-sm text-slate-600">{children}</div>
    </section>
  )
}
