<template>
  <div class="certificate-list">
    <div v-if="loading" class="loading">Loading certificates...</div>

    <div v-else>
      <div class="list-header">
        <h2>Certificates</h2>
        <button @click="showForm = true" class="btn btn-primary">
          Add Certificate
        </button>
      </div>
      <div
        v-for="certificate in certificates"
        :key="certificate.id"
        class="certificate-item"
      >
        <div class="certificate-header">
          <div class="certificate-info">
            <img v-if="certificate.image_url" :src="certificate.image_url" class="certificate-thumb" />
            <div class="certificate-details">
              <h3>{{ certificate.title || 'Untitled' }}</h3>
              <p>{{ certificate.issuer || '' }}</p>
              <p v-if="certificate.date">{{ formatDate(certificate.date) }}</p>
            </div>
          </div>
          <div class="certificate-actions">
            <label class="visibility-toggle">
              <input
                type="checkbox"
                :checked="certificate.is_visible"
                @change="toggleVisibility(certificate)"
              />
              <span>Show</span>
            </label>
            <button @click="editCertificate(certificate)" class="btn btn-small btn-secondary">
              Edit
            </button>
            <button @click="confirmDelete(certificate)" class="btn btn-small btn-danger">
              Delete
            </button>
          </div>
        </div>
      </div>

      <div v-if="showForm || editingCertificate" class="modal-overlay" @click="closeForm">
        <div class="modal-content" @click.stop>
          <h3>{{ editingCertificate ? 'Edit Certificate' : 'Add Certificate' }}</h3>
          <form @submit.prevent="saveCertificate">
            <div class="form-group">
              <label>Image</label>
              <input type="file" @change="onFileChange" accept="image/*" />
              <div v-if="imagePreview" class="image-preview">
                <img :src="imagePreview" />
              </div>
            </div>
            <div class="form-group">
              <label>Title</label>
              <input v-model="formData.title" type="text" placeholder="Certificate title" />
            </div>
            <div class="form-group">
              <label>Issuer</label>
              <input v-model="formData.issuer" type="text" placeholder="Issuing organization" />
            </div>
            <div class="form-group">
              <label>Date</label>
              <input v-model="formData.date" type="date" />
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
          <p>Are you sure you want to delete this certificate?</p>
          <div class="form-actions">
            <button @click="closeDeleteModal" class="btn btn-secondary">Cancel</button>
            <button @click="handleDelete" class="btn btn-danger">Delete</button>
          </div>
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

export default {
  name: "CertificateList",
  setup() {
    const profileStore = useProfileStore();
    const authStore = useAuthStore();

    const certificates = ref([]);
    const loading = ref(false);
    const showForm = ref(false);
    const editingCertificate = ref(null);

    const imageFile = ref(null);
    const imagePreview = ref(null);

    const showLightbox = ref(false);
    const lightboxImage = ref(null);

    const formData = ref({
      image: null,
      title: "",
      issuer: "",
      date: "",
      is_visible: true,
    });

    const api = axios.create({
      baseURL: '/api'
    });

    api.interceptors.request.use((config) => {
      if (authStore.token) {
        config.headers.Authorization = `Token ${authStore.token}`;
      }
      return config;
    });

    const loadCertificates = async () => {
      loading.value = true;
      try {
        const response = await api.get("/certificates/");
        certificates.value = response.data;
      } catch (err) {
        console.error("Failed to load certificates:", err);
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

    const saveCertificate = async () => {
      loading.value = true;
      try {
        const fd = new FormData();
        if (imageFile.value) {
          fd.append("image", imageFile.value);
        }
        if (formData.value.title) {
          fd.append("title", formData.value.title);
        }
        if (formData.value.issuer) {
          fd.append("issuer", formData.value.issuer);
        }
        if (formData.value.date) {
          fd.append("date", formData.value.date);
        }
        fd.append("is_visible", formData.value.is_visible ? "true" : "false");

        if (editingCertificate.value) {
          await api.patch(`/certificates/${editingCertificate.value.id}/`, fd);
        } else {
          await api.post("/certificates/", fd);
        }

        closeForm();
        await loadCertificates();
        await profileStore.fetchMyProfile();
      } catch (err) {
        alert(
          "Failed to save certificate: " +
            (err.response?.data?.detail || err.message)
        );
      } finally {
        loading.value = false;
      }
    };

    const editCertificate = (certificate) => {
      editingCertificate.value = certificate;
      formData.value = {
        image: null,
        title: certificate.title,
        issuer: certificate.issuer,
        date: certificate.date,
        is_visible: certificate.is_visible,
      };
      if (certificate.image_url) {
        imagePreview.value = certificate.image_url;
      }
      showForm.value = true;
    };

    const confirmDelete = (certificate) => {
      certificateToDelete.value = certificate;
      showDeleteModal.value = true;
    };

    const handleDelete = async () => {
      try {
        await api.delete(`/certificates/${certificateToDelete.value.id}/`);
        certificates.value = certificates.value.filter(
          (c) => c.id !== certificateToDelete.value.id
        );
        closeDeleteModal();
        await profileStore.fetchMyProfile();
      } catch (err) {
        alert(
          "Failed to delete certificate: " +
            (err.response?.data?.detail || err.message)
        );
      }
    };

    const toggleVisibility = async (certificate) => {
      try {
        await api.patch(`/certificates/${certificate.id}/`, {
          is_visible: !certificate.is_visible,
        });
        certificate.is_visible = !certificate.is_visible;
      } catch (err) {
        alert(
          "Failed to update visibility: " +
            (err.response?.data?.detail || err.message)
        );
        certificate.is_visible = !certificate.is_visible;
      }
    };

    const closeForm = () => {
      showForm.value = false;
      editingCertificate.value = null;
      formData.value = {
        image: null,
        title: "",
        issuer: "",
        date: "",
        is_visible: true,
      };
      imageFile.value = null;
      imagePreview.value = null;
    };

    const showDeleteModal = ref(false);
    const certificateToDelete = ref(null);

    const closeDeleteModal = () => {
      showDeleteModal.value = false;
      certificateToDelete.value = null;
    };

    const openLightbox = (imageUrl) => {
      lightboxImage.value = imageUrl;
      showLightbox.value = true;
    };

    const closeLightbox = () => {
      showLightbox.value = false;
      lightboxImage.value = null;
    };

    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long'
      })
    };

    onMounted(() => {
      loadCertificates();
    });

    return {
      certificates,
      loading,
      showForm,
      editingCertificate,
      formData,
      imagePreview,
      showDeleteModal,
      showLightbox,
      lightboxImage,
      saveCertificate,
      editCertificate,
      confirmDelete,
      handleDelete,
      closeForm,
      closeDeleteModal,
      toggleVisibility,
      onFileChange,
      openLightbox,
      closeLightbox,
      formatDate
    };
  },
};
</script>

<style scoped>
.certificate-list {
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

.certificate-item {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.certificate-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.certificate-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.certificate-thumb {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.2s;
}

.certificate-thumb:hover {
  transform: scale(1.05);
}

.certificate-details h3 {
  margin: 0;
  font-size: 1rem;
  color: #333;
}

.certificate-details p {
  margin: 0.25rem 0 0;
  font-size: 0.85rem;
  color: #666;
}

.certificate-actions {
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
.form-group input[type="date"],
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
