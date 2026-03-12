import React, { useState, useEffect } from 'react'
import { reportsApi, emailApi } from '../api/client'

function Reports() {
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [emailForm, setEmailForm] = useState({ to: '', subject: 'Weekly Pulse - Groww Reviews' })
  const [sending, setSending] = useState(false)
  const [sendResult, setSendResult] = useState(null)

  useEffect(() => {
    loadReport()
  }, [])

  const loadReport = async () => {
    try {
      setLoading(true)
      const res = await reportsApi.getLatest()
      setReport(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleSendEmail = async (e) => {
    e.preventDefault()
    try {
      setSending(true)
      const res = await emailApi.sendReport(emailForm.to, emailForm.subject)
      setSendResult(res.data)
    } catch (err) {
      setSendResult({ success: false, message: 'Failed to send email' })
    } finally {
      setSending(false)
    }
  }

  if (loading) return <div style={{ textAlign: 'center', padding: '2rem' }}>Loading...</div>
  if (!report) return <div style={{ padding: '2rem' }}>No reports found</div>

  return (
    <div>
      <h2 style={{ marginBottom: '1.5rem', color: '#2c3e50' }}>Weekly Pulse Report</h2>
      
      {/* Email Form */}
      <div style={{ backgroundColor: 'white', padding: '1.5rem', borderRadius: '8px', marginBottom: '2rem', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
        <h3 style={{ marginBottom: '1rem', color: '#2c3e50' }}>📧 Send Report via Email</h3>
        <form onSubmit={handleSendEmail} style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'flex-end' }}>
          <div style={{ flex: 1, minWidth: '200px' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.9rem', color: '#666' }}>To Email</label>
            <input
              type="email"
              value={emailForm.to}
              onChange={(e) => setEmailForm({ ...emailForm, to: e.target.value })}
              placeholder="recipient@example.com"
              required
              style={{ width: '100%', padding: '0.5rem', border: '1px solid #ddd', borderRadius: '4px' }}
            />
          </div>
          <div style={{ flex: 2, minWidth: '300px' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.9rem', color: '#666' }}>Subject</label>
            <input
              type="text"
              value={emailForm.subject}
              onChange={(e) => setEmailForm({ ...emailForm, subject: e.target.value })}
              required
              style={{ width: '100%', padding: '0.5rem', border: '1px solid #ddd', borderRadius: '4px' }}
            />
          </div>
          <button
            type="submit"
            disabled={sending}
            style={{
              padding: '0.5rem 1.5rem',
              backgroundColor: '#27ae60',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: sending ? 'not-allowed' : 'pointer',
              opacity: sending ? 0.7 : 1,
            }}
          >
            {sending ? 'Sending...' : 'Send Email'}
          </button>
        </form>
        
        {sendResult && (
          <div style={{
            marginTop: '1rem',
            padding: '1rem',
            backgroundColor: sendResult.success ? '#d4edda' : '#f8d7da',
            color: sendResult.success ? '#155724' : '#721c24',
            borderRadius: '4px',
          }}>
            {sendResult.message}
            {sendResult.report_summary && (
              <div style={{ marginTop: '0.5rem', fontSize: '0.9rem' }}>
                Themes: {sendResult.report_summary.themes} | 
                Quotes: {sendResult.report_summary.quotes} | 
                Actions: {sendResult.report_summary.actions}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Report Content */}
      <div style={{ backgroundColor: 'white', padding: '2rem', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
        <div style={{ marginBottom: '2rem', paddingBottom: '1rem', borderBottom: '2px solid #eee' }}>
          <h1 style={{ color: '#2c3e50' }}>Weekly Pulse - Groww Reviews</h1>
          <p style={{ color: '#666' }}>
            <strong>Week:</strong> {report.week_range} | 
            <strong>Reviews Analyzed:</strong> {report.total_reviews}
          </p>
        </div>

        {/* Themes */}
        <section style={{ marginBottom: '2rem' }}>
          <h2 style={{ color: '#2c3e50', marginBottom: '1rem' }}>Top 3 Themes</h2>
          {report.themes?.map((theme, i) => (
            <div key={i} style={{ 
              marginBottom: '1rem', 
              padding: '1rem', 
              backgroundColor: '#f8f9fa', 
              borderRadius: '6px',
              borderLeft: '4px solid #3498db'
            }}>
              <h3 style={{ color: '#2c3e50' }}>
                {i + 1}. {theme.name} 
                <span style={{ fontSize: '0.9rem', color: '#666', fontWeight: 'normal' }}>
                  ({theme.review_count} mentions)
                </span>
              </h3>
              <p style={{ color: '#555', margin: '0.5rem 0' }}>{theme.description}</p>
              <p style={{ fontSize: '0.9rem', color: '#888' }}>
                Sentiment: <strong>{theme.sentiment}</strong> | 
                Severity: <strong>{theme.severity}</strong>
              </p>
            </div>
          ))}
        </section>

        {/* Quotes */}
        <section style={{ marginBottom: '2rem' }}>
          <h2 style={{ color: '#2c3e50', marginBottom: '1rem' }}>User Voices</h2>
          {report.quotes?.map((quote, i) => (
            <blockquote key={i} style={{
              margin: '1rem 0',
              padding: '1rem 1.5rem',
              backgroundColor: '#f0f7ff',
              borderLeft: '4px solid #3498db',
              fontStyle: 'italic',
              borderRadius: '0 6px 6px 0',
            }}>
              <p style={{ marginBottom: '0.5rem' }}>"{quote.text}"</p>
              <footer style={{ fontSize: '0.9rem', color: '#666' }}>— {quote.theme}</footer>
            </blockquote>
          ))}
        </section>

        {/* Actions */}
        <section>
          <h2 style={{ color: '#2c3e50', marginBottom: '1rem' }}>Suggested Actions</h2>
          {report.actions?.map((action, i) => (
            <div key={i} style={{
              marginBottom: '1rem',
              padding: '1rem',
              backgroundColor: '#fff9e6',
              borderRadius: '6px',
              border: '1px solid #ffe082',
            }}>
              <h3 style={{ color: '#2c3e50' }}>
                {i + 1}. {action.title}
              </h3>
              <p style={{ color: '#555', margin: '0.5rem 0' }}>{action.description}</p>
              <p style={{ fontSize: '0.9rem', color: '#888' }}>
                Priority: <strong style={{ color: action.priority === 'high' ? '#e74c3c' : '#666' }}>{action.priority}</strong> | 
                Effort: <strong>{action.effort}</strong> | 
                Impact: <strong>{action.impact}</strong>
              </p>
            </div>
          ))}
        </section>
      </div>
    </div>
  )
}

export default Reports
