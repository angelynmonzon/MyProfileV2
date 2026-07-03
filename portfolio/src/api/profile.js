import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

const stripMediaHost = (url) => {
  if (!url) return url;
  return url.replace(/^https?:\/\/[^/]+/, "");
};

const normalizeProfile = (profile) => {
  if (!profile) return profile;
  return {
    ...profile,
    profile_image: stripMediaHost(profile.profile_image),
    about_image: stripMediaHost(profile.about_image),
    projects: (profile.projects || []).map((p) => ({
      ...p,
      image: stripMediaHost(p.image),
    })),
    testimonials: (profile.testimonials || []).map((t) => ({
      ...t,
      image: stripMediaHost(t.image),
    })),
    certificates: (profile.certificates || []).map((c) => ({
      ...c,
      image: stripMediaHost(c.image),
    })),
    // Ensure show flags are preserved
    show_services:
      profile.show_services !== undefined ? profile.show_services : true,
    show_skills: profile.show_skills !== undefined ? profile.show_skills : true,
    show_experience:
      profile.show_experience !== undefined ? profile.show_experience : true,
    show_education:
      profile.show_education !== undefined ? profile.show_education : true,
    show_projects:
      profile.show_projects !== undefined ? profile.show_projects : true,
    show_testimonials:
      profile.show_testimonials !== undefined
        ? profile.show_testimonials
        : true,
    show_certificates:
      profile.show_certificates !== undefined
        ? profile.show_certificates
        : true,
  };
};

export const fetchPublicProfile = async () => {
  const response = await api.get("/profiles/public_profile/");
  return normalizeProfile(response.data);
};
