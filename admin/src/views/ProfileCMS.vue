<template>
  <div class="profile-cms">
    <h1>Profile Management</h1>
    
    <div v-if="loading" class="loading">Loading...</div>
    
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else class="profile-content">
      <!-- Basic Profile Information -->
      <div class="section">
        <h2>Basic Information</h2>
        <form @submit.prevent="saveProfile" class="profile-form">
          <div class="form-group">
            <label>Full Name</label>
            <input v-model="profileData.full_name" type="text" />
          </div>
          <div class="form-group">
            <label>Professional Title</label>
            <input v-model="profileData.title" type="text" placeholder="e.g., Virtual Assistant" required />
          </div>
          <div class="form-group">
            <label>Hero Description <small>(shown on the landing page hero section)</small></label>
            <textarea v-model="profileData.hero_description" rows="3" placeholder="Short tagline or intro shown below your name on the homepage"></textarea>
          </div>
          <div class="form-group">
            <label>Bio <small>(shown on the About section)</small></label>
            <textarea v-model="profileData.bio" rows="4" placeholder="Short professional biography"></textarea>
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="profileData.email" type="email" />
          </div>
          <div class="form-group">
            <label>Phone</label>
            <input v-model="profileData.phone" type="text" />
          </div>
          <div class="form-group">
            <label>Location</label>
            <input v-model="profileData.location" type="text" />
          </div>
          <div class="form-group">
            <label>Website URL</label>
            <input v-model="profileData.website_url" type="url" />
          </div>
          <div class="form-group checkbox">
            <label>
              <input v-model="profileData.is_available" type="checkbox" />
              Available for new projects
            </label>
          </div>
          <button type="submit" class="btn btn-primary">Save Profile</button>
        </form>
      </div>

      <!-- Social Media Links -->
      <div class="section">
        <h2>Social Media Links</h2>
        <form @submit.prevent="saveProfile" class="profile-form">
          <div class="form-group">
            <label>LinkedIn URL</label>
            <input v-model="profileData.linkedin_url" type="url" />
          </div>
          <div class="form-group">
            <label>Facebook URL</label>
            <input v-model="profileData.facebook_url" type="url" />
          </div>
          <div class="form-group">
            <label>Instagram URL</label>
            <input v-model="profileData.instagram_url" type="url" />
          </div>
          <div class="form-group">
            <label>Twitter URL</label>
            <input v-model="profileData.twitter_url" type="url" />
          </div>
          <div class="form-group">
            <label>GitHub URL</label>
            <input v-model="profileData.github_url" type="url" />
          </div>
          <button type="submit" class="btn btn-primary">Save Links</button>
        </form>
      </div>

      <!-- Services Offered -->
      <div class="section">
        <h2>Services Offered</h2>
        <div class="services-list">
          <div v-for="(service, index) in profileData.services_offered" :key="index" class="service-item service-item-block">
            <div class="service-item-fields">
              <div class="service-field">
                <label>Icon</label>
                <input v-model="service.icon" type="text" placeholder="e.g. 📱" style="width:70px" />
              </div>
              <div class="service-field" style="flex:1">
                <label>Title</label>
                <input v-model="service.title" type="text" placeholder="Service title" />
              </div>
            </div>
            <div class="service-field">
              <label>Description</label>
              <textarea v-model="service.description" rows="2" placeholder="What this service includes..."></textarea>
            </div>
            <button @click="removeService(index)" class="btn btn-danger btn-small">Remove</button>
          </div>
          <button @click="addService" class="btn btn-secondary">+ Add Service</button>
        </div>
        <button @click="saveProfile" class="btn btn-primary">Save Services</button>
      </div>

      <!-- Skills -->
      <div class="section">
        <h2>Skills</h2>
        <div class="skills-list">
          <div v-for="(skill, index) in profileData.skills" :key="index" class="skill-item">
            <input v-model="profileData.skills[index]" type="text" />
            <button @click="removeSkill(index)" class="btn btn-danger">Remove</button>
          </div>
          <button @click="addSkill" class="btn btn-secondary">Add Skill</button>
        </div>
        <button @click="saveProfile" class="btn btn-primary">Save Skills</button>
      </div>

      <!-- Work Experience -->
      <div class="section">
        <h2>Work Experience</h2>
        <ExperienceList />
      </div>

      <!-- Education -->
      <div class="section">
        <h2>Education</h2>
        <EducationList />
      </div>

      <!-- Portfolio Projects -->
      <div class="section">
        <h2>Portfolio Projects</h2>
        <ProjectList />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useProfileStore } from '../stores/profile'
