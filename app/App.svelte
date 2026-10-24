<script>
  import { onDestroy, onMount } from 'svelte';
  import * as Blockly from 'blockly';

  let video;
  let stream;
  let error = '';
  let active = false;
  let blocklyElement;
  let workspace;
  let generatedCode = '';

  const toolbox = {
    kind: 'categoryToolbox',
    contents: [
      {
        kind: 'category', name: 'Logic', colour: 210,
        contents: [
          { kind: 'block', type: 'controls_if' },
          { kind: 'block', type: 'logic_compare' },
          { kind: 'block', type: 'logic_boolean' },
        ],
      },
      {
        kind: 'category', name: 'Loops', colour: 120,
        contents: [{ kind: 'block', type: 'controls_repeat_ext' }],
      },
      {
        kind: 'category', name: 'Math', colour: 230,
        contents: [
          { kind: 'block', type: 'math_number' },
          { kind: 'block', type: 'math_arithmetic' },
        ],
      },
      {
        kind: 'category', name: 'Text', colour: 160,
        contents: [
          { kind: 'block', type: 'text' },
          { kind: 'block', type: 'text_print' },
        ],
      },
    ],
  };

  async function startCamera() {
    error = '';
    if (!navigator.mediaDevices?.getUserMedia) {
      error = 'Camera access requires HTTPS or localhost.';
      return;
    }
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' }, audio: false });
      video.srcObject = stream;
      active = true;
    } catch (err) {
      error = `${err.name}: ${err.message}`;
    }
  }

  function stopCamera() {
    stream?.getTracks().forEach((track) => track.stop());
    stream = null;
    if (video) video.srcObject = null;
    active = false;
  }

  function updateCode() {
    generatedCode = workspace ? `${workspace.getAllBlocks(false).length} block(s) selected` : '';
  }

  onMount(() => {
    workspace = Blockly.inject(blocklyElement, {
      toolbox,
      grid: { spacing: 20, length: 3, colour: '#ddd', snap: true },
      zoom: { controls: true, wheel: true },
      trashcan: true,
    });
    workspace.addChangeListener(updateCode);
    updateCode();
  });

  onDestroy(() => {
    stopCamera();
    workspace?.dispose();
  });
</script>

<main>
  <h1>Camera test</h1>
  <p>Click the button and allow Firefox to use your camera.</p>
  <video bind:this={video} autoplay muted playsinline></video>
  {#if active}
    <button on:click={stopCamera}>Stop camera</button>
  {:else}
    <button on:click={startCamera}>Start camera</button>
  {/if}
  {#if error}<p class="error">{error}</p>{/if}

  <h2>Blockly test</h2>
  <div bind:this={blocklyElement} class="blockly"></div>
  <h3>Generated JavaScript</h3>
  <pre>{generatedCode || '// Add blocks to generate code'}</pre>
</main>

<style>
  main {
    max-width: 720px;
    margin: 2rem auto;
    padding: 0 1rem;
    font-family: system-ui, sans-serif;
  }

  video {
    display: block;
    width: 100%;
    min-height: 240px;
    margin: 1.5rem 0;
    background: #111;
    border-radius: 0.75rem;
    object-fit: cover;
  }

  button {
    padding: 0.7rem 1rem;
    border: 0;
    border-radius: 0.5rem;
    background: #2563eb;
    color: white;
    cursor: pointer;
  }

  .error {
    color: #b91c1c;
  }

  .blockly {
    width: 100%;
    height: 480px;
    border: 1px solid #d1d5db;
    border-radius: 0.75rem;
    overflow: hidden;
  }

  pre {
    min-height: 4rem;
    padding: 1rem;
    overflow: auto;
    background: #111827;
    color: #e5e7eb;
    border-radius: 0.5rem;
  }
</style>
