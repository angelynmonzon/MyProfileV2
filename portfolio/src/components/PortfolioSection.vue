<template>
  <section id="portfolio" class="section portfolio-section">
    <div class="container">
      <div class="section-title reveal">
        <span class="script">My Work</span>
        <h2>Portfolio</h2>
        <div class="divider"></div>
      </div>
      <div class="search-container">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search projects by title or description..."
          class="search-input"
        />
        <button
          v-if="searchQuery"
          @click="clearSearch"
          class="clear-search-btn"
          aria-label="Clear search"
        >
          &times;
        </button>
      </div>
      <div class="portfolio-grid">
        <div
          v-for="(project, i) in projects"
          :key="i"
          @click="openModal(project)"
          class="portfolio-card reveal"
          :class="'reveal-delay-' + Math.min((i % 3) + 1, 3)"
        >
          <div class="portfolio-thumb">
            <div v-if="hasMedia(project)" class="media-grid">
              <div
                v-for="(media, idx) in getAllMedia(project)"
                :key="idx"
                class="media-item"
              >
                <img
                  v-if="media.type === 'image'"
                  :src="media.url"
                  :alt="project.title"
                />
                <div v-else-if="media.type === 'video'" class="video-thumbnail">
                  <iframe
                    v-if="isYouTube(media.url)"
                    :src="getYouTubeEmbedUrl(media.url)"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen
                  ></iframe>
                  <iframe
                    v-else-if="isVimeo(media.url)"
                    :src="getVimeoEmbedUrl(media.url)"
                    frameborder="0"
                    allow="autoplay; fullscreen; picture-in-picture"
                    allowfullscreen
                  ></iframe>
                  <a
                    v-else
                    :href="media.url"
                    target="_blank"
                    class="video-link"
                    @click.stop
                  >
                    <span>▶ Video</span>
                  </a>
                </div>
              </div>
            </div>
            <img
              v-else-if="project.image_url || project.image"
              :src="project.image_url || project.image"
              :alt="project.title"
            />
            <div v-else class="thumb-placeholder">
              <span>{{ project.title.charAt(0) }}</span>
            </div>
            <div class="portfolio-overlay">
              <span class="view-label">View Project →</span>
            </div>
          </div>
          <div class="portfolio-info">
            <h3>{{ project.title }}</h3>
            <p>{{ project.description }}</p>
            <div v-if="project.technologies?.length" class="tech-tags">
              <span
                v-for="(tech, j) in project.technologies"
                :key="j"
                class="tech-tag"
                >{{ tech }}</span
              >
            </div>
          </div>
        </div>

        <div v-if="!projects.length" class="empty-state">
          No portfolio projects yet.
        </div>
      </div>
    </div>

    <!-- Project Modal -->
    <div v-if="selectedProject" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="closeModal">&times;</button>
        <h2 class="modal-title">{{ selectedProject.title }}</h2>
        <p class="modal-description">{{ selectedProject.description }}</p>
        
        <div v-if="hasMedia(selectedProject)" class="modal-media-grid">
          <div
            v-for="(media, idx) in getAllMedia(selectedProject)"
            :key="idx"
            class="modal-media-item"
          >
            <img
              v-if="media.type === 'image'"
              :src="media.url"
              :alt="selectedProject.title"
              @click="openLightbox(media.url)"
              class="modal-image-clickable"
            />
            <div v-else-if="media.type === 'video'" class="modal-video-wrapper" @click="openLightbox(media.url, 'video')">
              <img
                v-if="isYouTube(media.url)"
                :src="getYouTubeThumbnailUrl(media.url)"
                :alt="'Video thumbnail'"
                class="video-thumbnail-img"
              />
              <img
                v-else-if="isVimeo(media.url)"
                :src="getVimeoThumbnailUrl(media.url)"
                :alt="'Video thumbnail'"
                class="video-thumbnail-img"
              />
              <div v-else class="video-placeholder">
                <span>▶ Video</span>
              </div>
              <div class="video-play-overlay">
                <span class="play-icon">▶</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="selectedProject.technologies?.length" class="modal-tech-tags">
          <span
            v-for="(tech, j) in selectedProject.technologies"
            :key="j"
            class="modal-tech-tag"
            >{{ tech }}</span
          >
        </div>

        <a
          v-if="selectedProject.project_url"
          :href="selectedProject.project_url"
          target="_blank"
          class="modal-project-link"
        >
          Visit Project →
        </a>
      </div>
    </div>

    <!-- Lightbox -->
    <div v-if="lightboxImage || lightboxVideo" class="lightbox-overlay" @click="closeLightbox">
      <button class="lightbox-close" @click="closeLightbox">&times;</button>
      <img v-if="lightboxType === 'image'" :src="lightboxImage" class="lightbox-image" @click.stop />
      <div v-else-if="lightboxType === 'video'" class="lightbox-video-container">
        <iframe
          v-if="isYouTube(lightboxVideo)"
          :src="getYouTubeEmbedUrl(lightboxVideo) + '&autoplay=1'"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
          class="lightbox-video"
        ></iframe>
        <iframe
          v-else-if="isVimeo(lightboxVideo)"
          :src="getVimeoEmbedUrl(lightboxVideo) + '?autoplay=1'"
          frameborder="0"
          allow="autoplay; fullscreen; picture-in-picture"
          allowfullscreen
          class="lightbox-video"
        ></iframe>
        <a v-else :href="lightboxVideo" target="_blank" class="lightbox-video-link">
          ▶ Watch Video
        </a>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "PortfolioSection",
  props: ["profile"],
  data() {
    return {
      selectedProject: null,
      lightboxImage: null,
      lightboxVideo: null,
      lightboxType: 'image',
      searchQuery: '',
    };
  },
  computed: {
    projects() {
      const allProjects = (this.profile?.projects || []).filter(
        (proj) => proj.is_visible !== false,
      );
      
      if (!this.searchQuery.trim()) {
        return allProjects;
      }
      
      const query = this.searchQuery.toLowerCase();
      return allProjects.filter(
        (proj) =>
          (proj.title && proj.title.toLowerCase().includes(query)) ||
          (proj.description && proj.description.toLowerCase().includes(query))
      );
    },
  },
  methods: {
    openModal(project) {
      this.selectedProject = project;
      document.body.style.overflow = "hidden";
    },
    closeModal() {
      this.selectedProject = null;
      document.body.style.overflow = "";
    },
    clearSearch() {
      this.searchQuery = '';
    },
    openLightbox(url, type = 'image') {
      this.lightboxType = type;
      if (type === 'video') {
        this.lightboxVideo = url;
        this.lightboxImage = null;
      } else {
        this.lightboxImage = url;
        this.lightboxVideo = null;
      }
    },
    closeLightbox() {
      this.lightboxImage = null;
      this.lightboxVideo = null;
      this.lightboxType = 'image';
    },
    hasMedia(project) {
      return (
        (project.image_url || project.image) ||
        (project.project_images && project.project_images.length > 0) ||
        (project.video_links && project.video_links.length > 0)
      );
    },
    getAllMedia(project) {
      const media = [];
      if (project.image_url || project.image) {
        media.push({ type: "image", url: project.image_url || project.image });
      }
      if (project.project_images && project.project_images.length > 0) {
        project.project_images.forEach((img) => {
          media.push({ type: "image", url: img.image_url || img.image });
        });
      }
      if (project.video_links && project.video_links.length > 0) {
        project.video_links.forEach((video) => {
          media.push({ type: "video", url: video });
        });
      }
      return media;
    },
    isYouTube(url) {
      return url && (url.includes("youtube.com") || url.includes("youtu.be"));
    },
    getYouTubeEmbedUrl(url) {
      const videoId = this.extractYouTubeId(url);
      const embedUrl = videoId ? `https://www.youtube.com/embed/${videoId}?rel=0&modestbranding=1&playsinline=1` : url;
      console.log('YouTube URL:', url, 'Video ID:', videoId, 'Embed URL:', embedUrl);
      return embedUrl;
    },
    extractYouTubeId(url) {
      const regExp =
        /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=|shorts\/)([^#&?]*).*/;
      const match = url.match(regExp);
      return match && match[2].length === 11 ? match[2] : null;
    },
    isVimeo(url) {
      return url && url.includes("vimeo.com");
    },
    getVimeoEmbedUrl(url) {
      const videoId = this.extractVimeoId(url);
      return videoId ? `https://player.vimeo.com/video/${videoId}` : url;
    },
    extractVimeoId(url) {
      const match = url.match(/vimeo\.com\/(\d+)/);
      return match ? match[1] : null;
    },
    handleVideoError(event) {
      console.error('Video failed to load:', event);
    },
    getYouTubeThumbnailUrl(url) {
      const videoId = this.extractYouTubeId(url);
      return videoId ? `https://img.youtube.com/vi/${videoId}/mqdefault.jpg` : '';
    },
    getVimeoThumbnailUrl(url) {
      const videoId = this.extractVimeoId(url);
      return videoId ? `https://vumbnail.com/${videoId}.jpg` : '';
    },
  },
};
</script>

