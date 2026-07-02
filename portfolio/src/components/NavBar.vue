<template>
  <header class="navbar" :class="{ scrolled: isScrolled }">
    <div class="nav-container">
      <a href="#hero" class="nav-logo" @click.prevent="scrollTo('#hero')">
        <span class="script">Ging</span>
      </a>
      <nav class="nav-links" :class="{ open: menuOpen }">
        <a href="#about" @click.prevent="scrollTo('#about')">About</a>
        <a v-if="profile?.show_services" href="#services" @click.prevent="scrollTo('#services')">Services</a>
        <a v-if="profile?.show_skills" href="#skills" @click.prevent="scrollTo('#skills')">Skills</a>
        <a v-if="profile?.show_experience" href="#experience" @click.prevent="scrollTo('#experience')">Experience</a>
        <a v-if="profile?.show_education" href="#education" @click.prevent="scrollTo('#education')">Education</a>
        <a v-if="profile?.show_projects" href="#portfolio" @click.prevent="scrollTo('#portfolio')">Portfolio</a>
        <a v-if="profile?.show_testimonials" href="#testimonials" @click.prevent="scrollTo('#testimonials')">Testimonials</a>
        <a v-if="profile?.show_certificates" href="#certificates" @click.prevent="scrollTo('#certificates')">Certificates</a>
        <a href="#contact" @click.prevent="scrollTo('#contact')" class="nav-cta">Contact</a>
      </nav>
      <button class="hamburger" @click="menuOpen = !menuOpen" :class="{ active: menuOpen }">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
  </header>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'NavBar',
  props: ['profile'],
  setup() {
    const isScrolled = ref(false)
    const menuOpen = ref(false)

    const onScroll = () => {
      isScrolled.value = window.scrollY > 50
    }

    const scrollTo = (hash) => {
      menuOpen.value = false
      const el = document.querySelector(hash)
      if (el) el.scrollIntoView({ behavior: 'smooth' })
    }

    onMounted(() => window.addEventListener('scroll', onScroll))
    onUnmounted(() => window.removeEventListener('scroll', onScroll))

    return { isScrolled, menuOpen, scrollTo }
  }
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  padding: 1.25rem 0;
  transition: all 0.3s ease;
}

.navbar.scrolled {
  background: rgba(13, 13, 13, 0.95);
  backdrop-filter: blur(10px);
  padding: 0.75rem 0;
  box-shadow: 0 2px 20px rgba(0,0,0,0.5);
}

.nav-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-logo .script {
  font-family: 'Playlist-Script', cursive;
  font-size: 2rem;
  margin-right: 1rem;
  color: var(--color-gold);
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-links a {
  color: var(--color-white-80);
  font-size: 0.85rem;
  font-weight: 500;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: color 0.3s;
  position: relative;
}

.nav-links a::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--color-gold);
  transition: width 0.3s;
}

.nav-links a:hover {
  color: var(--color-gold);
}

.nav-links a:hover::after {
  width: 100%;
}

.nav-cta {
  background: linear-gradient(135deg, #e2b96f, #c9993a);
  color: #0d0d0d !important;
  padding: 0.5rem 1.25rem;
  border-radius: 20px;
  font-weight: 700 !important;
}

.nav-cta::after {
  display: none;
}

.nav-cta:hover {
  color: #0d0d0d !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(226,185,111,0.4);
}

.hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
}

.hamburger span {
  display: block;
  width: 24px;
  height: 2px;
  background: var(--color-white);
  transition: all 0.3s;
  border-radius: 2px;
}

.hamburger.active span:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.hamburger.active span:nth-child(2) {
  opacity: 0;
}

.hamburger.active span:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

@media (max-width: 768px) {
  .hamburger {
    display: flex;
  }

  .nav-links {
    position: fixed;
    top: 0;
    right: -100%;
    width: 75%;
    height: 100vh;
    background: #161616;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 2.5rem;
    transition: right 0.4s ease;
  }

  .nav-links.open {
    right: 0;
  }

  .nav-links a {
    font-size: 1rem;
  }
}
</style>
