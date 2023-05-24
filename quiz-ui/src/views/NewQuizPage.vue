<template>
  <div class="new-quiz-page">
    <h1 class="title">Nouveau Quiz</h1>

    <div class="form-container">
      <label for="username" class="input-label">Saisissez votre nom :</label>
      <input type="text" id="username" v-model="username" class="text-input" placeholder="Nom d'utilisateur">
      <div v-if="showErrorMessage" class="error-message">Veuillez saisir un nom d'utilisateur</div>
      <button @click="launchNewQuiz" class="start-quiz-button">Démarrer le Quiz</button>
    </div>
  </div>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  data() {
    return {
      username: '',
      showErrorMessage: false
    };
  },
  methods: {
    launchNewQuiz() {
      if (this.username === '') {
        this.showErrorMessage = true;
      } else {
        this.showErrorMessage = false;
        participationStorageService.savePlayerName(this.username);
        this.$router.push('/questions');
      }
    }
  }
};
</script>

<style scoped>
    .error-message {
    color: red;
    font-size: 15px;
    margin-bottom: 10px;
    }

    .form-container {
    align-items: center;
    display: flex;
    flex-direction: column;
    }

    .input-label {
    font-size: 20px;
    margin-bottom: 20px;
    }

    .new-quiz-page {
    margin: 0 auto;
    max-width: 550px;
    padding: 42px;
    text-align: center;
    }

    .start-quiz-button {
    background-color: #4caf50;
    border: none;
    border-radius: 4px;
    color: #fff;
    cursor: pointer;
    display: inline-block;
    font-size: 18px;
    padding: 10px 20px;
    transition: background-color 0.3s ease;
    }

    .start-quiz-button:hover {
    background-color: #45a049;
    }

    .text-input {
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
    margin-bottom: 20px;
    padding: 10px;
    width: 100%;
    }

    .title {
    font-size: 32px;
    margin-bottom: 20px;
    }

    .username-preview {
    font-size: 14px;
    margin-bottom: 20px;
    }
</style>
