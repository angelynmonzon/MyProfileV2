<template>
  <section id="certificates" class="certificate-section reveal">
    <div class="container">
      <h2 class="section-title">Certificates</h2>
      <div class="certificates-grid">
        <div
          v-for="certificate in visibleCertificates"
          :key="certificate.id"
          class="certificate-card"
        >
          <div class="certificate-image">
            <img 
              :src="certificate.image_url || certificate.image" 
              :alt="certificate.title || 'Certificate'"
              @click="openLightbox(certificate.image_url || certificate.image)"
            />
          </div>
          <div class="certificate-content">
            <h3 v-if="certificate.title" class="certificate-title">{{ certificate.title }}</h3>
            <p v-if="certificate.issuer" class="certificate-issuer">{{ certificate.issuer }}</p>
            <p v-if="certificate.date" class="certificate-date">{{ formatDate(certificate.date) }}</p>
          </div>
        </div>
      </div>
      <div v-if="visibleCertificates.length === 0" class="no-certificates">
        <p>No certificates yet.</p>
      </div>
    </div>

    <div v-if="showLightbox" class="lightbox-overlay" @click="closeLightbox">
      <div class="lightbox-content" @click.stop>
        <button @click="closeLightbox" class="lightbox-close">&times;</button>
        <img :src="lightboxImage" class="lightbox-image" />
      </div>
    </div>
  </section>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'CertificateSection',
  props: ['profile'],
  setup() {
    const showLightbox = ref(false)
    const lightboxImage = ref(null)

    const openLightbox = (imageUrl) => {
      lightboxImage.value = imageUrl
      showLightbox.value = true
    }

    const closeLightbox = () => {
      showLightbox.value = false
      lightboxImage.value = null
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long'
      })
    }

    return {
      showLightbox,
      lightboxImage,
      openLightbox,
      closeLightbox,
      formatDate
    }
  },
  computed: {
    visibleCertificates() {
      if (!this.profile?.certificates) return []
      return this.profile.certificates.filter(c => c.is_visible)
    }
  }
}
</script>

<style scoped>
.certificate-section {
  padding: 6rem 2rem;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  font-family: 'Montserrat', sans-serif;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-white);
  text-align: center;
  margin-bottom: 3rem;
  letter-spacing: 2px;
}

.certificates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.certificate-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(226, 185, 111, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.certificate-card:hover {
  transform: translateY(-5px);
  border-color: var(--color-gold);
  box-shadow: 0 10px 30px rgba(226, 185, 111, 0.2);
}

.certificate-image {
  width: 100%;
  height: 250px;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.certificate-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.certificate-card:hover .certificate-image img {
  transform: scale(1.05);
}

.certificate-content {
  text-align: center;
}

.certificate-title {
  font-family: 'Montserrat', sans-serif;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-white);
  margin-bottom: 0.5rem;
}

.certificate-issuer {
  font-size: 0.95rem;
  color: var(--color-gold);
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.certificate-date {
  font-size: 0.85rem;
  color: var(--color-white-60);
}

.no-certificates {
  text-align: center;
  color: var(--color-white-60);
  font-size: 1.1rem;
  padding: 2rem;
}

@media (max-width: 768px) {
  .certificate-section {
    padding: 4rem 1rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .certificates-grid {
    grid-template-columns: 1fr;
  }
}

.certificate-image img {
  cursor: pointer;
}

.lightbox-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.95);
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
  top: -50px;
  right: 0;
  background: none;
  border: none;
  color: var(--color-gold);
  font-size: 3rem;
  cursor: pointer;
  padding: 0.5rem;
  line-height: 1;
}

.lightbox-image {
  max-width: 100%;
  max-height: 90vh;
  object-fit: contain;
  border-radius: 8px;
}
</style>
