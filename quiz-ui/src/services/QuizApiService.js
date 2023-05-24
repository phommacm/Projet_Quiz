import axios from "axios";

const instance = axios.create({
	baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
    };
    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error(error);
      });
  },
  async getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  async addQuestion(question) {
    return this.call("post", "questions", question);
  },
  async deleteAllQuestions() {
    return this.call("delete", "questions/all");
  },
  async deleteQuestionById(questionId) {
    return this.call("delete", `questions/${questionId}`);
  },
  async deleteAllParticipations() {
    return this.call("delete", "participations/all");
  },
  async getQuestionById(questionId) {
    return this.call("get", `questions/${questionId}`);
  },
  async getQuestionByPosition(position) {
    return this.call("get", `questions?position=${position}`);
  },
  async updateQuestion(questionId, question) {
    return this.call("put", `questions/${questionId}`, question);
  },
  async addParticipation(participationData) {
    return this.call("post", "participations", participationData);
  },
  async rebuildDatabase() {
    return this.call("post", "rebuild-db");
  },
};