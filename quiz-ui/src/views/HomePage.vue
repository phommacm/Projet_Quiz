<template>
  <h1>Home page</h1>

  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
  {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>

  <router-link to="/start-new-quiz-page" class="start-quiz-button">Démarrer le quiz !</router-link>
</template>

<script>
 import quizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: []  
    };
  },
  async created() {
		console.log("Composant Home page 'created'");

    try {
      const response = await quizApiService.getQuizInfo();
      this.registeredScores = response.data.scores;
    } catch (error) {
      console.error(error);
    }
  }
};
</script>

<style>
  .start-quiz-button {
    display: inline-block;
    padding: 10px 20px;
    font-size: 18px;
    text-align: center;
    background-color: #4caf50;
    color: #fff;
    text-decoration: none;
    border-radius: 4px;
    transition: background-color 0.3s ease;
  }

  .start-quiz-button:hover {
    background-color: #45a049;
    color: #d5f6cd;
  }
</style>
