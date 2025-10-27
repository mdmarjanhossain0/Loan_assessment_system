<template>
  <div class="w-1/3 mx-auto mt-10">
    <el-card>
      <h2>Login</h2>
      <el-form :model="form" @submit.prevent="onSubmit">
        <el-form-item label="Email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="Password">
          <el-input type="password" v-model="form.password" />
        </el-form-item>
        <el-button type="primary" @click="onSubmit">Login</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const form = reactive({ email: "", password: "" });
const auth = useAuthStore();
const router = useRouter();

const onSubmit = async () => {
  await auth.login(form.email, form.password);
  router.push(auth.user.role === "Admin" ? "/admin" : "/profile");
};
</script>