<style scoped>
.portfolio-section {
  background: var(--color-dark-2);
}

.search-container {
  margin-bottom: 2rem;
  position: relative;
}

.search-input {
  width: 100%;
  max-width: 600px;
  padding: 1rem 1.5rem;
  padding-right: 3rem;
  background: var(--color-dark-3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: var(--color-white);
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--color-gold);
  box-shadow: 0 0 0 3px rgba(226, 185, 111, 0.1);
}

.search-input::placeholder {
  color: var(--color-white-50);
}

.clear-search-btn {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: var(--color-white);
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.clear-search-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.portfolio-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.portfolio-card {
  background: var(--color-dark-3);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  display: block;
  text-decoration: none;
  color: inherit;
}

.portfolio-card:hover {
  border-color: rgba(226, 185, 111, 0.25);
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
}

.portfolio-thumb {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.media-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 2px;
  width: 100%;
  height: 100%;
}

.media-item {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.media-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-thumbnail {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000;
}

.video-thumbnail iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.video-link {
  color: var(--color-gold);
  text-decoration: none;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.portfolio-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.portfolio-card:hover .portfolio-thumb img {
  transform: scale(1.05);
}

.thumb-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #1a1a2e, #0f3460);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
  font-family: "Playlist-Script", cursive;
  color: var(--color-gold);
  opacity: 0.7;
}

.portfolio-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(13, 13, 13, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.portfolio-card:hover .portfolio-overlay {
  opacity: 1;
}

.view-label {
  color: var(--color-gold);
  font-weight: 700;
  font-size: 0.9rem;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.portfolio-info {
  padding: 1.5rem;
}

.portfolio-info h3 {
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-white);
  margin-bottom: 0.5rem;
}

.portfolio-info p {
  color: var(--color-white-60);
  font-size: 0.87rem;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.tech-tag {
  background: rgba(226, 185, 111, 0.1);
  color: var(--color-gold);
  border: 1px solid rgba(226, 185, 111, 0.2);
  padding: 0.2rem 0.6rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.empty-state {
  text-align: center;
  color: rgba(255, 255, 255, 0.3);
  padding: 3rem;
  grid-column: 1 / -1;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: var(--color-dark-3);
  border: 1px solid rgba(226, 185, 111, 0.2);
  border-radius: 16px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  padding: 2rem;
  position: relative;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(226, 185, 111, 0.1);
  border: 1px solid rgba(226, 185, 111, 0.3);
  color: var(--color-gold);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.modal-close:hover {
  background: rgba(226, 185, 111, 0.2);
  transform: rotate(90deg);
}

.modal-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--color-white);
  margin-bottom: 1rem;
  padding-right: 3rem;
}

.modal-description {
  color: var(--color-white-70);
  font-size: 1rem;
  line-height: 1.7;
  margin-bottom: 1.5rem;
}

.modal-media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.modal-media-item {
  border-radius: 8px;
  overflow: hidden;
  background: var(--color-dark-2);
}

.modal-media-item img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}

.modal-video-wrapper {
  width: 100%;
  aspect-ratio: 16 / 9;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000;
  cursor: pointer;
  position: relative;
}

.video-thumbnail-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-dark-2);
  color: var(--color-gold);
  font-size: 0.9rem;
}

.video-play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.4);
  transition: background 0.3s;
}

