<template>
  <div class="max-w-4xl mx-auto mt-10">
    <el-card>
      <h2>My Loan Applications</h2>
      <el-table :data="loans">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="amount" label="Amount" />
        <el-table-column prop="status" label="Status" />
        <el-table-column prop="created_at" label="Date" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const loans = ref([]);

onMounted(async () => {
  const res = await axios.get("/api/loan/list/", {
    headers: { Authorization: `Bearer ${auth.token}` },
  });
  loans.value = res.data;
});
</script>
