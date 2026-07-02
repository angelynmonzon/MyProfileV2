<template>
  <div class="home">
    <div v-if="loading" class="page-loader">
      <div class="loader-ring"></div>
      <p class="script">Loading...</p>
    </div>
    <template v-else>
      <HeroSection :profile="profile" />
      <AboutSection :profile="profile" />
      <ServicesSection v-if="profile.show_services" :profile="profile" />
      <SkillsSection v-if="profile.show_skills" :profile="profile" />
      <ExperienceSection v-if="profile.show_experience" :profile="profile" />
      <EducationSection v-if="profile.show_education" :profile="profile" />
      <PortfolioSection v-if="profile.show_projects" :profile="profile" />
      <ContactSection :profile="profile" />
    </template>
  </div>
</template>

<script>
import HeroSection from "../components/HeroSection.vue";
import AboutSection from "../components/AboutSection.vue";
import ServicesSection from "../components/ServicesSection.vue";
import SkillsSection from "../components/SkillsSection.vue";
import ExperienceSection from "../components/ExperienceSection.vue";
import EducationSection from "../components/EducationSection.vue";
import PortfolioSection from "../components/PortfolioSection.vue";
import ContactSection from "../components/ContactSection.vue";

export default {
  name: "Home",
  components: {
    HeroSection,
    AboutSection,
    ServicesSection,
    SkillsSection,
    ExperienceSection,
    EducationSection,
    PortfolioSection,
    ContactSection,
  },
  props: ["profile", "loading"],
};
</script>

<style scoped>
.page-loader {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
}

.loader-ring {
  width: 50px;
  height: 50px;
  border: 3px solid rgba(226, 185, 111, 0.15);
  border-top-color: var(--color-gold);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.page-loader .script {
  font-family: "Playlist-Script", cursive;
  font-size: 1.8rem;
  color: var(--color-gold);
  opacity: 0.7;
}
</style>
