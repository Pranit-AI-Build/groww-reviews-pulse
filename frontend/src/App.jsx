import React from 'react'
import { Routes, Route, Link, useLocation } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Reports from './pages/Reports'
import Reviews from './pages/Reviews'

function App() {
  const location = useLocation()
  
  const isActive = (path) => location.pathname === path

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f8f9fa' }}>
      {/* Navigation */}
      <nav style={{
        backgroundColor: 'white',
        padding: '0 2rem',
        borderBottom: '1px solid #e9ecef',
        position: 'sticky',
        top: 0,
        zIndex: 100,
      }}>
        <div style={{
          maxWidth: '1400px',
          margin: '0 auto',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          height: '64px',
        }}>
          {/* Logo */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div style={{
              width: '32px',
              height: '32px',
              backgroundColor: '#6366f1',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontWeight: 'bold',
            }}>G</div>
            <span style={{ fontSize: '1.25rem', fontWeight: '600', color: '#1f2937' }}>
              GrowwReviews
            </span>
          </div>
          
          {/* Nav Links */}
          <div style={{ display: 'flex', gap: '2rem' }}>
            <NavLink to="/" active={isActive('/')}>Dashboard</NavLink>
            <NavLink to="/reports" active={isActive('/reports')}>Reports</NavLink>
            <NavLink to="/reviews" active={isActive('/reviews')}>Reviews</NavLink>
          </div>
          
          {/* User Avatar */}
          <div style={{
            width: '36px',
            height: '36px',
            borderRadius: '50%',
            backgroundColor: '#6366f1',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontWeight: '500',
          }}>U</div>
        </div>
      </nav>

      {/* Main Content */}
      <main style={{
        maxWidth: '1400px',
        margin: '0 auto',
        padding: '2rem',
      }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/reviews" element={<Reviews />} />
        </Routes>
      </main>
      
      {/* Footer */}
      <footer style={{
        borderTop: '1px solid #e9ecef',
        padding: '1.5rem 2rem',
        marginTop: '3rem',
        backgroundColor: 'white',
      }}>
        <div style={{
          maxWidth: '1400px',
          margin: '0 auto',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          color: '#6b7280',
          fontSize: '0.875rem',
        }}>
          <span>© 2024 GrowwReviews AI Tool. All rights reserved.</span>
          <div style={{ display: 'flex', gap: '1.5rem' }}>
            <a href="#" style={{ color: '#6b7280', textDecoration: 'none' }}>Privacy Policy</a>
            <a href="#" style={{ color: '#6b7280', textDecoration: 'none' }}>Terms of Service</a>
            <a href="#" style={{ color: '#6b7280', textDecoration: 'none' }}>Support</a>
          </div>
        </div>
      </footer>
    </div>
  )
}

function NavLink({ to, children, active }) {
  return (
    <Link
      to={to}
      style={{
        color: active ? '#6366f1' : '#6b7280',
        textDecoration: 'none',
        fontWeight: '500',
        fontSize: '0.875rem',
        padding: '0.5rem 0',
        borderBottom: active ? '2px solid #6366f1' : '2px solid transparent',
        transition: 'all 0.2s',
      }}
    >
      {children}
    </Link>
  )
}

export default App
