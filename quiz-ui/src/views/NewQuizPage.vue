<template>
  <link href="https://fonts.cdnfonts.com/css/pokemon-solid" rel="stylesheet">
                
  <div class="new-quiz-page">
    <h1 class="title">Ravi de faire ta connaissance !</h1>

    <div class="form-container">
      <label for="username" class="input-label">Comment t'appelles-tu, jeune dresseur ?</label>
      <input type="text" id="username" v-model="username" class="text-input" placeholder="Sacha">
      <div v-if="showErrorMessage" class="error-message">Tu n'as pas de prénom, jeune dresseur ?</div>
      <button @click="launchNewQuiz" class="start-quiz-button">Attrapez-les tous !</button>
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
  color: #FFCB05;
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
  color: #FFCB05;
}

.new-quiz-page {
  margin: 0 auto;
  max-width: 550px;
  padding: 42px;
  text-align: center;
  background-color: #3D7DCA;
  color: #FFF;
  border-radius: 20px;
}

.start-quiz-button {
  background-color: #FF5959;
  border: none;
  border-radius: 4px;
  color: #FFF;
  cursor: pointer;
  display: inline-block;
  font-size: 18px;
  padding: 10px 20px;
  transition: background-color 0.3s ease;
}

.start-quiz-button:hover {
  background-color: #FF0000;
}

.text-input {
  border: 1px solid #FFCB05;
  border-radius: 4px;
  font-size: 16px;
  margin-bottom: 20px;
  padding: 10px;
  width: 100%;
}

.title {
  font-family: "Pokemon Solid", sans-serif;
  font-size: 32px;
  margin-bottom: 20px;
}

.username-preview {
  font-size: 14px;
  margin-bottom: 20px;
}
</style>
