import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' }
})

export const fetchPublicProfile = async () => {
  const response = await api.get('/profiles/public/')
  return response.data
}
