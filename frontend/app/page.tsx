'use client'

import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import type { Components } from 'react-markdown'

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

interface Insights {
  technologies: string[]
  innovation_score: number
  tech_maturity_score: number
  signals: string[]
  insights: string[]
}

interface AnalysisResult {
  company: string
  insights: Insights
  report: string
}

const markdownComponents: Components = {
  h1: ({ children }) => (
    <h1 className="text-xl font-semibold text-white mb-4 mt-2">{children}</h1>
  ),
  h2: ({ children }) => (
    <h2 className="text-sm font-semibold text-zinc-300 uppercase tracking-widest mt-6 mb-2">
      {children}
    </h2>
  ),
  p: ({ children }) => (
    <p className="text-zinc-400 leading-relaxed mb-3 text-sm">{children}</p>
  ),
  ul: ({ children }) => (
    <ul className="space-y-1 mb-3 pl-4">{children}</ul>
  ),
  li: ({ children }) => (
    <li className="text-zinc-400 text-sm before:content-['–'] before:mr-2 before:text-zinc-600">
      {children}
    </li>
  ),
  strong: ({ children }) => (
    <strong className="font-semibold text-zinc-200">{children}</strong>
  ),
  table: ({ children }) => (
    <table className="w-full text-sm border-collapse mb-4">{children}</table>
  ),
  thead: ({ children }) => <thead>{children}</thead>,
  tbody: ({ children }) => <tbody>{children}</tbody>,
  tr: ({ children }) => (
    <tr className="border-b border-zinc-800">{children}</tr>
  ),
  th: ({ children }) => (
    <th className="text-left py-2 px-3 text-zinc-500 font-medium text-xs uppercase tracking-widest">
      {children}
    </th>
  ),
  td: ({ children }) => (
    <td className="py-2 px-3 text-zinc-400 text-sm">{children}</td>
  ),
  code: ({ children }) => (
    <code className="font-mono text-xs bg-zinc-800 px-1.5 py-0.5 rounded text-zinc-300">
      {children}
    </code>
  ),
  hr: () => <hr className="border-zinc-800 my-4" />,
}

export default function Home() {
  const [company, setCompany] = useState('')
  const [url, setUrl] = useState('')
  const [githubOrg, setGithubOrg] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setResult(null)
    setError(null)

    try {
      const res = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          company,
          url,
          github_org: githubOrg || null,
        }),
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail ?? `Error ${res.status}`)
      }
      setResult(await res.json())
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const inputClass =
    'w-full bg-zinc-900 border border-zinc-800 rounded-lg px-3.5 py-2.5 text-sm text-zinc-100 placeholder-zinc-600 focus:outline-none focus:border-zinc-600 focus:ring-1 focus:ring-zinc-600 transition'

  const labelClass =
    'block text-xs font-medium text-zinc-500 mb-1.5 uppercase tracking-widest'

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100">
      <div className="max-w-3xl mx-auto px-6 py-14">

        {/* Header */}
        <div className="mb-10">
          <h1 className="text-2xl font-semibold tracking-tight text-white">
            Company Intelligence
          </h1>
          <p className="mt-1.5 text-sm text-zinc-500">
            Analyze a company&apos;s tech stack, market signals, and generate actionable insights.
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label className={labelClass}>Company name</label>
              <input
                type="text"
                required
                value={company}
                onChange={e => setCompany(e.target.value)}
                placeholder="Stripe"
                className={inputClass}
              />
            </div>
            <div>
              <label className={labelClass}>Website URL</label>
              <input
                type="url"
                required
                value={url}
                onChange={e => setUrl(e.target.value)}
                placeholder="https://stripe.com"
                className={inputClass}
              />
            </div>
          </div>

          <div className="sm:w-1/2">
            <label className={labelClass}>
              GitHub org{' '}
              <span className="normal-case text-zinc-700">(optional)</span>
            </label>
            <input
              type="text"
              value={githubOrg}
              onChange={e => setGithubOrg(e.target.value)}
              placeholder="stripe"
              className={inputClass}
            />
          </div>

          <div className="pt-2">
            <button
              type="submit"
              disabled={loading}
              className="bg-white text-zinc-950 text-sm font-medium px-5 py-2.5 rounded-lg hover:bg-zinc-200 disabled:opacity-40 disabled:cursor-not-allowed transition"
            >
              {loading ? 'Analyzing…' : 'Analyze'}
            </button>
          </div>
        </form>

        {/* Loading */}
        {loading && (
          <div className="mt-16 flex flex-col items-center gap-4 text-zinc-500">
            <div className="h-7 w-7 rounded-full border-2 border-zinc-700 border-t-zinc-400 animate-spin" />
            <p className="text-sm">Running analysis pipeline…</p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mt-8 rounded-lg border border-red-900/50 bg-red-950/20 px-4 py-3 text-sm text-red-400">
            {error}
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="mt-12 space-y-8">

            {/* Scores */}
            <div className="grid grid-cols-2 gap-4">
              <div className="rounded-xl bg-zinc-900 border border-zinc-800 p-6">
                <p className="text-xs font-medium uppercase tracking-widest text-zinc-500 mb-3">
                  Innovation Score
                </p>
                <p className="text-5xl font-bold text-white tabular-nums leading-none">
                  {result.insights.innovation_score}
                  <span className="text-lg font-normal text-zinc-600 ml-1">/ 100</span>
                </p>
              </div>
              <div className="rounded-xl bg-zinc-900 border border-zinc-800 p-6">
                <p className="text-xs font-medium uppercase tracking-widest text-zinc-500 mb-3">
                  Tech Maturity
                </p>
                <p className="text-5xl font-bold text-white tabular-nums leading-none">
                  {result.insights.tech_maturity_score}
                  <span className="text-lg font-normal text-zinc-600 ml-1">/ 100</span>
                </p>
              </div>
            </div>

            {/* Technologies */}
            {result.insights.technologies.length > 0 && (
              <div>
                <p className="text-xs font-medium uppercase tracking-widest text-zinc-500 mb-3">
                  Technologies
                </p>
                <div className="flex flex-wrap gap-2">
                  {result.insights.technologies.map(tech => (
                    <span
                      key={tech}
                      className="px-2.5 py-1 rounded-md bg-zinc-900 border border-zinc-700 text-xs font-mono text-zinc-300"
                    >
                      {tech}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Report */}
            <div>
              <p className="text-xs font-medium uppercase tracking-widest text-zinc-500 mb-4">
                Report
              </p>
              <div className="rounded-xl bg-zinc-900 border border-zinc-800 px-6 py-5">
                <ReactMarkdown components={markdownComponents}>
                  {result.report}
                </ReactMarkdown>
              </div>
            </div>

          </div>
        )}
      </div>
    </main>
  )
}