.modal-video-wrapper:hover .video-play-overlay {
  background: rgba(0, 0, 0, 0.6);
}

.play-icon {
  font-size: 3rem;
  color: white;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.modal-video-link {
  color: var(--color-gold);
  text-decoration: none;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.modal-tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.modal-tech-tag {
  background: rgba(226, 185, 111, 0.1);
  color: var(--color-gold);
  border: 1px solid rgba(226, 185, 111, 0.2);
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.modal-project-link {
  display: inline-block;
  background: var(--color-gold);
  color: var(--color-dark-1);
  text-decoration: none;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.modal-project-link:hover {
  background: rgba(226, 185, 111, 0.8);
  transform: translateY(-2px);
}

.modal-image-clickable {
  cursor: pointer;
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.modal-image-clickable:hover {
  transform: scale(1.02);
  opacity: 0.9;
}

/* Lightbox Styles */
.lightbox-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  animation: fadeIn 0.2s ease;
}

.lightbox-close {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  background: rgba(226, 185, 111, 0.1);
  border: 1px solid rgba(226, 185, 111, 0.3);
  color: var(--color-gold);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  font-size: 2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 2001;
}

.lightbox-close:hover {
  background: rgba(226, 185, 111, 0.2);
  transform: rotate(90deg);
}

.lightbox-image {
  max-width: 90vw;
  max-height: 90vh;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
}

.lightbox-video-container {
  width: 90vw;
  max-width: 1200px;
  aspect-ratio: 16 / 9;
}

.lightbox-video {
  width: 100%;
  height: 100%;
  border: none;
  border-radius: 8px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
}

.lightbox-video-link {
  color: white;
  text-decoration: none;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>
