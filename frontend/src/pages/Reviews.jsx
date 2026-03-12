import React, { useState, useEffect } from 'react'
import { reviewsApi } from '../api/client'

function Reviews() {
  const [reviews, setReviews] = useState([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(0)
  const limit = 20

  useEffect(() => {
    loadReviews()
  }, [page])

  const loadReviews = async () => {
    try {
      setLoading(true)
      const res = await reviewsApi.getReviews(limit, page * limit)
      setReviews(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const getRatingStars = (rating) => {
    return '★'.repeat(rating) + '☆'.repeat(5 - rating)
  }

  const getRatingColor = (rating) => {
    if (rating <= 2) return '#e74c3c'
    if (rating === 3) return '#f39c12'
    return '#27ae60'
  }

  if (loading) return <div style={{ textAlign: 'center', padding: '2rem' }}>Loading...</div>

  return (
    <div>
      <h2 style={{ marginBottom: '1.5rem', color: '#2c3e50' }}>Processed Reviews</h2>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {reviews.map((review, i) => (
          <div key={review.id || i} style={{
            backgroundColor: 'white',
            padding: '1.5rem',
            borderRadius: '8px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <span style={{
                fontSize: '1.2rem',
                color: getRatingColor(review.rating),
              }}>
                {getRatingStars(review.rating)}
              </span>
              <span style={{ color: '#888', fontSize: '0.9rem' }}>
                {review.review_date?.split('T')[0]}
              </span>
            </div>
            
            {review.title && (
              <h4 style={{ color: '#2c3e50', marginBottom: '0.5rem' }}>{review.title}</h4>
            )}
            
            <p style={{ color: '#555', lineHeight: '1.6' }}>{review.text}</p>
            
            {review.app_version && (
              <p style={{ color: '#888', fontSize: '0.85rem', marginTop: '0.75rem' }}>
                App Version: {review.app_version}
              </p>
            )}
          </div>
        ))}
      </div>

      {/* Pagination */}
      <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginTop: '2rem' }}>
        <button
          onClick={() => setPage(p => Math.max(0, p - 1))}
          disabled={page === 0}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: page === 0 ? '#ccc' : '#3498db',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: page === 0 ? 'not-allowed' : 'pointer',
          }}
        >
          ← Previous
        </button>
        <span style={{ padding: '0.5rem 1rem', color: '#666' }}>
          Page {page + 1}
        </span>
        <button
          onClick={() => setPage(p => p + 1)}
          disabled={reviews.length < limit}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: reviews.length < limit ? '#ccc' : '#3498db',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: reviews.length < limit ? 'not-allowed' : 'pointer',
          }}
        >
          Next →
        </button>
      </div>
    </div>
  )
}

export default Reviews
