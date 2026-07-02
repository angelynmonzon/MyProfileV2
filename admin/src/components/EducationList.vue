<template>
  <div class="education-list">
    <div v-if="loading" class="loading">Loading education...</div>

    <div v-else>
      <div v-for="edu in education" :key="edu.id" class="education-item">
        <div class="education-header">
          <h3>{{ edu.degree }} from {{ edu.institution }}</h3>
          <div class="education-actions">
            <label class="visibility-toggle">
              <input
                type="checkbox"
                v-model="edu.is_visible"
                @change="toggleVisibility(edu)"
              />
              <span>Show</span>
            </label>
            <button
              @click="editEducation(edu)"
              class="btn btn-small btn-secondary"
            >
              Edit
            </button>
            <button
              @click="deleteEducation(edu.id)"
              class="btn btn-small btn-danger"
            >
              Delete
            </button>
          </div>
        </div>
        <div class="education-details">
          <p>
            <strong>Location:</strong> {{ edu.location || "Not specified" }}
          </p>
          <p>
            <strong>Period:</strong> {{ formatDate(edu.start_date) }} -
            {{ edu.is_current ? "Present" : formatDate(edu.end_date) }}
          </p>
          <p v-if="edu.description">
            <strong>Description:</strong> {{ edu.description }}
          </p>
        </div>
      </div>

      <button @click="showForm = true" class="btn btn-primary">
        Add Education
      </button>
    </div>

    <!-- Education Form Modal -->
    <div v-if="showForm" class="modal">
      <div class="modal-content">
        <h2>{{ editingEducation ? "Edit Education" : "Add Education" }}</h2>
        <form @submit.prevent="saveEducation" class="education-form">
          <div class="form-group">
            <label>Degree</label>
            <input
              v-model="formData.degree"
              type="text"
              required
              placeholder="e.g., Bachelor of Science in Computer Science"
            />
          </div>
          <div class="form-group">
            <label>Institution</label>
            <input
              v-model="formData.institution"
              type="text"
              required
              placeholder="e.g., University of Example"
            />
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
            <input
              v-model="formData.end_date"
              type="date"
              :disabled="formData.is_current"
            />
          </div>
          <div class="form-group checkbox">
            <label>
              <input v-model="formData.is_current" type="checkbox" />
              Currently studying here
            </label>
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea
              v-model="formData.description"
              rows="4"
              placeholder="Field of study, achievements, etc."
            ></textarea>
          </div>
          <div class="form-group checkbox">
            <label>
              <input v-model="formData.is_visible" type="checkbox" />
              Show in portfolio
            </label>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary">Save</button>
            <button type="button" @click="closeForm" class="btn btn-secondary">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useProfileStore } from "../stores/profile";

export default {
  name: "EducationList",
  setup() {
    const profileStore = useProfileStore();

    const education = ref([]);
    const loading = ref(false);
    const showForm = ref(false);
    const editingEducation = ref(null);

    const formData = ref({
      degree: "",
      institution: "",
      location: "",
      start_date: "",
      end_date: "",
      is_current: false,
      description: "",
      is_visible: true,
    });

    const loadEducation = async () => {
      loading.value = true;
      try {
        await profileStore.fetchEducation();
        education.value = profileStore.education;
      } catch (err) {
        console.error("Failed to load education:", err);
      } finally {
        loading.value = false;
      }
    };

    const saveEducation = async () => {
      try {
        if (editingEducation.value) {
          await profileStore.updateEducation(
            editingEducation.value.id,
            formData.value,
          );
        } else {
          await profileStore.createEducation(formData.value);
        }
        closeForm();
        loadEducation();
      } catch (err) {
        alert(
          "Failed to save education: " +
            (err.response?.data?.detail || err.message),
        );
      }
    };

    const editEducation = (edu) => {
      editingEducation.value = edu;
      formData.value = {
        degree: edu.degree,
        institution: edu.institution,
        location: edu.location,
        start_date: edu.start_date,
        end_date: edu.end_date,
        is_current: edu.is_current,
        description: edu.description,
        is_visible: edu.is_visible !== undefined ? edu.is_visible : true,
      };
      showForm.value = true;
    };

    const deleteEducation = async (id) => {
      if (confirm("Are you sure you want to delete this education entry?")) {
        try {
          await profileStore.deleteEducation(id);
          loadEducation();
        } catch (err) {
          alert(
            "Failed to delete education: " +
              (err.response?.data?.detail || err.message),
          );
        }
      }
    };

    const closeForm = () => {
      showForm.value = false;
      editingEducation.value = null;
      formData.value = {
        degree: "",
        institution: "",
        location: "",
        start_date: "",
        end_date: "",
        is_current: false,
        description: "",
        is_visible: true,
      };
    };

    const toggleVisibility = async (edu) => {
      try {
        await profileStore.updateEducation(edu.id, {
          is_visible: edu.is_visible,
        });
      } catch (err) {
        alert(
          "Failed to update visibility: " +
            (err.response?.data?.detail || err.message),
        );
        edu.is_visible = !edu.is_visible;
      }
    };

    const formatDate = (dateString) => {
      if (!dateString) return "Not specified";
      const date = new Date(dateString);
      return date.toLocaleDateString("en-US", {
        month: "long",
        year: "numeric",
      });
    };

    onMounted(() => {
      loadEducation();
    });

    return {
      education,
      loading,
      showForm,
      editingEducation,
      formData,
      saveEducation,
      editEducation,
      deleteEducation,
      closeForm,
      formatDate,
      toggleVisibility,
    };
  },
};
</script>

<style scoped>
.education-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.education-item {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #27ae60;
}

.education-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.education-header h3 {
  margin: 0;
  color: #2c3e50;
}

.education-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.visibility-toggle {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.85rem;
  color: #555;
  cursor: pointer;
}

.visibility-toggle input {
  width: auto;
}

.education-details p {
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
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
}

.education-form {
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
