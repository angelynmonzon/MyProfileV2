<template>
  <div class="testimonial-list">
    <div v-if="loading" class="loading">Loading testimonials...</div>

    <div v-else>
      <div class="list-header">
        <h2>Testimonials</h2>
        <button @click="showForm = true" class="btn btn-primary">
          Add Testimonial
        </button>
      </div>
      <div
        v-for="testimonial in testimonials"
        :key="testimonial.id"
        class="testimonial-item"
      >
        <div class="testimonial-header">
          <div class="testimonial-info">
            <img 
              v-if="testimonial.image_url" 
              :src="testimonial.image_url" 
              class="testimonial-thumb" 
              @click="openLightbox(testimonial.image_url)"
            />
            <div class="testimonial-details">
              <h3>{{ testimonial.name || 'Anonymous' }}</h3>
              <p>{{ testimonial.role || '' }}</p>
            </div>
          </div>
          <div class="testimonial-actions">
            <label class="visibility-toggle">
              <input
                type="checkbox"
                :checked="testimonial.is_visible"
                @change="toggleVisibility(testimonial)"
              />
              <span>Show</span>
            </label>
            <button @click="editTestimonial(testimonial)" class="btn btn-small btn-secondary">
              Edit
            </button>
            <button @click="confirmDelete(testimonial)" class="btn btn-small btn-danger">
              Delete
            </button>
          </div>
        </div>
      </div>

      <div v-if="showForm || editingTestimonial" class="modal-overlay" @click="closeForm">
        <div class="modal-content" @click.stop>
          <h3>{{ editingTestimonial ? 'Edit Testimonial' : 'Add Testimonial' }}</h3>
          <form @submit.prevent="saveTestimonial">
            <div class="form-group">
              <label>Image</label>
              <input type="file" @change="onFileChange" accept="image/*" />
              <div v-if="imagePreview" class="image-preview">
                <img :src="imagePreview" />
              </div>
            </div>
            <div class="form-group">
              <label>Name</label>
              <input v-model="formData.name" type="text" placeholder="Name of the person" />
            </div>
            <div class="form-group">
              <label>Role/Title</label>
              <input v-model="formData.role" type="text" placeholder="Role or title" />
            </div>
            <div class="form-group checkbox">
              <label>
                <input v-model="formData.is_visible" type="checkbox" />
                Show in portfolio
              </label>
            </div>
            <div class="form-actions">
              <button type="button" @click="closeForm" class="btn btn-secondary">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                {{ loading ? 'Saving...' : 'Save' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
        <div class="modal-content modal-small" @click.stop>
          <h3>Confirm Delete</h3>
          <p>Are you sure you want to delete this testimonial?</p>
          <div class="form-actions">
            <button @click="closeDeleteModal" class="btn btn-secondary">Cancel</button>
            <button @click="handleDelete" class="btn btn-danger">Delete</button>
          </div>
        </div>
      </div>

      <div v-if="showLightbox" class="lightbox-overlay" @click="closeLightbox">
        <div class="lightbox-content" @click.stop>
          <button @click="closeLightbox" class="lightbox-close">&times;</button>
          <img :src="lightboxImage" class="lightbox-image" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useProfileStore } from "../../stores/profile";
import { useAuthStore } from "../../stores/auth";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

export default {
  name: "TestimonialList",
  setup() {
    const profileStore = useProfileStore();
    const authStore = useAuthStore();

    const testimonials = ref([]);
    const loading = ref(false);
    const showForm = ref(false);
    const editingTestimonial = ref(null);

    const imageFile = ref(null);
    const imagePreview = ref(null);

    const showLightbox = ref(false);
    const lightboxImage = ref(null);

    const formData = ref({
      image: null,
      name: "",
      role: "",
      is_visible: true,
    });

    const api = axios.create({
      baseURL: API_BASE_URL
    });

    api.interceptors.request.use((config) => {
      if (authStore.token) {
        config.headers.Authorization = `Token ${authStore.token}`;
      }
      return config;
    });

    const loadTestimonials = async () => {
      loading.value = true;
      try {
        const response = await api.get("/testimonials/");
        testimonials.value = response.data;
      } catch (err) {
        console.error("Failed to load testimonials:", err);
      } finally {
        loading.value = false;
      }
    };

    const onFileChange = (e) => {
      const file = e.target.files[0];
      if (file) {
        imageFile.value = file;
        imagePreview.value = URL.createObjectURL(file);
      }
    };

    const saveTestimonial = async () => {
      loading.value = true;
      try {
        const fd = new FormData();
        if (imageFile.value) {
          fd.append("image", imageFile.value);
        }
        if (formData.value.name) {
          fd.append("name", formData.value.name);
        }
        if (formData.value.role) {
          fd.append("role", formData.value.role);
        }
        fd.append("is_visible", formData.value.is_visible ? "true" : "false");

        if (editingTestimonial.value) {
          await api.patch(`/testimonials/${editingTestimonial.value.id}/`, fd);
        } else {
          await api.post("/testimonials/", fd);
        }

        closeForm();
        await loadTestimonials();
        await profileStore.fetchMyProfile();
      } catch (err) {
        alert(
          "Failed to save testimonial: " +
            (err.response?.data?.detail || err.message)
        );
      } finally {
        loading.value = false;
      }
    };

    const editTestimonial = (testimonial) => {
      editingTestimonial.value = testimonial;
      formData.value = {
        image: null,
        name: testimonial.name,
        role: testimonial.role,
        is_visible: testimonial.is_visible,
      };
      if (testimonial.image_url) {
        imagePreview.value = testimonial.image_url;
      }
      showForm.value = true;
    };

    const confirmDelete = (testimonial) => {
      testimonialToDelete.value = testimonial;
      showDeleteModal.value = true;
    };

    const handleDelete = async () => {
      try {
        await api.delete(`/testimonials/${testimonialToDelete.value.id}/`);
        testimonials.value = testimonials.value.filter(
          (t) => t.id !== testimonialToDelete.value.id
        );
        closeDeleteModal();
        await profileStore.fetchMyProfile();
      } catch (err) {
        alert(
          "Failed to delete testimonial: " +
            (err.response?.data?.detail || err.message)
        );
      }
    };

    const toggleVisibility = async (testimonial) => {
      try {
        await api.patch(`/testimonials/${testimonial.id}/`, {
          is_visible: !testimonial.is_visible,
        });
        testimonial.is_visible = !testimonial.is_visible;
      } catch (err) {
        alert(
          "Failed to update visibility: " +
            (err.response?.data?.detail || err.message)
        );
        testimonial.is_visible = !testimonial.is_visible;
      }
    };

    const closeForm = () => {
      showForm.value = false;
      editingTestimonial.value = null;
      formData.value = {
        image: null,
        name: "",
        role: "",
        is_visible: true,
      };
      imageFile.value = null;
      imagePreview.value = null;
    };

    const showDeleteModal = ref(false);
    const testimonialToDelete = ref(null);

    const closeDeleteModal = () => {
      showDeleteModal.value = false;
      testimonialToDelete.value = null;
    };

    const openLightbox = (imageUrl) => {
      lightboxImage.value = imageUrl;
      showLightbox.value = true;
    };

    const closeLightbox = () => {
      showLightbox.value = false;
      lightboxImage.value = null;
    };

    onMounted(() => {
      loadTestimonials();
    });

    return {
      testimonials,
      loading,
      showForm,
      editingTestimonial,
      formData,
      imagePreview,
      showDeleteModal,
      showLightbox,
      lightboxImage,
      saveTestimonial,
      editTestimonial,
      confirmDelete,
      handleDelete,
      closeForm,
      closeDeleteModal,
      toggleVisibility,
      onFileChange,
      openLightbox,
      closeLightbox,
    };
  },
};
</script>

<style scoped>
.testimonial-list {
  padding: 1rem 0;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.list-header h2 {
  font-size: 1.5rem;
  color: #333;
}

.testimonial-item {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.testimonial-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.testimonial-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.testimonial-thumb {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 50%;
}

.testimonial-details h3 {
  margin: 0;
  font-size: 1rem;
  color: #333;
}

.testimonial-details p {
  margin: 0.25rem 0 0;
  font-size: 0.85rem;
  color: #666;
}

.testimonial-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.visibility-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #666;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-small {
  max-width: 400px;
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input[type="text"],
.form-group input[type="file"] {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-group.checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-group.checkbox label {
  margin-bottom: 0;
}

.image-preview {
  margin-top: 0.5rem;
}

.image-preview img {
  max-width: 100%;
  max-height: 200px;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-primary {
  background: #e2b96f;
  color: #0d0d0d;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-small {
  padding: 0.25rem 0.5rem;
  font-size: 0.8rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.testimonial-thumb {
  cursor: pointer;
  transition: transform 0.2s;
}

.testimonial-thumb:hover {
  transform: scale(1.05);
}

.lightbox-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.lightbox-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
}

.lightbox-close {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: white;
  font-size: 2rem;
  cursor: pointer;
  padding: 0.5rem;
}

.lightbox-image {
  max-width: 100%;
  max-height: 90vh;
  object-fit: contain;
  border-radius: 4px;
}
</style>
