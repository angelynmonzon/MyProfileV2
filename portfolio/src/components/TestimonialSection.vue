<template>
  <section id="testimonials" class="testimonial-section reveal">
    <div class="container">
      <h2 class="section-title">What People Say</h2>
      <div class="testimonials-grid">
        <div
          v-for="testimonial in visibleTestimonials"
          :key="testimonial.id"
          class="testimonial-card"
        >
          <div class="testimonial-image">
            <img 
              :src="testimonial.image_url || testimonial.image" 
              :alt="testimonial.name || 'Testimonial'"
              @click="openLightbox(testimonial.image_url || testimonial.image)"
            />
          </div>
          <div class="testimonial-content">
            <h3 v-if="testimonial.name" class="testimonial-name">{{ testimonial.name }}</h3>
            <p v-if="testimonial.role" class="testimonial-role">{{ testimonial.role }}</p>
          </div>
        </div>
      </div>
      <div v-if="visibleTestimonials.length === 0" class="no-testimonials">
        <p>No testimonials yet.</p>
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
  name: 'TestimonialSection',
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

    return {
      showLightbox,
      lightboxImage,
      openLightbox,
      closeLightbox
    }
  },
  computed: {
    visibleTestimonials() {
      if (!this.profile?.testimonials) return []
      return this.profile.testimonials.filter(t => t.is_visible)
    }
  }
}
</script>

<style scoped>
.testimonial-section {
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

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.testimonial-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(226, 185, 111, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.testimonial-card:hover {
  transform: translateY(-5px);
  border-color: var(--color-gold);
  box-shadow: 0 10px 30px rgba(226, 185, 111, 0.2);
}

.testimonial-image {
  width: 100%;
  height: 250px;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.testimonial-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.testimonial-card:hover .testimonial-image img {
  transform: scale(1.05);
}

.testimonial-content {
  text-align: center;
}

.testimonial-name {
  font-family: 'Montserrat', sans-serif;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-white);
  margin-bottom: 0.5rem;
}

.testimonial-role {
  font-size: 0.95rem;
  color: var(--color-gold);
  font-weight: 500;
}

.no-testimonials {
  text-align: center;
  color: var(--color-white-60);
  font-size: 1.1rem;
  padding: 2rem;
}

@media (max-width: 768px) {
  .testimonial-section {
    padding: 4rem 1rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .testimonials-grid {
    grid-template-columns: 1fr;
  }
}

.testimonial-image img {
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
