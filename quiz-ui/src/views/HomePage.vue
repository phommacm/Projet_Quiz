<template>
  <div class="home-page">
    <h1 class="title">Bienvenue sur le Quiz du Groupe 12</h1>

    <div class="score-list">
      <div v-for="scoreEntry in registeredScores" :key="scoreEntry.date" class="score-entry">
        <span class="player-name">{{ scoreEntry.playerName }}</span>
        <span class="score">{{ scoreEntry.score }}</span>
      </div>
    </div>

    <router-link to="/start-new-quiz-page" class="start-quiz-button">Démarrer le quiz !</router-link>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: [],
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
  },
};
</script>

<style scoped>
  .home-page {
    margin: 0 auto;
    max-width: 800px;
    padding: 40px;
    text-align: center;
  }

  .player-name {
    font-weight: bold;
  }

  .score {
    color: #888;
  }

  .score-entry {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
  }

  .score-list {
    margin-bottom: 40px;
  }

  .start-quiz-button {
    background-color: #4caf50;
    border-radius: 4px;
    color: #fff;
    display: inline-block;
    font-size: 18px;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    transition: background-color 0.3s ease;
  }

  .start-quiz-button:hover {
    background-color: #45a049;
    color: #d5f6cd;
  }

  .title {
    font-size: 32px;
    margin-bottom: 40px;
  }
</style>