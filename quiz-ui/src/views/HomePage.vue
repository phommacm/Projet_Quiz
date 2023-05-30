<template>
  <link href="https://fonts.cdnfonts.com/css/pokemon-solid" rel="stylesheet">

  <div class="home-page">
    <h1 class="title">Bienvenue dans l'univers Pokémon !</h1>

    <h2 class="leaderboard">Leaderboard</h2>

    <div class="score-list" :class="{'scrollable': registeredScores.length > 5}">
      <div v-if="registeredScores.length === 0" class="empty-leaderboard">
        Aucun dresseur dans les environs
      </div>
      <div v-else>
        <div v-for="(scoreEntry, index) in registeredScores.slice(0, 10)" :key="scoreEntry.date" :class="['score-entry', getScoreEntryClass(index)]">
          <div class="player-container">
            <span class="player-name">{{ scoreEntry.playerName }}</span>
          </div>
          <div class="score-container">
            <span class="score">{{ scoreEntry.score }}</span>
          </div>
        </div>
      </div>
    </div>

    <router-link to="/start-new-quiz-page" class="start-quiz-button">Es-tu prêt à relever le défi ?</router-link>
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
  methods: {
    getScoreEntryClass(index) {
      if (index === 0) {
        return "gold";
      } else if (index === 1) {
        return "silver";
      } else if (index === 2) {
        return "bronze";
      } else {
        return "";
      }
    },
  },
};
</script>

<style scoped>
  .home-page {
    background-color: #3D7DCA;
    border-radius: 20px;
    color: #FFF;
    margin: 0 auto;
    max-width: 800px;
    padding: 40px;
    text-align: center;
  }

  .empty-leaderboard {
    background-color: #FF5959;
    border-radius: 10px;
    box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    color: #FFF;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100px;
    margin-bottom: 10px;
  }

  .leaderboard {
    color: #FFCB05;
    font-size: 24px;
    margin-bottom: 20px;
    text-shadow: none;
  }

  .player-container {
    flex: 1;
    text-align: left;
  }

  .player-name {
    color: #FFF;
    font-weight: bold;
  }

  .score {
    color: #FFF;
  }

  .score-container {
    flex: 1;
    text-align: right;
  }

  .score-entry {
    background-color: #FF5959;
    border-radius: 10px;
    box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
    padding: 10px;
  }

  .score-entry.gold {
    background-color: #FFCB05; 
  }

  .score-entry.silver {
    background-color: silver;
  }

  .score-entry.bronze {
    background-color: #cd7f32;
  }

  .score-list {
    margin-bottom: 40px;
    max-height: 200px;
    overflow-y: auto;
  }

  .score-list.scrollable {
    overflow-x: hidden;
  }

  .start-quiz-button {
    background-color: #FF5959;
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
    background-color: #FF0000;
  }

  .title {
    font-family: "Pokemon Solid", sans-serif;
    font-size: 32px;
    margin-bottom: 40px;
  }
</style>
