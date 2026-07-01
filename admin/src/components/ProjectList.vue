<template>
  <div class="project-list">
    <div v-if="loading" class="loading">Loading projects...</div>
    
    <div v-else>
      <div v-for="project in projects" :key="project.id" class="project-item">
        <div class="project-header">
          <h3>{{ project.title }}</h3>
          <div class="project-actions">
            <button @click="editProject(project)" class="btn btn-small btn-secondary">Edit</button>
            <button @click="deleteProject(project.id)" class="btn btn-small btn-danger">Delete</button>
          </div>
        </div>
        <div class="project-details">
          <div v-if="project.image" class="project-thumb">
            <img :src="'http://localhost:8000/media/' + project.image" :alt="project.title" />
          </div>
          <p><strong>Description:</strong> {{ project.description }}</p>
          <p v-if="project.project_url"><strong>Project URL:</strong> <a :href="project.project_url" target="_blank">{{ project.project_url }}</a></p>
          <p v-if="project.technologies && project.technologies.length">
            <strong>Technologies:</strong>
            <span v-for="(tech, index) in project.technologies" :key="index" class="tech-tag">
              {{ tech }}
            </span>
          </p>
        </div>
      </div>
      
      <button @click="showForm = true" class="btn btn-primary">Add Project</button>
    </div>

    <!-- Project Form Modal -->
    <div v-if="showForm" class="modal">
      <div class="modal-content">
        <h2>{{ editingProject ? 'Edit Project' : 'Add Project' }}</h2>
        <form @submit.prevent="saveProject" class="project-form">
          <div class="form-group">
            <label>Project Title</label>
            <input v-model="formData.title" type="text" required />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="formData.description" rows="4" required></textarea>
          </div>
          <div class="form-group">
            <label>Project URL</label>
            <input v-model="formData.project_url" type="url" placeholder="https://example.com" />
          </div>
          <div class="form-group">
            <label>Technologies (comma-separated)</label>
            <input v-model="technologiesInput" type="text" placeholder="React, Node.js, MongoDB" />
            <small>Enter technologies separated by commas</small>
          </div>
          <div class="form-group">
            <label>Project Image</label>
            <div class="image-upload-area" @click="triggerFileInput" @dragover.prevent @drop.prevent="onDrop">
              <input ref="fileInput" type="file" accept="image/*" @change="onFileChange" style="display:none" />
              <div v-if="imagePreview" class="image-preview">
                <img :src="imagePreview" alt="Preview" />
                <button type="button" class="remove-image" @click.stop="removeImage">✕</button>
              </div>
              <div v-else class="upload-placeholder">
                <span class="upload-icon">🖼️</span>
                <p>Click or drag & drop an image here</p>
                <small>JPG, PNG, WEBP — max 5MB</small>
              </div>
            </div>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary">Save</button>
            <button type="button" @click="closeForm" class="btn btn-secondary">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useProfileStore } from '../stores/profile'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'ProjectList',
  setup() {
    const profileStore = useProfileStore()
    
    const projects = ref([])
    const loading = ref(false)
    const showForm = ref(false)
    const editingProject = ref(null)
    const technologiesInput = ref('')
    
    const formData = ref({
      title: '',
      description: '',
      project_url: '',
      technologies: []
    })
    const fileInput = ref(null)
    const selectedFile = ref(null)
    const imagePreview = ref('')
    const authStore = useAuthStore()

    const triggerFileInput = () => fileInput.value?.click()

    const onFileChange = (e) => {
      const file = e.target.files[0]
      if (file) setFile(file)
    }

    const onDrop = (e) => {
      const file = e.dataTransfer.files[0]
      if (file && file.type.startsWith('image/')) setFile(file)
    }

    const setFile = (file) => {
      if (file.size > 5 * 1024 * 1024) {
        alert('Image must be under 5MB')
        return
      }
      selectedFile.value = file
      imagePreview.value = URL.createObjectURL(file)
    }

    const removeImage = () => {
      selectedFile.value = null
      imagePreview.value = ''
      if (fileInput.value) fileInput.value.value = ''
    }

    const loadProjects = async () => {
      loading.value = true
      try {
        await profileStore.fetchProjects()
        projects.value = profileStore.projects
      } catch (err) {
        console.error('Failed to load projects:', err)
      } finally {
        loading.value = false
      }
    }

    const saveProject = async () => {
      formData.value.technologies = technologiesInput.value
        .split(',')
        .map(t => t.trim())
        .filter(t => t.length > 0)

      try {
        const payload = new FormData()
        payload.append('title', formData.value.title)
        payload.append('description', formData.value.description)
        payload.append('project_url', formData.value.project_url || '')
        payload.append('technologies', JSON.stringify(formData.value.technologies))
        if (selectedFile.value) {
          payload.append('image', selectedFile.value)
        }

        const headers = {
          Authorization: `Token ${authStore.token}`
        }

        if (editingProject.value) {
          const res = await axios.patch(`/api/projects/${editingProject.value.id}/`, payload, { headers })
          const idx = profileStore.projects.findIndex(p => p.id === editingProject.value.id)
          if (idx !== -1) profileStore.projects[idx] = res.data
        } else {
          const res = await axios.post('/api/projects/', payload, { headers })
          profileStore.projects.push(res.data)
        }
        closeForm()
        loadProjects()
      } catch (err) {
        alert('Failed to save project: ' + (err.response?.data ? JSON.stringify(err.response.data) : err.message))
      }
    }

    const editProject = (project) => {
      editingProject.value = project
      formData.value = {
        title: project.title,
        description: project.description,
        project_url: project.project_url,
        technologies: project.technologies || []
      }
      technologiesInput.value = (project.technologies || []).join(', ')
      selectedFile.value = null
      imagePreview.value = project.image ? 'http://localhost:8000/media/' + project.image : ''
      showForm.value = true
    }

    const deleteProject = async (id) => {
      if (confirm('Are you sure you want to delete this project?')) {
        try {
          await profileStore.deleteProject(id)
          loadProjects()
        } catch (err) {
          alert('Failed to delete project: ' + (err.response?.data?.detail || err.message))
        }
      }
    }

    const closeForm = () => {
      showForm.value = false
      editingProject.value = null
      formData.value = {
        title: '',
        description: '',
        project_url: '',
        technologies: []
      }
      technologiesInput.value = ''
      selectedFile.value = null
      imagePreview.value = ''
      if (fileInput.value) fileInput.value.value = ''
    }

    onMounted(() => {
      loadProjects()
    })

    return {
      projects,
      loading,
      showForm,
      editingProject,
      formData,
      technologiesInput,
      fileInput,
      imagePreview,
      triggerFileInput,
      onFileChange,
      onDrop,
      removeImage,
      saveProject,
      editProject,
      deleteProject,
      closeForm
    }
  }
}
</script>

