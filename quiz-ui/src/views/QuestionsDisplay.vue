<template>
  <div class="question-container">
    <h1 class="question-indicator">Question {{ question.position }} / {{ totalNumberOfQuestions }}</h1>
    <h2>{{ question.title }}</h2>
    <div class="question-image-wrapper">
      <img v-if="question.image" :src="question.image" class="question-image" />
    </div>
    <p class="question-text" v-html="question.text"></p>
    <div class="answer-buttons">
      <button
        v-for="(answer, index) in question.possibleAnswers"
        :key="index"
        @click="$emit('answer-selected', index)"
        class="answer-button"
      >
        {{ answer.text }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    question: {
      type: Object,
      required: true,
    },
    totalNumberOfQuestions: {
      type: Number,
      required: true,
    },
  },
};
</script>

<style scoped>
  .answer-button {
    align-items: center;
    background-color: #4caf50;
    border: none;
    border-radius: 50px;
    box-shadow: 0px 10px 20px rgba(0,0,0,0.1);
    color: #fff;
    cursor: pointer;
    display: flex;
    font-size: 14px;
    justify-content: center;
    margin-bottom: 15px;
    min-height: 40px;
    padding: 10px 20px;
    transition: background-color 0.3s;
  }

  .answer-button:hover {
    background-color: #45a049;
  }

  .answer-buttons {
    align-items: center;
    display: flex;
    flex-direction: column;
    margin-top: 30px;
    min-height: 180px;
  }

  .question-container {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 90%;
    max-width: 800px;
    padding: 20px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.1);
    text-align: center;
  }

  .question-image {
    border-radius: 10px;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.1);
    max-height: 200px;
    max-width: 300px;
    object-fit: cover;
  }

  .question-image-wrapper {
    display: flex;
    justify-content: center;
    margin-bottom: 30px;
  }

  .question-indicator {
    color: #4caf50;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    text-align: center;
  }

  .question-text {
    color: #666;
    font-size: 20px; 
    line-height: 1.5;
    margin-bottom: 30px;
    padding: 0 10px;
    text-align: justify;
  }

  h2 {
    color: #333;
    font-size: 28px;
    margin-bottom: 30px;
    text-align: center;
  }
</style>