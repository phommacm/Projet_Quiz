<template>
  <div class="page-wrapper">
    <div class="content-wrapper">
      <QuestionDisplay
        v-if="currentQuestion"
        :question="currentQuestion"
        :totalNumberOfQuestions="totalNumberOfQuestions"
        @answer-selected="answerClickedHandler"
      />
    </div>
  </div>
</template>

<script>
import QuizApiService from "@/services/QuizApiService";
import QuestionDisplay from "./QuestionsDisplay.vue";
import ParticipationStorageService from "@/services/ParticipationStorageService";

export default {
  components: {
    QuestionDisplay,
  },
  data() {
    return {
      totalNumberOfQuestions: 0,
      currentQuestion: null,
      currentQuestionPosition: 1,
      selectedAnswers: [],
      questions: [],
    };
  },
  async created() {
    try {
      const { data } = await QuizApiService.getQuizInfo();
      this.totalNumberOfQuestions = data.size;
      if (this.totalNumberOfQuestions > 0) {
        await this.loadQuestionByPosition(this.currentQuestionPosition);
      }
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async loadQuestionByPosition(position) {
      try {
        const { data } = await QuizApiService.getQuestionByPosition(position);
        this.currentQuestion = data;
        this.questions.push(data);
      } catch (error) {
        console.error(error);
      }
    },
    async answerClickedHandler(answerIndex) {
      this.selectedAnswers.push(answerIndex + 1);

      if (this.currentQuestionPosition < this.totalNumberOfQuestions) {
        this.currentQuestionPosition++;
        await this.loadQuestionByPosition(this.currentQuestionPosition);
      } else {
        this.endQuiz();
      }
    },
    async endQuiz() {
      try {
        const playerName = ParticipationStorageService.getPlayerName();
        const participationScore = this.selectedAnswers.map((answerIndex, i) => {
          const selectedAnswer = this.questions[i].possibleAnswers[answerIndex - 1];
          return selectedAnswer.isCorrect ? 1 : 0;
        });

        const finalScore = participationScore.reduce((a, b) => a + b, 0);
        ParticipationStorageService.saveParticipationScore(finalScore);

        await QuizApiService.addParticipation({
          playerName: playerName,
          answers: this.selectedAnswers
        });

        this.$router.push("/results");
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
  .content-wrapper {
    align-items: center;
    display: flex;
    flex-grow: 1;
    justify-content: center;
  }

  .content-wrapper img {
    max-height: 400px;
    max-width: 100%;
  }

  .page-wrapper {
    align-items: center;
    display: flex;
    flex-direction: column;
    height: 100vh;
    justify-content: center;
  }

  .question-indicator {
    left: 10px;
    position: absolute;
    top: 10px;
  }
</style>