<style scoped>
.project-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.project-item {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #e67e22;
}

.project-thumb {
  margin-bottom: 0.75rem;
}

.project-thumb img {
  width: 100%;
  max-height: 180px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid #ddd;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.project-header h3 {
  margin: 0;
  color: #2c3e50;
}

.project-actions {
  display: flex;
  gap: 0.5rem;
}

.project-details p {
  margin: 0.5rem 0;
  color: #555;
}

.project-details a {
  color: #3498db;
  text-decoration: none;
}

.project-details a:hover {
  text-decoration: underline;
}

.tech-tag {
  display: inline-block;
  background: #3498db;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
  margin-right: 0.5rem;
  margin-top: 0.5rem;
}

.btn-small {
  padding: 0.4rem 0.8rem;
  font-size: 0.9rem;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
}

.project-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #2c3e50;
}

.form-group input,
.form-group textarea {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group small {
  color: #7f8c8d;
  font-size: 0.85rem;
}

.image-upload-area {
  border: 2px dashed #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: border-color 0.2s;
  overflow: hidden;
}

.image-upload-area:hover {
  border-color: #3498db;
}

.upload-placeholder {
  padding: 2rem;
  text-align: center;
  color: #95a5a6;
}

.upload-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 0.5rem;
}

.upload-placeholder p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
  color: #555;
}

.image-preview {
  position: relative;
}

.image-preview img {
  width: 100%;
  max-height: 220px;
  object-fit: cover;
  display: block;
}

.remove-image {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: rgba(231,76,60,0.85);
  color: white;
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  font-size: 0.85rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-image:hover {
  background: #c0392b;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.btn-danger {
  background-color: #e74c3c;
  color: white;
}

.btn-danger:hover {
  background-color: #c0392b;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
}
</style>
