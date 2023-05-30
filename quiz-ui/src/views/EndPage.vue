<template>
  <link href="https://fonts.cdnfonts.com/css/pokemon-solid" rel="stylesheet">

  <div class="end-page">
    <h1>{{ getTitle() }}</h1>
    <p>Participant : {{ playerName }}</p>
    <p>Score : {{ finalScore }} / 10</p>
  </div>
</template>

<script>
import ParticipationStorageService from "@/services/ParticipationStorageService";

export default {
  data() {
    return {
      playerName: "",
      finalScore: 0,
    };
  },
  created() {
    this.playerName = ParticipationStorageService.getPlayerName();
    this.finalScore = ParticipationStorageService.getParticipationScore();
  },
  methods: {
    getTitle() {
      if (this.finalScore >= 0 && this.finalScore <= 4) {
        return "Oh non ! Tu feras mieux la prochaine fois !";
      } else if (this.finalScore >= 5 && this.finalScore <= 8) {
        return "Pas mal ! Continues comme ça !";
      } else if (this.finalScore === 9) {
        return "Bien joué !";
      } else if (this.finalScore === 10) {
        return "Excellent !";
      } else {
        return "Fin !";
      }
    },
  },
};
</script>

<style scoped>
  .end-page {
    background-color: #3D7DCA;
    border-radius: 20px;
    color: #FFF;
    margin: 0 auto;
    max-width: 550px;
    padding: 42px;
    text-align: center;
  }

  h1 {
    color: #FFF;
    font-family: "Pokemon Solid", sans-serif;
    font-size: 24px;
    margin-bottom: 20px;
  }

  p {
    color: #FFCB05;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
  }
</style>
