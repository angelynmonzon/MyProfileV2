<template>
  <div class="profile-cms">
    <h1>Profile Management</h1>

    <div v-if="loading" class="loading">Loading...</div>

    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else class="profile-content">
      <!-- Tabs -->
      <div class="tabs">
        <button
          v-for="tab in [
            'basic',
            'social',
            'services',
            'skills',
            'experience',
            'education',
            'projects',
          ]"
          :key="tab"
          @click="activeTab = tab"
          :class="['tab-button', { active: activeTab === tab }]"
        >
          {{ tab.charAt(0).toUpperCase() + tab.slice(1) }}
        </button>
      </div>

      <!-- Basic Profile Information -->
      <div v-show="activeTab === 'basic'" class="section">
        <h2>Basic Information</h2>
        <form @submit.prevent="saveProfile" class="profile-form">
          <div class="image-upload-row">
            <div class="form-group">
              <label>Hero Photo <small>(shown in hero section)</small></label>
              <div class="image-upload-box" @click="$refs.heroInput.click()">
                <img
                  v-if="heroPreview"
                  :src="heroPreview"
                  class="img-preview"
                  alt="Hero preview"
                />
                <img
                  v-else-if="profileData.profile_image"
                  :src="profileData.profile_image"
                  class="img-preview"
                  alt="Current hero"
                />
                <div v-else class="upload-placeholder">📷 Click to upload</div>
              </div>
              <input
                ref="heroInput"
                type="file"
                accept="image/*"
                style="display: none"
                @change="onHeroChange"
              />
              <button
                v-if="heroPreview"
                type="button"
                class="btn btn-danger btn-small"
                style="margin-top: 0.4rem"
                @click="
                  heroPreview = null;
                  heroFile = null;
                "
              >
                Remove
              </button>
            </div>
            <div class="form-group">
              <label>About Photo <small>(shown in about section)</small></label>
              <div class="image-upload-box" @click="$refs.aboutInput.click()">
                <img
                  v-if="aboutPreview"
                  :src="aboutPreview"
                  class="img-preview"
                  alt="About preview"
                />
                <img
                  v-else-if="profileData.about_image"
                  :src="profileData.about_image"
                  class="img-preview"
                  alt="Current about"
                />
                <div v-else class="upload-placeholder">📷 Click to upload</div>
              </div>
              <input
                ref="aboutInput"
                type="file"
                accept="image/*"
                style="display: none"
                @change="onAboutChange"
              />
              <button
                v-if="aboutPreview"
                type="button"
                class="btn btn-danger btn-small"
                style="margin-top: 0.4rem"
                @click="
                  aboutPreview = null;
                  aboutFile = null;
                "
              >
                Remove
              </button>
            </div>
          </div>
          <div class="form-group">
            <label>Full Name</label>
            <input v-model="profileData.full_name" type="text" />
          </div>
          <div class="form-group">
            <label>Professional Title</label>
            <input
              v-model="profileData.title"
              type="text"
              placeholder="e.g., Virtual Assistant"
              required
            />
          </div>
          <div class="form-group">
            <label
              >Hero Description
              <small>(shown on the landing page hero section)</small></label
            >
            <textarea
              v-model="profileData.hero_description"
              rows="3"
              placeholder="Short tagline or intro shown below your name on the homepage"
            ></textarea>
          </div>
          <div class="form-group">
            <label>Bio <small>(shown on the About section)</small></label>
            <textarea
              v-model="profileData.bio"
              rows="4"
              placeholder="Short professional biography"
            ></textarea>
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
      <div v-show="activeTab === 'social'" class="section">
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
      <div v-show="activeTab === 'services'" class="section">
        <h2>Services Offered</h2>
        <div class="form-group checkbox">
          <label>
            <input v-model="profileData.show_services" type="checkbox" />
            Show services section in portfolio
          </label>
        </div>
        <div class="services-list">
          <div
            v-for="(service, index) in profileData.services_offered"
            :key="index"
            class="service-item service-item-block"
          >
            <div class="service-item-fields">
              <div class="service-field">
                <label>Icon</label>
                <input
                  v-model="service.icon"
                  type="text"
                  placeholder="e.g. 📱"
                  style="width: 70px"
                />
              </div>
              <div class="service-field" style="flex: 1">
                <label>Title</label>
                <input
                  v-model="service.title"
                  type="text"
                  placeholder="Service title"
                />
              </div>
              <div class="service-field">
                <label class="visibility-toggle">
                  <input type="checkbox" v-model="service.is_visible" />
                  <span>Show</span>
                </label>
              </div>
            </div>
            <div class="service-field">
              <label>Description</label>
              <textarea
                v-model="service.description"
                rows="2"
                placeholder="What this service includes..."
              ></textarea>
            </div>
            <button
              @click="removeService(index)"
              class="btn btn-danger btn-small"
            >
              Remove
            </button>
          </div>
          <button @click="addService" class="btn btn-secondary">
            + Add Service
          </button>
        </div>
        <button @click="saveProfile" class="btn btn-primary">
          Save Services
        </button>
      </div>

      <!-- Skills -->
      <div v-show="activeTab === 'skills'" class="section">
        <h2>Skills</h2>
        <div class="form-group checkbox">
          <label>
            <input v-model="profileData.show_skills" type="checkbox" />
            Show skills section in portfolio
          </label>
        </div>
        <div class="skill-categories">
          <div
            v-for="(group, gi) in profileData.skills"
            :key="gi"
            class="skill-category-block"
          >
            <div class="skill-category-header">
              <input
                v-model="group.category"
                type="text"
                placeholder="Category name (e.g. Social Media)"
                class="category-name-input"
              />
              <button
                @click="removeSkillGroup(gi)"
                class="btn btn-danger btn-small"
              >
                Remove Group
              </button>
            </div>
            <div class="skill-tags-editor">
              <div
                v-for="(skill, si) in group.skills"
                :key="si"
                class="skill-tag-item"
              >
                <input v-model="skill.name" type="text" placeholder="Skill" />
                <label class="visibility-toggle">
                  <input type="checkbox" v-model="skill.is_visible" />
                  <span>Show</span>
                </label>
                <button
                  @click="removeSkillItem(gi, si)"
                  class="btn btn-danger btn-small"
                >
                  &times;
                </button>
              </div>
              <button
                @click="addSkillItem(gi)"
                class="btn btn-secondary btn-small"
              >
                + Add Skill
              </button>
            </div>
          </div>
        </div>
        <button
          @click="addSkillGroup"
          class="btn btn-secondary"
          style="margin-top: 0.75rem"
        >
          + Add Category
        </button>
        <button
          @click="saveProfile"
          class="btn btn-primary"
          style="margin-left: 0.5rem"
        >
          Save Skills
        </button>
      </div>

      <!-- Work Experience -->
      <div v-show="activeTab === 'experience'" class="section">
        <h2>Work Experience</h2>
        <div class="form-group checkbox">
          <label>
            <input v-model="profileData.show_experience" type="checkbox" />
            Show work experience section in portfolio
          </label>
        </div>
        <ExperienceList />
      </div>

      <!-- Education -->
      <div v-show="activeTab === 'education'" class="section">
        <h2>Education</h2>
        <div class="form-group checkbox">
          <label>
            <input v-model="profileData.show_education" type="checkbox" />
            Show education section in portfolio
          </label>
        </div>
        <EducationList />
      </div>

      <!-- Portfolio Projects -->
      <div v-show="activeTab === 'projects'" class="section">
        <h2>Portfolio Projects</h2>
        <div class="form-group checkbox">
          <label>
            <input v-model="profileData.show_projects" type="checkbox" />
            Show portfolio projects section in portfolio
          </label>
        </div>
        <ProjectList />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, reactive } from "vue";
