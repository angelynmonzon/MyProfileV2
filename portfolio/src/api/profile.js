import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' }
})

const stripMediaHost = (url) => {
  if (!url) return url
  return url.replace(/^https?:\/\/[^/]+/, '')
}

const normalizeProfile = (profile) => {
  if (!profile) return profile
  return {
    ...profile,
    profile_image: stripMediaHost(profile.profile_image),
    about_image: stripMediaHost(profile.about_image),
    projects: (profile.projects || []).map(p => ({
      ...p,
      image: stripMediaHost(p.image)
    }))
  }
}

export const fetchPublicProfile = async () => {
  const response = await api.get('/profiles/public/')
  return response.data.map(normalizeProfile)
}
