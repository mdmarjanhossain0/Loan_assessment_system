import { defineStore } from "pinia";
import api from "../utils/axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as any,
    token: localStorage.getItem("token") || "",
  }),
  actions: {
    async login(email: string, password: string) {
      const { data } = await api.post("auth/login/", { email, password });
      this.token = data.token;
      localStorage.setItem("token", data.token);
      this.user = data.user;
    },
    async register(username: string, email: string, password: string) {
      await api.post("auth/register/", { username, email, password });
    },
    async fetchProfile() {
      const { data } = await api.get("auth/profile/");
      this.user = data;
    },
    logout() {
      this.user = null;
      this.token = "";
      localStorage.removeItem("token");
    },
  },
});
