import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue";
import Login from "../pages/Login.vue";
import Register from "../pages/Register.vue";
import Profile from "../pages/Profile.vue";
import ProfileEdit from "../pages/ProfileEdit.vue";
import LoanApply from "../pages/LoanApply.vue";
import LoanList from "../pages/LoanList.vue";
import AdminDashboard from "../pages/AdminDashboard.vue";
import { useAuthStore } from "../stores/auth";

import MainLayout from "../layout/MainLayout.vue";
import AdminLayout from "../layout/AdminLayout.vue";
// import AdminLayout from "../layout/AdminLayout.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: MainLayout,
      children: [
        { path: '', name: 'Home', component: Home },
        { path: 'login', name: 'Login', component: Login },
        { path: 'register', name: 'Register', component: Register },
        { path: "/loan/apply", component: LoanApply },
      ],
    },
    {
      path: '/dashboard',
      component: AdminLayout,
      children: [
        { path: '', name: 'Dashboard', component: AdminDashboard },
        { path: "loan", name: 'Loan', component: LoanList },
      ],
    },

    { path: "/profile", component: Profile },
    { path: "/profile/edit", component: ProfileEdit },
    
    
  ],
});

router.beforeEach((to, _from, next) => {
  const auth = useAuthStore();
  const publicPages = ["/", "/login", "/register", "/loan/apply",];
  const authRequired = !publicPages.includes(to.path);

  if (authRequired && !auth.token) return next("/login");
  next();
});

export default router;
