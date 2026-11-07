'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

type Finding = {
  result_id: string;
  result_type: string;
  entity_id: string | null;
  group_key: string;
  period_start: string | null;
  period_end: string | null;
  result_value: number;
  result_unit: string;
  result_category: string;
  priority_rank: number | null;
  finding: string;
  evidence: {
    budget_total?: number;
    actual_total?: number;
    variance_amount?: number;
    variance_percentage?: number;
    committed_total?: number;
    forecast_total?: number;
    independent_source_count?: number;
    source_record_ids?: string[];
    canonical_record_ids?: string[];
    aggregation_method?: string;
    reporting_period?: {
      period_start?: string;
      period_end?: string;
    };
    currency_unit?: string;
  };
  method_version: string;
  data_version: string;
  generated_at: string;
  quality_status: string;
  limitation: string[] | string | null;
};

type ApiResult = {
  total: number;
  results: Finding[];
};

type HealthResponse = {
  status: string;
  message?: string;
};

type MetadataResponse = {
  approved_track?: string;
  dataset_version?: string;
  method_version?: string;
  contract_version?: string;
  generated_at?: string;
  result_count?: number;
  validation_status?: string;
};

type ValidationSection = {
  status?: string;
  passed_count?: number;
  total_checks?: number;
};

type ValidationMetrics = {
  analytical_validation?: ValidationSection;
  reconciliation_validation?: ValidationSection;
  overall_status?: string;
  passed_count?: number;
  failed_count?: number;
};

type SensitivityAssessment = {
  test_design?: string;
  rank_changed_count?: number;
  variance_changed_count?: number;
  quality_status_changed_count?: number;
  newly_insufficient_evidence_count?: number;
  interpretation?: string;
};

type IntelligenceSummary = {
  overall_finding_count?: number;
  monthly_finding_count?: number;
  sensitivity_assessment?: SensitivityAssessment;
  primary_analytical_question?: string;
  decision_to_be_supported?: string;
  baseline_method?: string;
  important_limitations?: string[];
  limitations?: string[];
};

type SummaryPayload = {
  summary?: IntelligenceSummary;
  validation_metrics?: ValidationMetrics;
  baseline_reconciliation?: {
    overall_status?: string;
    total_checks?: number;
  };
  weak_case_review?: {
    weak_case_count?: number;
  };
};

const money = (value?: number, unit = 'USD') => {
  if (typeof value !== 'number' || !Number.isFinite(value)) return '—';

  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: unit,
    maximumFractionDigits: 2,
  }).format(value);
};

const number = (value?: number) =>
  typeof value === 'number' && Number.isFinite(value)
    ? value.toLocaleString('en-US')
    : '—';

const percent = (value?: number) =>
  typeof value === 'number' && Number.isFinite(value)
    ? `${value.toFixed(2)}%`
    : '—';

const dateLabel = (value?: string) => {
  if (!value) return '—';
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? value
    : date.toLocaleString();
};

const label = (value?: string) =>
  (value || 'Unknown').replaceAll('_', ' ');

function MetricCard({
  title,
  value,
  note,
}: {
  title: string;
  value: string | number;
  note: string;
}) {
  return (
    <div className="rounded-2xl border border-[#263244] bg-[#101622] p-5">
      <p className="text-xs font-medium uppercase tracking-wider text-[#8995a8]">
        {title}
      </p>
      <p className="mt-3 text-2xl font-semibold text-[#e8edf5]">{value}</p>
      <p className="mt-2 text-xs text-[#8995a8]">{note}</p>
    </div>
  );
}

function StatusLabel({ value }: { value: string }) {
  const color =
    value === 'validated_with_limitations'
      ? 'border-emerald-400/30 bg-emerald-400/10 text-emerald-300'
      : value === 'insufficient_evidence'
        ? 'border-amber-400/30 bg-amber-400/10 text-amber-300'
        : 'border-[#526078] bg-[#263244] text-[#cbd5e1]';

  return (
    <span className={`inline-flex rounded-full border px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wide ${color}`}>
      {label(value)}
    </span>
  );
}

