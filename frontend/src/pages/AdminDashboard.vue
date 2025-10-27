<template>
  <div class="max-w-5xl mx-auto mt-10">
    <el-card>
      <h2>Admin Dashboard</h2>
      <el-table :data="users">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="Username" />
        <el-table-column prop="email" label="Email" />
        <el-table-column prop="role" label="Role" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const users = ref([]);

onMounted(async () => {
  const res = await axios.get("/api/account/list/", {
    headers: { Authorization: `Bearer ${auth.token}` },
  });
  users.value = res.data;
});
</script>