import { useProfileStore } from "../stores/profile";
import ExperienceList from "../components/ExperienceList.vue";
import EducationList from "../components/EducationList.vue";
import ProjectList from "../components/ProjectList.vue";

export default {
  name: "ProfileCMS",
  components: {
    ExperienceList,
    EducationList,
    ProjectList,
  },
  setup() {
    const profileStore = useProfileStore();

    const stripMediaHost = (url) =>
      url ? url.replace(/^https?:\/\/[^/]+/, "") : null;

    const heroFile = ref(null);
    const heroPreview = ref(null);
    const aboutFile = ref(null);
    const aboutPreview = ref(null);

    const onHeroChange = (e) => {
      const file = e.target.files[0];
      if (!file) return;
      heroFile.value = file;
      heroPreview.value = URL.createObjectURL(file);
    };

    const onAboutChange = (e) => {
      const file = e.target.files[0];
      if (!file) return;
      aboutFile.value = file;
      aboutPreview.value = URL.createObjectURL(file);
    };

    const profileData = ref({
      profile_image: null,
      about_image: null,
      full_name: "",
      title: "",
      hero_description: "",
      bio: "",
      email: "",
      phone: "",
      location: "",
      website_url: "",
      linkedin_url: "",
      facebook_url: "",
      instagram_url: "",
      twitter_url: "",
      github_url: "",
      services_offered: [],
      skills: [],
      is_available: true,
      show_services: true,
      show_skills: true,
      show_experience: true,
      show_education: true,
      show_projects: true,
    });

    const activeTab = ref("basic");

    const loading = ref(false);
    const error = ref(null);

    const loadProfile = async () => {
      loading.value = true;
      error.value = null;
      try {
        console.log("Fetching profile...");
        const data = await profileStore.fetchMyProfile();
        console.log("Profile data received:", data);
        if (data) {
          profileData.value = {
            profile_image:
              data.profile_image_url ||
              stripMediaHost(data.profile_image) ||
              null,
            about_image:
              data.about_image_url || stripMediaHost(data.about_image) || null,
            full_name: data.full_name || "",
            title: data.title || "",
            hero_description: data.hero_description || "",
            bio: data.bio || "",
            email: data.email || "",
            phone: data.phone || "",
            location: data.location || "",
            website_url: data.website_url || "",
            linkedin_url: data.linkedin_url || "",
            facebook_url: data.facebook_url || "",
            instagram_url: data.instagram_url || "",
            twitter_url: data.twitter_url || "",
            github_url: data.github_url || "",
            services_offered: data.services_offered || [],
            skills: data.skills || [],
            is_available:
              data.is_available !== undefined ? data.is_available : true,
            show_services:
              data.show_services !== undefined ? data.show_services : true,
            show_skills:
              data.show_skills !== undefined ? data.show_skills : true,
            show_experience:
              data.show_experience !== undefined ? data.show_experience : true,
            show_education:
              data.show_education !== undefined ? data.show_education : true,
            show_projects:
              data.show_projects !== undefined ? data.show_projects : true,
          };
          console.log("Profile data set:", profileData.value);
        }
      } catch (err) {
        console.error("Load profile error:", err);
        if (err.response?.status === 404) {
          // Profile doesn't exist yet, that's okay
          error.value = null;
        } else {
          error.value = err.message || "Failed to load profile";
        }
      } finally {
        loading.value = false;
      }
    };

    const saveProfile = async () => {
      loading.value = true;
      error.value = null;
      try {
        console.log(
          "[Save] heroFile:",
          heroFile.value,
          "aboutFile:",
          aboutFile.value,
        );
        const hasImage = heroFile.value || aboutFile.value;
        const imageKeys = ["profile_image", "about_image"];
        if (hasImage) {
          const fd = new FormData();
          Object.entries(profileData.value).forEach(([k, v]) => {
            if (imageKeys.includes(k)) return;
            if (v === null || v === undefined) return;
            fd.append(k, typeof v === "object" ? JSON.stringify(v) : v);
          });
          if (heroFile.value) fd.append("profile_image", heroFile.value);
          if (aboutFile.value) fd.append("about_image", aboutFile.value);
          await profileStore.updateProfileForm(fd);
        } else {
          const payload = Object.fromEntries(
            Object.entries(profileData.value).filter(
              ([k]) => !imageKeys.includes(k),
            ),
          );
          if (profileStore.profile?.id) {
            await profileStore.updateProfile(payload);
          } else {
            await profileStore.createProfile(payload);
          }
        }
        heroFile.value = null;
        heroPreview.value = null;
        aboutFile.value = null;
        aboutPreview.value = null;
        alert("Profile saved successfully!");
      } catch (err) {
        const detail = err.response?.data;
        const msg =
          typeof detail === "object"
            ? Object.entries(detail)
                .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(", ") : v}`)
                .join("\n")
            : err.message || "Failed to save profile";
        error.value = msg;
        alert("Failed to save profile:\n" + msg);
      } finally {
        loading.value = false;
      }
    };

    const addService = () => {
      profileData.value.services_offered.push({
        icon: "",
        title: "",
        description: "",
        is_visible: true,
      });
    };

    const removeService = (index) => {
      profileData.value.services_offered.splice(index, 1);
    };

    const addSkillGroup = () => {
      profileData.value.skills.push({ category: "", skills: [] });
    };

    const removeSkillGroup = (gi) => {
      profileData.value.skills.splice(gi, 1);
    };

    const addSkillItem = (gi) => {
      profileData.value.skills[gi].skills.push({ name: "", is_visible: true });
    };

    const removeSkillItem = (gi, si) => {
      profileData.value.skills[gi].skills.splice(si, 1);
    };

    onMounted(() => {
      loadProfile();
    });

    return {
      profileData,
      heroFile,
      heroPreview,
      onHeroChange,
      aboutFile,
      aboutPreview,
      onAboutChange,
      loading,
      error,
      saveProfile,
      addService,
      removeService,
      addSkillGroup,
      removeSkillGroup,
      addSkillItem,
      removeSkillItem,
      activeTab,
    };
  },
};
</script>

<style scoped>
.profile-cms {
  max-width: 900px;
  margin: 0 auto;
}

.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 0.5rem;
  overflow-x: auto;
}

.tab-button {
  padding: 0.75rem 1.25rem;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  color: #7f8c8d;
  border-radius: 4px 4px 0 0;
  transition: all 0.2s;
  white-space: nowrap;
}

.tab-button:hover {
  background: #f5f5f5;
  color: #3498db;
}

.tab-button.active {
  background: #3498db;
  color: white;
  font-weight: 600;
}

.image-upload-row {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 0.5rem;
}

.image-upload-row .form-group {
  flex: 1;
}

.image-upload-box {
  width: 100%;
  height: 180px;
  border: 2px dashed #ccc;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  overflow: hidden;
  background: #fafafa;
  transition: border-color 0.2s;
}

.image-upload-box:hover {
  border-color: #3498db;
}

.img-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-placeholder {
  color: #aaa;
  font-size: 0.9rem;
  text-align: center;
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
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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

.skill-categories {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.skill-category-block {
  background: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.skill-category-header {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.category-name-input {
  flex: 1;
  padding: 0.5rem 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.95rem;
  font-weight: 600;
}

.skill-tags-editor {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.skill-tag-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: white;
  border: 1px solid #ddd;
  border-radius: 20px;
  padding: 0.2rem 0.2rem 0.2rem 0.5rem;
}

.skill-tag-item input {
  border: none;
  outline: none;
  font-size: 0.85rem;
  width: 110px;
  background: transparent;
  padding: 0.1rem 0.25rem;
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
