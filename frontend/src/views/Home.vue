<template>
  <div class="home">
    <h1>Welcome to MTG Mulligan Trainer</h1>
    <p class="subtitle">Practice your mulligan decisions with the Magic: The Gathering community</p>

    <div class="features">
      <div class="feature-card">
        <h3>Vote on Scenarios</h3>
        <p>Help others learn by voting on Keep or Mulligan decisions</p>
        <router-link to="/scenarios" class="btn">View Scenarios</router-link>
      </div>

      <div class="feature-card">
        <h3>Upload Decklists</h3>
        <p>Share your decklists and generate practice scenarios</p>
        <router-link to="/decklists" class="btn">Browse Decklists</router-link>
      </div>

      <div class="feature-card">
        <h3>Create Scenarios</h3>
        <p>Generate mulligan scenarios from any decklist</p>
        <router-link to="/scenarios/new" class="btn btn-primary">Create Now</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  text-align: center;
}

h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.2rem;
  color: #7f8c8d;
  margin-bottom: 3rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.feature-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #7f8c8d;
  margin-bottom: 1.5rem;
}

.btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background 0.2s;
}

.btn:hover {
  background: #2980b9;
}

.btn-primary {
  background: #2ecc71;
}

.btn-primary:hover {
  background: #27ae60;
}
</style>
