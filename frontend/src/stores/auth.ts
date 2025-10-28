import { defineStore } from "pinia";
import api from "../utils/axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as any,
    token: localStorage.getItem("token") || "",
    refresh_token: localStorage.getItem("refresh") || ""
  }),
  actions: {
    async login(email: string, password: string) {
      console.log(`Call login ${email} ${password}`)
      const { data } = await api.post("account/login", { email, password });
      this.token = data.data.tokens.access;
      this.refresh_token = data.data.tokens.refresh;
      localStorage.setItem("token", data.data.tokens.access);
      localStorage.setItem("refresh", data.data.tokens.refresh);
      this.user = data.data;
    },
    async register(username: string, email: string, password: string, password2: string) {
      await api.post("account/register", { username, email, password, password2 });
    },
    async fetchProfile() {
      const { data } = await api.get("account/properties");
      this.user = data;
    },
    logout() {
      this.user = null;
      this.token = "";
      this.refresh_token = "";
      localStorage.removeItem("token");
      localStorage.removeItem("refresh");
    },
  },
});
