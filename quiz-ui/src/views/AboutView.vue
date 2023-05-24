<template>
  <div class="about">
    <h1>About page</h1>
    <div class="about-content">
      <p>Ce site web a été réalisé par le Groupe 12 composé de Melvyn DAO et Matthieu PHOMMACHANH dans le cadre de l'unité 4I-IN6 Web Full Stack.</p>
    </div>
  </div>
</template>
<style scoped>
.about {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.about-content {
  margin-top: 20px;
}

@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    align-items: flex-start;
    padding-left: 40px;
  }
}
</style>