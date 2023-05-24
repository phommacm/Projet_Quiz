<template>
  <div class="end-page">
    <h1>Fin !</h1>
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
};
</script>

<style scoped>
  .end-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }

  h1 {
    font-size: 24px;
    margin-bottom: 20px;
  }

  p {
    font-size: 18px;
    margin-bottom: 10px;
  }
</style>
