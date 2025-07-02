    var $jq = jQuery.noConflict();
    
    const optionsPanel = document.getElementById('avatar-options-panel');
    const avatarContainer = document.getElementById('avatar-container');
    const avatarSelectButton = document.getElementById('avatar-select-button');
    const minButton = document.getElementById('min-button-wrapper');
    const closeAvatarBtn = document.getElementById('close-avatar');

    function avatar_options() {
        if (avatarContainer.classList.contains('avatar-visible')) {
            showToast("Please close the avatar first!","error")
            return; 
        }
        optionsPanel.classList.toggle('visible');

    }
    
    // Close options panel
    function closeOptionsPanel() {
      optionsPanel.classList.remove('visible');
    }
    
    // Load Avatar
    avatarSelectButton.addEventListener('click', function(e) {
      e.preventDefault();
      const selectedLang = $jq("#avatar-select").val();
      const avatar_selection_options=document.getElementById('avatar-select');
      const selectedOption = avatar_selection_options.options[avatar_selection_options.selectedIndex];
      
      if(selectedLang != $jq("#root").attr('data-language') && selectedLang!="") {
        // Set language and show avatar
        $jq("#root").attr('data-language', selectedLang);
        resetReactApp();
        
        // Update UI
        avatarSelectButton.textContent = 'Close Avatar';
        avatarSelectButton.classList.remove('primary');
        avatarSelectButton.classList.add('danger');
        optionsPanel.classList.remove('visible');
        
        // Show avatar container
        avatarContainer.classList.add('avatar-visible');
        
        // Update language label
        $jq(".avatar-title span").html(`AI Narration - ${selectedOption.innerHTML}`);
      }
    });
    
    // Close Avatar
    closeAvatarBtn.addEventListener('click', function() {
      $jq("#root").attr('data-language', '');
      resetReactApp();
      avatarContainer.classList.remove('avatar-visible');
      
      // Reset options button
      avatarSelectButton.textContent = 'Load Avatar';
      avatarSelectButton.classList.remove('danger');
      avatarSelectButton.classList.add('primary');
    });
    
    // Minimize/Maximize Avatar
    minButton.addEventListener('click', function() {
      const root = document.getElementById('root');
      if(root.style.display !== 'none') {
        root.style.display = 'none';
        minButton.innerHTML = '<i class="fas fa-expand"></i>';
      } else {
        root.style.display = 'block';
        minButton.innerHTML = '<i class="fas fa-minus"></i>';
      }
    });
  
    const reactRoot = document.getElementById("root");
    // Simulate functions
function resetReactApp() {
   var language=$jq("#root").attr('data-language');
    if (reactRoot) {
      if (window.resetAudio) {
         window.resetAudio(language); 
       }
    }
    setTimeout(() => {
    const root = document.getElementById('root');
    if (root) {
      root.style.display = 'none';
      minButton.innerHTML = '<i class="fas fa-expand"></i>';
      setTimeout(() => {
        root.style.display = 'block';
        minButton.innerHTML = '<i class="fas fa-minus"></i>';
      }, 50);
    }
  }, 300);
}
    
    // Initialize
    $jq(document).ready(function() {
      optionsPanel.classList.remove('visible');
    });