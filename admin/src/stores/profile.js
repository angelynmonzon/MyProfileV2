import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useProfileStore = defineStore('profile', () => {
  const profile = ref(null)
  const experiences = ref([])
  const education = ref([])
  const projects = ref([])
  const loading = ref(false)
  const error = ref(null)

  const authStore = useAuthStore()

  const api = axios.create({
    baseURL: '/api',
    headers: {
      'Content-Type': 'application/json'
    }
  })

  api.interceptors.request.use((config) => {
    if (authStore.token) {
      config.headers.Authorization = `Token ${authStore.token}`
    }
    return config
  })

  const fetchMyProfile = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/profiles/my_profile/')
      profile.value = response.data
      experiences.value = response.data.experiences || []
      education.value = response.data.education || []
      projects.value = response.data.projects || []
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch profile'
      console.error('Fetch profile error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createProfile = async (profileData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/profiles/', profileData)
      profile.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data || 'Failed to create profile'
      console.error('Create profile error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateProfile = async (profileData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.patch(`/profiles/${profile.value.id}/`, profileData)
      profile.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data || 'Failed to update profile'
      console.error('Update profile error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchExperiences = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/experiences/')
      experiences.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch experiences'
      console.error('Fetch experiences error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createExperience = async (experienceData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/experiences/', experienceData)
      experiences.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data || 'Failed to create experience'
      console.error('Create experience error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateExperience = async (id, experienceData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.put(`/experiences/${id}/`, experienceData)
      const index = experiences.value.findIndex(e => e.id === id)
      if (index !== -1) {
        experiences.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data || 'Failed to update experience'
      console.error('Update experience error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteExperience = async (id) => {
    loading.value = true
    error.value = null
    try {
      await api.delete(`/experiences/${id}/`)
      experiences.value = experiences.value.filter(e => e.id !== id)
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to delete experience'
      console.error('Delete experience error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchEducation = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/education/')
      education.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch education'
      console.error('Fetch education error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createEducation = async (educationData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/education/', educationData)
      education.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data || 'Failed to create education'
      console.error('Create education error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateEducation = async (id, educationData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.put(`/education/${id}/`, educationData)
      const index = education.value.findIndex(e => e.id === id)
      if (index !== -1) {
        education.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data || 'Failed to update education'
      console.error('Update education error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteEducation = async (id) => {
    loading.value = true
    error.value = null
    try {
      await api.delete(`/education/${id}/`)
      education.value = education.value.filter(e => e.id !== id)
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to delete education'
      console.error('Delete education error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchProjects = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/projects/')
      projects.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch projects'
      console.error('Fetch projects error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createProject = async (projectData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/projects/', projectData)
      projects.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data || 'Failed to create project'
      console.error('Create project error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateProject = async (id, projectData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.put(`/projects/${id}/`, projectData)
      const index = projects.value.findIndex(p => p.id === id)
      if (index !== -1) {
        projects.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data || 'Failed to update project'
      console.error('Update project error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteProject = async (id) => {
    loading.value = true
    error.value = null
    try {
      await api.delete(`/projects/${id}/`)
      projects.value = projects.value.filter(p => p.id !== id)
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to delete project'
      console.error('Delete project error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    profile,
    experiences,
    education,
    projects,
    loading,
    error,
    fetchMyProfile,
    createProfile,
    updateProfile,
    fetchExperiences,
    createExperience,
    updateExperience,
    deleteExperience,
    fetchEducation,
    createEducation,
    updateEducation,
    deleteEducation,
    fetchProjects,
    createProject,
    updateProject,
    deleteProject
  }
})
