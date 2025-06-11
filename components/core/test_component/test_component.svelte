<script>
  export let message = "Test OK";
  export let status = "success";
</script>

<div class={`px-3 py-2 rounded text-xs font-mono mb-2 
  ${status === 'success' ? 'bg-green-100 text-green-700 border border-green-300' : ''}
  ${status === 'error' ? 'bg-red-100 text-red-700 border border-red-300' : ''}
  ${status === 'info' ? 'bg-gray-100 text-gray-700 border border-gray-300' : ''}
`}>
  {message}
</div> 