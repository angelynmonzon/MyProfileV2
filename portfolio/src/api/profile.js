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
    })),
    // Ensure show flags are preserved
    show_services: profile.show_services !== undefined ? profile.show_services : true,
    show_skills: profile.show_skills !== undefined ? profile.show_skills : true,
    show_experience: profile.show_experience !== undefined ? profile.show_experience : true,
    show_education: profile.show_education !== undefined ? profile.show_education : true,
    show_projects: profile.show_projects !== undefined ? profile.show_projects : true
  }
}

export const fetchPublicProfile = async () => {
  const response = await api.get('/profiles/public/')
  return response.data.map(normalizeProfile)
}
