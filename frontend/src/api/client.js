import axios from 'axios'

// Streamlit Cloud backend URL
const API_BASE_URL = 'https://groww-reviews-pulse-ejz7vvesnkrmpkms6ridug.streamlit.app/api'

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const reviewsApi = {
  getReviews: (limit = 100, offset = 0) => 
    client.get(`/reviews?limit=${limit}&offset=${offset}`),
  
  getStats: () => 
    client.get('/reviews/stats'),
}

export const reportsApi = {
  getLatest: () => 
    client.get('/reports/latest'),
  
  getList: () => 
    client.get('/reports/list'),
  
  getById: (id) => 
    client.get(`/reports/${id}`),
}

export const emailApi = {
  sendReport: (toEmail, subject, reportId = 'latest') => 
    client.post('/email/send-report', {
      to_email: toEmail,
      subject: subject,
      report_id: reportId,
    }),
}

export default client
