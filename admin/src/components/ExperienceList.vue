<template>
  <div class="experience-list">
    <div v-if="loading" class="loading">Loading experiences...</div>
    
    <div v-else>
      <div v-for="experience in experiences" :key="experience.id" class="experience-item">
        <div class="experience-header">
          <h3>{{ experience.job_title }} at {{ experience.company }}</h3>
          <div class="experience-actions">
            <button @click="editExperience(experience)" class="btn btn-small btn-secondary">Edit</button>
            <button @click="deleteExperience(experience.id)" class="btn btn-small btn-danger">Delete</button>
          </div>
        </div>
        <div class="experience-details">
          <p><strong>Location:</strong> {{ experience.location || 'Not specified' }}</p>
          <p><strong>Period:</strong> {{ formatDate(experience.start_date) }} - {{ experience.is_current ? 'Present' : formatDate(experience.end_date) }}</p>
          <p><strong>Description:</strong> {{ experience.description }}</p>
        </div>
      </div>
      
      <button @click="showForm = true" class="btn btn-primary">Add Experience</button>
    </div>

    <!-- Experience Form Modal -->
    <div v-if="showForm" class="modal">
      <div class="modal-content">
        <h2>{{ editingExperience ? 'Edit Experience' : 'Add Experience' }}</h2>
        <form @submit.prevent="saveExperience" class="experience-form">
          <div class="form-group">
            <label>Job Title</label>
            <input v-model="formData.job_title" type="text" required />
          </div>
          <div class="form-group">
            <label>Company</label>
            <input v-model="formData.company" type="text" required />
          </div>
          <div class="form-group">
            <label>Location</label>
            <input v-model="formData.location" type="text" />
          </div>
          <div class="form-group">
            <label>Start Date</label>
            <input v-model="formData.start_date" type="date" required />
          </div>
          <div class="form-group">
            <label>End Date</label>
            <input v-model="formData.end_date" type="date" :disabled="formData.is_current" />
          </div>
          <div class="form-group checkbox">
            <label>
              <input v-model="formData.is_current" type="checkbox" />
              Currently working here
            </label>
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="formData.description" rows="4" required></textarea>
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

export default {
  name: 'ExperienceList',
  setup() {
    const profileStore = useProfileStore()
    
    const experiences = ref([])
    const loading = ref(false)
    const showForm = ref(false)
    const editingExperience = ref(null)
    
    const formData = ref({
      job_title: '',
      company: '',
      location: '',
      start_date: '',
      end_date: '',
      is_current: false,
      description: ''
    })

    const loadExperiences = async () => {
      loading.value = true
      try {
        await profileStore.fetchExperiences()
        experiences.value = profileStore.experiences
      } catch (err) {
        console.error('Failed to load experiences:', err)
      } finally {
        loading.value = false
      }
    }

    const saveExperience = async () => {
      try {
        if (editingExperience.value) {
          await profileStore.updateExperience(editingExperience.value.id, formData.value)
        } else {
          await profileStore.createExperience(formData.value)
        }
        closeForm()
        loadExperiences()
      } catch (err) {
        alert('Failed to save experience: ' + (err.response?.data?.detail || err.message))
      }
    }

    const editExperience = (experience) => {
      editingExperience.value = experience
      formData.value = {
        job_title: experience.job_title,
        company: experience.company,
        location: experience.location,
        start_date: experience.start_date,
        end_date: experience.end_date,
        is_current: experience.is_current,
        description: experience.description
      }
      showForm.value = true
    }

    const deleteExperience = async (id) => {
      if (confirm('Are you sure you want to delete this experience?')) {
        try {
          await profileStore.deleteExperience(id)
          loadExperiences()
        } catch (err) {
          alert('Failed to delete experience: ' + (err.response?.data?.detail || err.message))
        }
      }
    }

    const closeForm = () => {
      showForm.value = false
      editingExperience.value = null
      formData.value = {
        job_title: '',
        company: '',
        location: '',
        start_date: '',
        end_date: '',
        is_current: false,
        description: ''
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'Not specified'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
    }

    onMounted(() => {
      loadExperiences()
    })

    return {
      experiences,
      loading,
      showForm,
      editingExperience,
      formData,
      saveExperience,
      editExperience,
      deleteExperience,
      closeForm,
      formatDate
    }
  }
}
</script>

<style scoped>
.experience-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.experience-item {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #3498db;
}

.experience-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.experience-header h3 {
  margin: 0;
  color: #2c3e50;
}

.experience-actions {
  display: flex;
  gap: 0.5rem;
}

.experience-details p {
  margin: 0.5rem 0;
  color: #555;
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

.experience-form {
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

.form-group input:disabled {
  background-color: #f5f5f5;
}

.form-group.checkbox {
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
}

.form-group.checkbox input {
  width: auto;
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
