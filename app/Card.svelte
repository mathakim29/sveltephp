<script>
  import dayjs from 'dayjs';

  let { title } = $props();
  let time = dayjs().format('HH:mm:ss');
</script>

<div class="card">
  <h3>{title}</h3>
  <p>Loaded at {time}</p>
</div>

<style>
  .card {
    border: 1px solid #ddd;
    padding: 1rem;
    border-radius: 6px;
  }
</style>
