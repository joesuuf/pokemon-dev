<script lang="ts">
  // No timer, just a spinning pokeball
</script>

<div class="spinner-container">
  <div class="pokeball">
    <div class="pokeball-top"></div>
    <div class="pokeball-bottom"></div>
    <div class="pokeball-middle"></div>
    <div class="pokeball-button"></div>
  </div>
</div>

<style>
  .spinner-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
  }

  .pokeball {
    position: relative;
    width: 80px;
    height: 80px;
    animation: spin 1.5s linear infinite;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .pokeball-top,
  .pokeball-bottom {
    position: absolute;
    width: 80px;
    height: 40px;
    border-radius: 80px 80px 0 0;
  }

  .pokeball-top {
    background: #e74c3c;
    top: 0;
    border-bottom: 3px solid #2c3e50;
  }

  .pokeball-bottom {
    background: #ffffff;
    bottom: 0;
    border-radius: 0 0 80px 80px;
    border-top: 3px solid #2c3e50;
  }

  .pokeball-middle {
    position: absolute;
    width: 80px;
    height: 8px;
    background: #2c3e50;
    top: 50%;
    transform: translateY(-50%);
    z-index: 2;
  }

  .pokeball-button {
    position: absolute;
    width: 24px;
    height: 24px;
    background: #ffffff;
    border: 4px solid #2c3e50;
    border-radius: 50%;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 3;
    box-shadow: inset 0 0 0 2px #ffffff;
  }

  .pokeball-button::after {
    content: '';
    position: absolute;
    width: 10px;
    height: 10px;
    background: #2c3e50;
    border-radius: 50%;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
</style>