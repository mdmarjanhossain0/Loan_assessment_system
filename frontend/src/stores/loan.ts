import { defineStore } from "pinia";
import api from "../utils/axios";

export const useLoanStore = defineStore("loan", {
  state: () => ({
    loans: [] as any[],
    loanDetail: null as any,
  }),
  actions: {
    async fetchLoans(page: number = 1) {
      try {
        const { data } = await api.get(`loan/applications/?page=${page}`);
        this.loans = data.results;
        return data;
      } catch (error) {
        console.error("Error fetching loans:", error);
        throw error;
      }
    },
    async getLoanDetail(pk: number) {
      try {
        const { data } = await api.get(`loan/applications/${pk}/`);
        this.loanDetail = data
        return data;
      } catch (error) {
        console.error("Error fetching loans:", error);
        throw error;
      }
    },

    async applyLoan(payload: any) {
      try {
        const { data } = await api.post("loan/applications/", payload);
        return data;
      } catch (error) {
        console.error("Error applying for loan:", error);
        throw error;
      }
    },
    async updateLoan(payload: any) {
      try {
        const { data } = await api.patch(`loan/applications/${payload.id}/`, payload);
        await this.fetchLoans()
        return data;
      } catch (error) {
        console.error("Error applying for loan:", error);
        throw error;
      }
    },
  },
});
