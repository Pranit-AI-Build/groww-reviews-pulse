import React, { useState, useEffect } from 'react'
import { reviewsApi, reportsApi } from '../api/client'

function Dashboard() {
  const [stats, setStats] = useState(null)
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [emailForm, setEmailForm] = useState({ 
    to: '', 
    subject: 'Weekly Product Insight Summary - Negative Reviews' 
  })
  const [sending, setSending] = useState(false)
  const [sendResult, setSendResult] = useState(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [statsRes, reportRes] = await Promise.all([
        reviewsApi.getStats(),
        reportsApi.getLatest(),
      ])
      setStats(statsRes.data)
      setReport(reportRes.data)
    } catch (err) {
      console.error('Failed to load data:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSendEmail = async (e) => {
    e.preventDefault()
    try {
      setSending(true)
      const { emailApi } = await import('../api/client')
      const res = await emailApi.sendReport(emailForm.to, emailForm.subject)
      setSendResult(res.data)
    } catch (err) {
      setSendResult({ success: false, message: 'Failed to send email' })
    } finally {
      setSending(false)
    }
  }

  if (loading) return <div style={{ textAlign: 'center', padding: '3rem', color: '#6b7280' }}>Loading...</div>

  return (
    <div>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: '600', color: '#1f2937', marginBottom: '0.5rem' }}>
            Weekly Product Insight Summary
          </h1>
        </div>
        <button
          onClick={loadData}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.625rem 1rem',
            backgroundColor: '#6366f1',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            fontSize: '0.875rem',
            fontWeight: '500',
            cursor: 'pointer',
          }}
        >
          <span>↻</span> Refresh Analysis
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 380px', gap: '2rem' }}>
        {/* Left Column */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          {/* Top 3 Themes */}
          <section style={{ backgroundColor: 'white', borderRadius: '12px', padding: '1.5rem', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem' }}>
              <span style={{ color: '#f59e0b', fontSize: '1.25rem' }}>🔥</span>
              <h2 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1f2937' }}>Top 3 Themes</h2>
            </div>
            
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem' }}>
              {report?.themes?.slice(0, 3).map((theme, i) => (
                <ThemeCard key={i} theme={theme} index={i} />
              ))}
            </div>
          </section>

          {/* User Quotes & Actions */}
          <section style={{ backgroundColor: 'white', borderRadius: '12px', padding: '1.5rem', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            {/* Quotes Section */}
            <div style={{ marginBottom: '2rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                <span style={{ color: '#6366f1', fontSize: '1.25rem' }}>❝</span>
                <h2 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1f2937' }}>Representative User Quotes</h2>
              </div>
              
              {/* Single Box for All Quotes */}
              <div style={{
                backgroundColor: '#f9fafb',
                borderRadius: '8px',
                padding: '1.25rem',
                border: '1px solid #e5e7eb'
              }}>
                {report?.quotes?.map((quote, i) => (
                  <div key={i} style={{
                    paddingBottom: i < report.quotes.length - 1 ? '1rem' : '0',
                    marginBottom: i < report.quotes.length - 1 ? '1rem' : '0',
                    borderBottom: i < report.quotes.length - 1 ? '1px solid #e5e7eb' : 'none'
                  }}>
                    <p style={{ 
                      fontSize: '0.9375rem', 
                      color: '#374151', 
                      lineHeight: '1.6', 
                      marginBottom: '0.5rem',
                      fontStyle: 'italic',
                      margin: '0 0 0.5rem 0'
                    }}>
                      "{quote.text}"
                    </p>
                    <p style={{ 
                      fontSize: '0.75rem', 
                      color: '#9ca3af',
                      margin: 0
                    }}>
                      — Verified User, {quote.rating || 1} Star Review
                    </p>
                  </div>
                ))}
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem' }}>
              <span style={{ color: '#10b981', fontSize: '1.25rem' }}>💡</span>
              <h2 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1f2937' }}>Suggested Action Ideas</h2>
            </div>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {report?.actions?.map((action, i) => (
                <ActionCard key={i} action={action} index={i} />
              ))}
            </div>
          </section>
        </div>

        {/* Right Column - Send Report Panel */}
        <div style={{ position: 'sticky', top: '80px', height: 'fit-content' }}>
          <div style={{ backgroundColor: 'white', borderRadius: '12px', padding: '1.5rem', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem' }}>
              <span style={{ color: '#6366f1', fontSize: '1.25rem' }}>📧</span>
              <h2 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1f2937' }}>Send Report</h2>
            </div>
            
            <form onSubmit={handleSendEmail} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: '#374151', marginBottom: '0.375rem' }}>
                  Recipient Email
                </label>
                <input
                  type="email"
                  value={emailForm.to}
                  onChange={(e) => setEmailForm({ ...emailForm, to: e.target.value })}
                  placeholder="product-team@company.com"
                  required
                  style={{
                    width: '100%',
                    padding: '0.625rem',
                    border: '1px solid #d1d5db',
                    borderRadius: '8px',
                    fontSize: '0.875rem',
                  }}
                />
              </div>
              
              <div>
                <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: '#374151', marginBottom: '0.375rem' }}>
                  Subject
                </label>
                <input
                  type="text"
                  value={emailForm.subject}
                  onChange={(e) => setEmailForm({ ...emailForm, subject: e.target.value })}
                  required
                  style={{
                    width: '100%',
                    padding: '0.625rem',
                    border: '1px solid #d1d5db',
                    borderRadius: '8px',
                    fontSize: '0.875rem',
                  }}
                />
              </div>
              
              {/* Preview Summary */}
              <div style={{ backgroundColor: '#f9fafb', borderRadius: '8px', padding: '1rem', marginTop: '0.5rem' }}>
                <h4 style={{ fontSize: '0.75rem', fontWeight: '600', color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>
                  Summary Overview
                </h4>
                <p style={{ fontSize: '0.875rem', color: '#4b5563', marginBottom: '0.75rem' }}>
                  This week we analyzed {stats?.total_reviews || 0} negative reviews. The core issues remain technical stability and performance.
                </p>
                <h5 style={{ fontSize: '0.75rem', fontWeight: '600', color: '#1f2937', marginBottom: '0.5rem' }}>KEY THEMES:</h5>
                <ul style={{ fontSize: '0.875rem', color: '#4b5563', paddingLeft: '1.25rem', margin: 0 }}>
                  {report?.themes?.slice(0, 3).map((theme, i) => (
                    <li key={i}>{theme.name}</li>
                  ))}
                </ul>
              </div>
              
              <button
                type="submit"
                disabled={sending}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '0.5rem',
                  width: '100%',
                  padding: '0.75rem',
                  backgroundColor: '#6366f1',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  fontSize: '0.875rem',
                  fontWeight: '500',
                  cursor: sending ? 'not-allowed' : 'pointer',
                  opacity: sending ? 0.7 : 1,
                  marginTop: '0.5rem',
                }}
              >
                <span>📧</span> {sending ? 'Sending...' : 'Send Email'}
              </button>
              
              {sendResult && (
                <div style={{
                  padding: '0.75rem',
                  borderRadius: '8px',
                  fontSize: '0.875rem',
                  backgroundColor: sendResult.success ? '#d1fae5' : '#fee2e2',
                  color: sendResult.success ? '#065f46' : '#991b1b',
                }}>
                  {sendResult.message}
                </div>
              )}
              
              <p style={{ fontSize: '0.75rem', color: '#9ca3af', textAlign: 'center', marginTop: '0.5rem' }}>
                The report will be sent as a PDF attachment with a summarized HTML body.
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

function ThemeCard({ theme, index }) {
  const bgColors = ['#fef2f2', '#fffbeb', '#eff6ff']
  const icons = ['🔥', '⚡', '💡']
  
  return (
    <div style={{
      backgroundColor: bgColors[index] || '#f9fafb',
      borderRadius: '12px',
      padding: '1.25rem',
      border: '1px solid #e5e7eb',
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '0.75rem',
      }}>
        <span style={{
          fontSize: '0.625rem',
          fontWeight: '600',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          color: '#6b7280',
        }}>
          Theme {index + 1}
        </span>
        <span style={{ fontSize: '1rem' }}>{icons[index]}</span>
      </div>
      <h3 style={{ fontSize: '0.9375rem', fontWeight: '600', color: '#1f2937', marginBottom: '0.5rem' }}>
        {theme.name}
      </h3>
      <p style={{ fontSize: '0.8125rem', color: '#6b7280', lineHeight: '1.5' }}>
        {theme.description}
      </p>
    </div>
  )
}



function ActionCard({ action, index }) {
  return (
    <div style={{
      display: 'flex',
      gap: '1rem',
      padding: '1.25rem',
      backgroundColor: '#f0fdf4',
      borderRadius: '12px',
      border: '1px solid #d1fae5',
    }}>
      <div style={{
        width: '28px',
        height: '28px',
        borderRadius: '50%',
        backgroundColor: '#10b981',
        color: 'white',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '0.875rem',
        fontWeight: '600',
        flexShrink: 0,
      }}>
        {index + 1}
      </div>
      <div style={{ flex: 1 }}>
        <h4 style={{ fontSize: '0.9375rem', fontWeight: '600', color: '#1f2937', marginBottom: '0.375rem' }}>
          {action.title}
        </h4>
        <p style={{ fontSize: '0.8125rem', color: '#6b7280', lineHeight: '1.5' }}>
          {action.description}
        </p>
      </div>
    </div>
  )
}

export default Dashboard
