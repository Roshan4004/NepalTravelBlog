const synth = window.speechSynthesis;
var $jq = jQuery.noConflict();
function read(){
   var $jq = jQuery.noConflict();
      if($jq("#read-box").css("display")=="flex"){
         $jq("#read-box").css("display","none");
         synth.cancel()
         $jq("#play-button").attr("src","/static/blog/play.png")
      }else{
         $jq("#read-box").css("display","flex");
      }
}

function avatar_options(){
   var $jq = jQuery.noConflict();
      if($jq("#avatar-box").css("display")=="flex"){
         $jq("#avatar-box").css("display","none");
         $jq("#root").attr('data-language','');
         $jq("#sidebar-user").css("display","block");
         $jq("#sidebar-avatar").css("display","none");
         $jq("#avatar-mobile").css("display","none");
         $jq("#tooltip-avatar").html("AI narration video");
         $jq("#min-button-wrapper").css("display","none");
         $jq("#min-button").attr("src","/static/blog/min.png")

         $jq("#avatar-select-button").html("Load Avatar");
         $jq("#avatar-select-button").attr("class","btn btn-primary btn-sm");
      }else{
         $jq("#avatar-box").css("display","flex");
      }
}

$jq("#avatar-select-button").on('click',function(e){
   e.preventDefault();
   if($jq("#avatar-select").val()!= $jq("#root").attr('data-language') && $jq("#avatar-select").val()!=""){
      $jq("#root").attr('data-language',$jq("#avatar-select").val());
      closeReactApp();
      $jq("#tooltip-avatar").html("Close Avatar");
      $jq("#sidebar-user").css("display","none");
      $jq("#sidebar-avatar").css("display","block");
      $jq("#avatar-mobile").css("display","block");
      if (window.innerWidth <= 768){
         $jq("#min-button-wrapper").css("display","block");
      }
      $jq("#avatar-select-button").html("Close Avatar");
      $jq("#avatar-select-button").attr("class","btn btn-danger btn-sm");
   }else if($jq("#avatar-select").val()== $jq("#root").attr('data-language') && $jq("#avatar-select-button").html()=="Close Avatar" && $jq("#avatar-select").val()!=""){
      $jq("#avatar-box").css("display","none");
      $jq("#root").attr('data-language','');
      $jq("#sidebar-user").css("display","block");
      $jq("#sidebar-avatar").css("display","none");
      $jq("#avatar-mobile").css("display","none");
      $jq("#min-button-wrapper").css("display","none");
      $jq("#tooltip-avatar").html("AI narration video");
      $jq("#min-button").attr("src","/static/blog/min.png")
      closeReactApp();

      $jq("#avatar-select-button").html("Load Avatar");
      $jq("#avatar-select-button").attr("class","btn btn-primary btn-sm");
   }else if($jq("#avatar-select").val()=="" && $jq("#avatar-select-button").html()=="Close Avatar"){
      $jq("#avatar-box").css("display","none");
      $jq("#root").attr('data-language','');
      $jq("#sidebar-user").css("display","block");
      $jq("#sidebar-avatar").css("display","none");
      $jq("#avatar-mobile").css("display","none");
      $jq("#min-button-wrapper").css("display","none");
      $jq("#tooltip-avatar").html("AI narration video");
      $jq("#min-button").attr("src","/static/blog/min.png")

      closeReactApp();
      $jq("#avatar-select-button").html("Load Avatar");
      $jq("#avatar-select-button").attr("class","btn btn-primary btn-sm");
   }
})

$jq("#avatar-select").on('change',function(e){
   e.preventDefault();
   if($jq("#avatar-select").val()!=""){
      $jq("#avatar-select-button").html("Load Avatar");
      $jq("#avatar-select-button").attr("class","btn btn-primary btn-sm");
      $jq("#min-button-wrapper").css("display","none");
   }
})

$jq("#min-button-wrapper").on('click',function(e){
   if($jq("#avatar-mobile").css("display")=="block"){
      $jq("#avatar-mobile").css("display","none");
      $jq("#min-button").attr("src","/static/blog/max.png")
   }else{
      $jq("#avatar-mobile").css("display","block");
      $jq("#min-button").attr("src","/static/blog/min.png")
   }
})

const reactRoot = document.getElementById("root");

function closeReactApp() {
   var language=$jq("#root").attr('data-language');
   console.log(language);
    if (reactRoot) {
      if (window.resetAudio) {
         window.resetAudio(language); 
       }
    }
}

$jq("#play-button").on('click',function(e){
   e.preventDefault();
   var $jq = jQuery.noConflict();
   if(synth.paused){
      synth.resume();
      $jq("#play-button").attr("src","/static/blog/pause.png")
   }else if(synth.speaking){
      synth.pause();
      $jq("#play-button").attr("src","/static/blog/play.png")
   }else{
      get_contents();
      $jq("#play-button").attr("src","/static/blog/pause.png")      
   }

})

function get_contents(){
   var j=$jq('div#content_div p');
   let split=$jq('div#content_div').html().split('\n\n')
   split.forEach(function(item){speak(item.replace(/<[^>]*>/g, ''))})
}

function speak(ok) {
   utterance = new SpeechSynthesisUtterance(ok);
   voices = synth.getVoices();
   utterance.voice = voices[4];
   synth.speak(utterance);
 }