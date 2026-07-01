<template>
  <div id="app">
    <NavBar :profile="profile" />
    <router-view :profile="profile" :loading="loading" />
    <FooterSection :profile="profile" />
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import NavBar from './components/NavBar.vue'
import FooterSection from './components/FooterSection.vue'
import { fetchPublicProfile } from './api/profile.js'

export default {
  name: 'App',
  components: { NavBar, FooterSection },
  setup() {
    const profile = ref(null)
    const loading = ref(true)

    const initReveal = () => {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible')
            observer.unobserve(entry.target)
          }
        })
      }, { threshold: 0, rootMargin: '0px 0px -40px 0px' })

      document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach(el => {
        const rect = el.getBoundingClientRect()
        if (rect.top < window.innerHeight && rect.bottom > 0) {
          el.classList.add('visible')
        } else {
          observer.observe(el)
        }
      })
    }

    const checkVisible = () => {
      document.querySelectorAll('.reveal:not(.visible), .reveal-left:not(.visible), .reveal-right:not(.visible)').forEach(el => {
        const rect = el.getBoundingClientRect()
        if (rect.top < window.innerHeight - 40 && rect.bottom > 0) {
          el.classList.add('visible')
        }
      })
    }

    onMounted(async () => {
      try {
        const data = await fetchPublicProfile()
        profile.value = data.length > 0 ? data[0] : null
      } catch (err) {
        console.error('Failed to load profile:', err)
      } finally {
        loading.value = false
        await nextTick()
        initReveal()
        setTimeout(checkVisible, 100)
      }
      window.addEventListener('scroll', checkVisible, { passive: true })
    })

    onUnmounted(() => {
      window.removeEventListener('scroll', checkVisible)
    })

    return { profile, loading }
  }
}
</script>
