<script setup lang="ts">
import { useAuthStore } from "../stores/auth";
import { useForm } from "vee-validate";
import * as yup from "yup";
import { ref } from "vue";

// access auth store
const auth = useAuthStore();

// form validation schema
const schema = yup.object({
  username: yup.string().required("Username is required"),
  email: yup.string().email("Invalid email").required("Email is required"),
  password: yup.string().min(6, "Password must be at least 6 characters").required("Password is required"),
  password2: yup
    .string()
    .oneOf([yup.ref("password")], "Passwords must match")
    .required("Confirm your password"),
});

// vee-validate form setup
const { handleSubmit, errors, defineField, isSubmitting } = useForm({
  validationSchema: schema,
});

const [username, usernameAttrs] = defineField("username");
const [email, emailAttrs] = defineField("email");
const [password, passwordAttrs] = defineField("password");
const [password2, password2Attrs] = defineField("password2");

const message = ref("");

const onSubmit = handleSubmit(async (values) => {
  try {
    await auth.register(values.username, values.email, values.password, values.password2);
    message.value = "Registration successful! You can now log in.";
  } catch (error: any) {
    message.value = error.response?.data?.message || "Registration failed.";
  }
});
</script>

<template>
  <div class="flex justify-center items-center min-h-screen bg-gray-100">
    <div class="bg-white p-8 rounded shadow-md w-full max-w-md">
      <h2 class="text-2xl font-semibold mb-6 text-center">Create an Account</h2>

      <form @submit.prevent="onSubmit" class="space-y-4">
        <!-- Username -->
        <div>
          <label class="block text-sm font-medium mb-1">Username</label>
          <input
            v-model="username"
            v-bind="usernameAttrs"
            type="text"
            class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <p v-if="errors.username" class="text-red-500 text-sm mt-1">{{ errors.username }}</p>
        </div>

        <!-- Email -->
        <div>
          <label class="block text-sm font-medium mb-1">Email</label>
          <input
            v-model="email"
            v-bind="emailAttrs"
            type="email"
            class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <p v-if="errors.email" class="text-red-500 text-sm mt-1">{{ errors.email }}</p>
        </div>

        <!-- Password -->
        <div>
          <label class="block text-sm font-medium mb-1">Password</label>
          <input
            v-model="password"
            v-bind="passwordAttrs"
            type="password"
            class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <p v-if="errors.password" class="text-red-500 text-sm mt-1">{{ errors.password }}</p>
        </div>

        <!-- Confirm Password -->
        <div>
          <label class="block text-sm font-medium mb-1">Confirm Password</label>
          <input
            v-model="password2"
            v-bind="password2Attrs"
            type="password"
            class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <p v-if="errors.password2" class="text-red-500 text-sm mt-1">{{ errors.password2 }}</p>
        </div>

        <!-- Submit -->
        <button
          type="submit"
          :disabled="isSubmitting"
          class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {{ isSubmitting ? "Registering..." : "Register" }}
        </button>

        <!-- Message -->
        <p v-if="message" class="text-center text-sm mt-4" :class="message.includes('success') ? 'text-green-600' : 'text-red-500'">
          {{ message }}
        </p>
      </form>
    </div>
  </div>
</template>