import ExperienceList from '../components/ExperienceList.vue'
import EducationList from '../components/EducationList.vue'
import ProjectList from '../components/ProjectList.vue'

export default {
  name: 'ProfileCMS',
  components: {
    ExperienceList,
    EducationList,
    ProjectList
  },
  setup() {
    const profileStore = useProfileStore()
    
    const profileData = ref({
      full_name: '',
      title: '',
      hero_description: '',
      bio: '',
      email: '',
      phone: '',
      location: '',
      website_url: '',
      linkedin_url: '',
      facebook_url: '',
      instagram_url: '',
      twitter_url: '',
      github_url: '',
      services_offered: [],
      skills: [],
      is_available: true
    })

    const loading = ref(false)
    const error = ref(null)

    const loadProfile = async () => {
      loading.value = true
      error.value = null
      try {
        const data = await profileStore.fetchMyProfile()
        if (data) {
          profileData.value = {
            full_name: data.full_name || '',
            title: data.title || '',
            hero_description: data.hero_description || '',
            bio: data.bio || '',
            email: data.email || '',
            phone: data.phone || '',
            location: data.location || '',
            website_url: data.website_url || '',
            linkedin_url: data.linkedin_url || '',
            facebook_url: data.facebook_url || '',
            instagram_url: data.instagram_url || '',
            twitter_url: data.twitter_url || '',
            github_url: data.github_url || '',
            services_offered: data.services_offered || [],
            skills: data.skills || [],
            is_available: data.is_available !== undefined ? data.is_available : true
          }
        }
      } catch (err) {
        if (err.response?.status === 404) {
          // Profile doesn't exist yet, that's okay
          error.value = null
        } else {
          error.value = err.message || 'Failed to load profile'
        }
      } finally {
        loading.value = false
      }
    }

    const saveProfile = async () => {
      loading.value = true
      error.value = null
      try {
        if (profileStore.profile) {
          await profileStore.updateProfile(profileData.value)
        } else {
          await profileStore.createProfile(profileData.value)
        }
        alert('Profile saved successfully!')
      } catch (err) {
        error.value = err.message || 'Failed to save profile'
        alert('Failed to save profile: ' + error.value)
      } finally {
        loading.value = false
      }
    }

    const addService = () => {
      profileData.value.services_offered.push({ icon: '', title: '', description: '' })
    }

    const removeService = (index) => {
      profileData.value.services_offered.splice(index, 1)
    }

    const addSkill = () => {
      profileData.value.skills.push('')
    }

    const removeSkill = (index) => {
      profileData.value.skills.splice(index, 1)
    }

    onMounted(() => {
      loadProfile()
    })

    return {
      profileData,
      loading,
      error,
      saveProfile,
      addService,
      removeService,
      addSkill,
      removeSkill
    }
  }
}
</script>

<style scoped>
.profile-cms {
  max-width: 900px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 2rem;
  color: #2c3e50;
}

h2 {
  margin-bottom: 1rem;
  color: #34495e;
  border-bottom: 2px solid #3498db;
  padding-bottom: 0.5rem;
}

.section {
  background: white;
  padding: 2rem;
  margin-bottom: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.profile-form {
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

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3498db;
}

.form-group.checkbox {
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
}

.form-group.checkbox input {
  width: auto;
}

.services-list,
.skills-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.service-item,
.skill-item {
  display: flex;
  gap: 0.5rem;
}

.service-item input,
.skill-item input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.service-item-block {
  flex-direction: column;
  background: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  gap: 0.75rem;
}

.service-item-fields {
  display: flex;
  gap: 0.75rem;
  align-items: flex-end;
}

.service-field {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.service-field label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #555;
}

.service-field input,
.service-field textarea {
  padding: 0.5rem 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.95rem;
  width: 100%;
}

.service-field textarea {
  resize: vertical;
}

.btn-small {
  padding: 0.35rem 0.75rem;
  font-size: 0.82rem;
  align-self: flex-end;
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
  padding: 0.5rem 1rem;
}

.btn-danger:hover {
  background-color: #c0392b;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
}

.error {
  background-color: #fee;
  color: #c0392b;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}
</style>
