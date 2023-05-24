import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/about',
      name: 'AboutPage',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/start-new-quiz-page',
      name: 'NewQuizPage',
      component: () => import('../views/NewQuizPage.vue')
    },
    {
      path: '/questions',
      name: 'QuestionsManager',
      component: () => import('../views/QuestionsManager.vue')
    },
    {
      path: '/results',
      name: 'EndPage',
      component: () => import('../views/EndPage.vue')
    }
  ]
});

export default router;
