import { defineStore } from "pinia";
import api from "../utils/axios";

export const useLoanStore = defineStore("loan", {
  state: () => ({
    loans: [] as any[],
  }),
  actions: {
    async fetchLoans() {
      const { data } = await api.get("loan/applications/");
      this.loans = data;
    },
    async applyLoan(payload: any) {
      const { data } = await api.post("loan/applications/", payload);
      return data;
    },
  },
});