export default function DataIntelligencePage() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [metadata, setMetadata] = useState<MetadataResponse | null>(null);
  const [payload, setPayload] = useState<SummaryPayload | null>(null);
  const [apiResults, setApiResults] = useState<ApiResult | null>(null);
  const [selected, setSelected] = useState<Finding | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [detailLoading, setDetailLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [view, setView] = useState('overall');

  useEffect(() => {
    let active = true;

    async function loadPage() {
      setLoading(true);
      setError('');

      try {
        const responses = await Promise.all([
          fetch(`${API_URL}/api/intelligence/health`, { cache: 'no-store' }),
          fetch(`${API_URL}/api/intelligence/metadata`, { cache: 'no-store' }),
          fetch(`${API_URL}/api/intelligence/summary`, { cache: 'no-store' }),
          fetch(`${API_URL}/api/intelligence/results?limit=100&offset=0`, {
            cache: 'no-store',
          }),
        ]);

        const healthData = await responses[0].json();

        if (!responses[0].ok || healthData.status !== 'ready') {
          throw new Error(
            healthData.message || 'Intelligence data is not ready.',
          );
        }

        for (const response of responses.slice(1)) {
          if (!response.ok) {
            throw new Error(
              'The approved intelligence data could not be loaded.',
            );
          }
        }

        const [metadataData, summaryData, resultsData] = await Promise.all([
          responses[1].json(),
          responses[2].json(),
          responses[3].json(),
        ]);

        if (!active) return;

        setHealth(healthData);
        setMetadata(metadataData);
        setPayload(summaryData);
        setApiResults(resultsData);
      } catch (err) {
        if (active) {
          setError(
            err instanceof Error
              ? err.message
              : 'Unable to load intelligence data.',
          );
        }
      } finally {
        if (active) setLoading(false);
      }
    }

    loadPage();

    return () => {
      active = false;
    };
  }, []);

  const allFindings = useMemo(() => apiResults?.results ?? [], [apiResults]);

  const visibleFindings = useMemo(() => {
    return allFindings.filter((item) => {
      const isMonthly = item.result_type.startsWith('monthly_');
      if (view === 'overall' && isMonthly) return false;
      if (view === 'monthly' && !isMonthly) return false;

      if (
        statusFilter !== 'all' &&
        item.quality_status !== statusFilter
      ) {
        return false;
      }

      if (
        categoryFilter !== 'all' &&
        item.result_category !== categoryFilter
      ) {
        return false;
      }

      if (search.trim()) {
        const term = search.trim().toLowerCase();
        const text = [
          item.group_key,
          item.entity_id,
          item.result_type,
          item.finding,
          item.result_category,
        ]
          .filter(Boolean)
          .join(' ')
          .toLowerCase();

        if (!text.includes(term)) return false;
      }

      return true;
    });
  }, [allFindings, view, statusFilter, categoryFilter, search]);

  const summary = payload?.summary;
  const validation = payload?.validation_metrics;
  const sensitivity = summary?.sensitivity_assessment;
  const reconciliation = payload?.baseline_reconciliation;
  const weakCases = payload?.weak_case_review;

  async function openFinding(item: Finding) {
    setSelected(item);
    setDetailLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/api/intelligence/results/${encodeURIComponent(item.result_id)}`,
        { cache: 'no-store' },
      );

      if (!response.ok) {
        throw new Error('Could not load finding details.');
      }

      const data = await response.json();
      setSelected(data.result);
    } catch {
      // The list item already contains the published evidence.
      setSelected(item);
    } finally {
      setDetailLoading(false);
    }
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-[#080b12] px-5 py-16 text-[#e8edf5]">
        <div className="mx-auto max-w-7xl">
          <p className="text-sm text-[#8995a8]">
            Loading approved intelligence results…
          </p>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="min-h-screen bg-[#080b12] px-5 py-10 text-[#e8edf5]">
        <div className="mx-auto max-w-4xl rounded-2xl border border-amber-400/30 bg-[#101622] p-7">
          <p className="text-xs font-semibold uppercase tracking-widest text-amber-300">
            Intelligence data unavailable
          </p>
          <h1 className="mt-3 text-xl font-semibold">
            Data Intelligence could not be loaded
          </h1>
          <p className="mt-3 text-sm text-[#aab5c5]">{error}</p>
          <p className="mt-2 text-xs text-[#8995a8]">
            Check that the backend is running and the approved output
            artifacts are available.
          </p>
          <Link
            href="/"
            className="mt-6 inline-flex rounded-xl border border-[#526078] px-4 py-2 text-sm text-[#e8edf5] hover:bg-white/5"
          >
            Return to operational dashboard
          </Link>
        </div>
      </main>
    );
  }

  const overallCount = summary?.overall_finding_count ?? 0;
  const monthlyCount = summary?.monthly_finding_count ?? 0;
  const unit = 'USD';

  return (
    <main className="min-h-screen bg-[#080b12] text-[#e8edf5]">
      <header className="border-b border-[#263244] bg-[#0b111c] px-5 py-6 sm:px-8">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-[10px] font-semibold uppercase tracking-[0.24em] text-[#55a6ff]">
              Infocreon Internship · PoC-4 · Batch 8
            </p>
            <h1 className="mt-2 text-2xl font-semibold tracking-tight sm:text-3xl">
              Data Intelligence
            </h1>
            <p className="mt-2 max-w-2xl text-sm text-[#8995a8]">
              Evidence-led comparative intelligence for budget versus actual
              financial review.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <span className="rounded-full border border-emerald-400/30 bg-emerald-400/10 px-3 py-2 text-xs text-emerald-300">
              API {health?.status || 'unknown'}
            </span>
            <Link
              href="/"
              className="rounded-xl border border-[#526078] px-4 py-2.5 text-sm text-[#dce5f2] transition hover:bg-white/5"
            >
              Operational dashboard
            </Link>
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-7xl space-y-8 px-5 py-8 sm:px-8">
        <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <MetricCard
            title="Overall comparisons"
            value={number(overallCount)}
            note="Eligible overall grouped findings"
          />
          <MetricCard
            title="Monthly findings"
            value={number(monthlyCount)}
            note="Separate descriptive monthly findings"
          />
          <MetricCard
            title="Analytical validation"
            value={`${number(validation?.analytical_validation?.passed_count)} / ${number(validation?.analytical_validation?.total_checks)}`}
            note="Recorded analytical validation checks passed"
          />
          <MetricCard
            title="Reconciliation"
            value={`${number(validation?.reconciliation_validation?.passed_count)} / ${number(validation?.reconciliation_validation?.total_checks)}`}
            note="Baseline and aggregation checks passed"
          />
        </section>

        <section className="rounded-2xl border border-[#263244] bg-[#101622] p-5 sm:p-6">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <p className="text-xs font-semibold uppercase tracking-widest text-[#55a6ff]">
                Approved analytical track
              </p>
              <h2 className="mt-2 text-lg font-semibold">
                {metadata?.approved_track}
              </h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-[#aab5c5]">
                {summary?.primary_analytical_question}
              </p>
            </div>
            <div className="text-xs leading-6 text-[#8995a8]">
              <p>Dataset version: {metadata?.dataset_version}</p>
              <p>Method version: {metadata?.method_version}</p>
              <p>Contract version: {metadata?.contract_version}</p>
            </div>
          </div>
          <div className="mt-5 border-t border-[#263244] pt-4">
            <p className="text-xs font-semibold uppercase tracking-wider text-[#8995a8]">
              Decision supported
            </p>
            <p className="mt-2 text-sm leading-6 text-[#c3cedd]">
              {summary?.decision_to_be_supported}
            </p>
          </div>
        </section>

        <section className="space-y-4">
          <div className="flex flex-wrap items-end justify-between gap-3">
            <div>
              <p className="text-xs font-semibold uppercase tracking-widest text-[#55a6ff]">
                Published findings
              </p>
              <h2 className="mt-1 text-xl font-semibold">
                Comparative intelligence
              </h2>
            </div>
            <span className="text-xs text-[#8995a8]">
              {number(apiResults?.total)} findings available from the API
            </span>
          </div>

          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setView('overall')}
              className={`rounded-xl px-4 py-2 text-sm ${view === 'overall' ? 'bg-[#24518a] text-white' : 'border border-[#263244] text-[#aab5c5] hover:bg-white/5'}`}
            >
              Overall comparisons ({number(overallCount)})
            </button>
            <button
              onClick={() => setView('monthly')}
              className={`rounded-xl px-4 py-2 text-sm ${view === 'monthly' ? 'bg-[#24518a] text-white' : 'border border-[#263244] text-[#aab5c5] hover:bg-white/5'}`}
            >
              Monthly findings ({number(monthlyCount)})
            </button>
          </div>

          {view === 'monthly' && (
            <div className="rounded-xl border border-amber-400/30 bg-amber-400/[0.07] p-4 text-sm leading-6 text-amber-200">
              Monthly findings are descriptive and marked
              insufficient_evidence where independent source counts are below
              the required threshold. Do not interpret them as reliable trends,
              forecasts, or risk scores.
            </div>
          )}

          <div className="grid gap-3 md:grid-cols-3">
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search group or finding…"
              aria-label="Search findings"
              className="rounded-xl border border-[#263244] bg-[#101622] px-4 py-3 text-sm text-[#e8edf5] outline-none placeholder:text-[#68758a] focus:border-[#55a6ff]"
            />
            <select
              value={statusFilter}
              onChange={(event) => setStatusFilter(event.target.value)}
              aria-label="Filter by evidence status"
              className="rounded-xl border border-[#263244] bg-[#101622] px-4 py-3 text-sm text-[#e8edf5] outline-none focus:border-[#55a6ff]"
            >
              <option value="all">All evidence statuses</option>
              <option value="validated_with_limitations">
                Validated with limitations
              </option>
              <option value="insufficient_evidence">
                Insufficient evidence
              </option>
            </select>
            <select
              value={categoryFilter}
              onChange={(event) => setCategoryFilter(event.target.value)}
              aria-label="Filter by variance category"
              className="rounded-xl border border-[#263244] bg-[#101622] px-4 py-3 text-sm text-[#e8edf5] outline-none focus:border-[#55a6ff]"
            >
              <option value="all">All variance categories</option>
              <option value="overspend">Overspending</option>
              <option value="underspend">Underspending</option>
              <option value="on_budget">On budget</option>
            </select>
          </div>

          <div className="overflow-hidden rounded-2xl border border-[#263244] bg-[#101622]">
            <div className="overflow-x-auto">
              <table className="w-full min-w-[850px] text-left text-sm">
                <thead className="bg-[#151e2c] text-[10px] uppercase tracking-wider text-[#8995a8]">
                  <tr>
                    <th className="px-4 py-4">Rank</th>
                    <th className="px-4 py-4">Group</th>
                    <th className="px-4 py-4">Variance</th>
                    <th className="px-4 py-4">Category</th>
                    <th className="px-4 py-4">Sources</th>
                    <th className="px-4 py-4">Evidence status</th>
                    <th className="px-4 py-4">Details</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#263244]">
                  {visibleFindings.map((item) => (
                    <tr key={item.result_id} className="hover:bg-white/[0.025]">
                      <td className="px-4 py-4 text-[#aab5c5]">
                        {view === 'overall' && item.priority_rank
                          ? `#${item.priority_rank}`
                          : '—'}
                      </td>
                      <td className="px-4 py-4">
                        <p className="font-semibold text-[#e8edf5]">
                          {item.group_key}
                        </p>
                        <p className="mt-1 text-xs text-[#8995a8]">
                          {label(item.result_type)}
                        </p>
                      </td>
                      <td className="px-4 py-4">
                        <p className="font-semibold">
                          {money(item.evidence?.variance_amount, unit)}
                        </p>
                        <p className="mt-1 text-xs text-[#8995a8]">
                          {percent(item.evidence?.variance_percentage)}
                        </p>
                      </td>
                      <td className="px-4 py-4 capitalize text-[#c3cedd]">
                        {label(item.result_category)}
                      </td>
                      <td className="px-4 py-4 text-[#c3cedd]">
                        {number(item.evidence?.independent_source_count)}
                      </td>
                      <td className="px-4 py-4">
                        <StatusLabel value={item.quality_status} />
                      </td>
                      <td className="px-4 py-4">
                        <button
                          onClick={() => openFinding(item)}
                          className="rounded-lg border border-[#526078] px-3 py-2 text-xs text-[#dce5f2] hover:border-[#55a6ff] hover:text-white"
                        >
                          View evidence
                        </button>
                      </td>
                    </tr>
                  ))}
                  {visibleFindings.length === 0 && (
                    <tr>
                      <td
                        colSpan={7}
                        className="px-4 py-10 text-center text-sm text-[#8995a8]"
                      >
                        No findings match the selected filters.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </section>

        {selected && (
          <section className="rounded-2xl border border-[#55a6ff]/30 bg-[#101622] p-5 sm:p-6">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <p className="text-xs font-semibold uppercase tracking-widest text-[#55a6ff]">
                  Finding evidence {detailLoading ? '· Loading details…' : ''}
                </p>
                <h2 className="mt-2 text-lg font-semibold">
                  {selected.group_key}
                </h2>
              </div>
              <button
                onClick={() => setSelected(null)}
                className="rounded-lg border border-[#526078] px-3 py-2 text-xs text-[#c3cedd] hover:bg-white/5"
              >
                Close details
              </button>
            </div>

            <p className="mt-4 text-sm leading-6 text-[#c3cedd]">
              {selected.finding}
            </p>

            <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {[
                ['Budget', money(selected.evidence?.budget_total, unit)],
                ['Actual', money(selected.evidence?.actual_total, unit)],
                ['Absolute variance', money(selected.evidence?.variance_amount, unit)],
                ['Variance percentage', percent(selected.evidence?.variance_percentage)],
                ['Committed', money(selected.evidence?.committed_total, unit)],
                ['Forecast', money(selected.evidence?.forecast_total, unit)],
                ['Independent sources', number(selected.evidence?.independent_source_count)],
                ['Period start', selected.period_start || '—'],
                ['Period end', selected.period_end || '—'],
              ].map(([name, value]) => (
                <div
                  key={name}
                  className="rounded-xl border border-[#263244] bg-[#0b111c] p-4"
                >
                  <p className="text-[10px] uppercase tracking-wider text-[#8995a8]">
                    {name}
                  </p>
                  <p className="mt-2 text-sm font-semibold text-[#e8edf5]">
                    {value}
                  </p>
                </div>
              ))}
            </div>

            <div className="mt-5 grid gap-5 lg:grid-cols-2">
              <div>
                <h3 className="text-sm font-semibold">Evidence traceability</h3>
                <p className="mt-2 text-xs text-[#8995a8]">
                  Source record IDs
                </p>
                <p className="mt-1 break-words text-xs leading-5 text-[#c3cedd]">
                  {selected.evidence?.source_record_ids?.join(', ') || '—'}
                </p>
                <p className="mt-3 text-xs text-[#8995a8]">
                  Canonical record IDs
                </p>
                <p className="mt-1 break-words text-xs leading-5 text-[#c3cedd]">
                  {selected.evidence?.canonical_record_ids?.join(', ') || '—'}
                </p>
              </div>
              <div>
                <h3 className="text-sm font-semibold">Method and quality</h3>
                <p className="mt-2 text-xs text-[#8995a8]">
                  Aggregation method
                </p>
                <p className="mt-1 text-xs leading-5 text-[#c3cedd]">
                  {selected.evidence?.aggregation_method || '—'}
                </p>
                <div className="mt-3">
                  <StatusLabel value={selected.quality_status} />
                </div>
                {selected.limitation && (
                  <ul className="mt-3 list-disc space-y-1 pl-5 text-xs leading-5 text-amber-200">
                    {(Array.isArray(selected.limitation)
                      ? selected.limitation
                      : [selected.limitation]
                    ).map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </section>
        )}

        <section className="grid gap-5 lg:grid-cols-2">
          <div className="rounded-2xl border border-[#263244] bg-[#101622] p-5">
            <p className="text-xs font-semibold uppercase tracking-widest text-[#55a6ff]">
              Validation evidence
            </p>
            <h2 className="mt-2 text-lg font-semibold">
              Recorded validation outcomes
            </h2>
            <div className="mt-4 space-y-3 text-sm">
              <div className="flex items-center justify-between gap-3">
                <span className="text-[#aab5c5]">Analytical validation</span>
                <StatusLabel value={validation?.analytical_validation?.status || 'unknown'} />
              </div>
              <div className="flex items-center justify-between gap-3">
                <span className="text-[#aab5c5]">Baseline reconciliation</span>
                <StatusLabel value={validation?.reconciliation_validation?.status || 'unknown'} />
              </div>
              <div className="flex items-center justify-between gap-3">
                <span className="text-[#aab5c5]">Overall validation</span>
                <StatusLabel value={validation?.overall_status || 'unknown'} />
              </div>
              <p className="border-t border-[#263244] pt-3 text-xs leading-5 text-[#8995a8]">
                Combined validation: {number(validation?.passed_count)} passed,
                {' '}{number(validation?.failed_count)} failed. Sensitivity
                assessment is reported separately and is not included in this
                check total.
              </p>
              <p className="text-xs text-[#8995a8]">
                Reconciliation report: {reconciliation?.overall_status || '—'}
                {' · '}{number(reconciliation?.total_checks)} checks
              </p>
              <p className="text-xs text-[#8995a8]">
                Weak-case review: {number(weakCases?.weak_case_count)} findings
                below the minimum evidence threshold.
              </p>
            </div>
          </div>

          <div className="rounded-2xl border border-amber-400/25 bg-[#101622] p-5">
            <p className="text-xs font-semibold uppercase tracking-widest text-amber-300">
              Sensitivity assessment
            </p>
            <h2 className="mt-2 text-lg font-semibold">
              Single-scenario sensitivity review
            </h2>
            <p className="mt-3 text-sm text-[#c3cedd]">
              {sensitivity?.test_design || '—'}
            </p>
            <div className="mt-4 grid grid-cols-2 gap-3">
              {[
                ['Rank changes', sensitivity?.rank_changed_count],
                ['Variance changes', sensitivity?.variance_changed_count],
                ['Status changes', sensitivity?.quality_status_changed_count],
                ['Newly insufficient', sensitivity?.newly_insufficient_evidence_count],
              ].map(([name, value]) => (
                <div key={String(name)} className="rounded-xl bg-[#0b111c] p-3">
                  <p className="text-xs text-[#8995a8]">{name}</p>
                  <p className="mt-1 text-xl font-semibold text-amber-200">
                    {number(typeof value === 'number' ? value : undefined)}
                  </p>
                </div>
              ))}
            </div>
            <p className="mt-4 text-xs leading-5 text-[#aab5c5]">
              {sensitivity?.interpretation}
            </p>
            <p className="mt-2 text-xs leading-5 text-amber-200">
              This is one descriptive removal scenario, not a statistical
              robustness test or proof of population-level validity.
            </p>
          </div>
        </section>

        <section className="rounded-2xl border border-[#263244] bg-[#101622] p-5">
          <p className="text-xs font-semibold uppercase tracking-widest text-[#55a6ff]">
            Methodology and limitations
          </p>
          <h2 className="mt-2 text-lg font-semibold">
            How to interpret these results
          </h2>
          <p className="mt-3 text-sm leading-6 text-[#c3cedd]">
            {summary?.baseline_method}
          </p>
          <p className="mt-3 text-sm leading-6 text-[#aab5c5]">
            Variance is Actual minus Budget. Positive variance indicates
            overspending; negative variance indicates underspending. Absolute
            variance and percentage variance are shown separately. Budget,
            Actual, Committed, and Forecast remain separate measures.
          </p>
          <ul className="mt-4 list-disc space-y-2 pl-5 text-sm leading-6 text-[#aab5c5]">
            {(summary?.important_limitations || summary?.limitations || []).map(
              (item: string, index: number) => (
                <li key={index}>{item}</li>
              ),
            )}
          </ul>
        </section>

        <section className="flex flex-wrap items-center justify-between gap-3 border-t border-[#263244] py-5 text-xs text-[#8995a8]">
          <div>
            <p>Data generated: {dateLabel(metadata?.generated_at)}</p>
            <p className="mt-1">
              Findings: {number(metadata?.result_count)} · Validation status:{' '}
              {metadata?.validation_status || '—'}
            </p>
          </div>
          <p>Read-only view of approved Track A outputs</p>
        </section>
      </div>
    </main>
  );
}
