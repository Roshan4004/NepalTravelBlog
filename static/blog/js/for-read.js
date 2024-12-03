
const synth = window.speechSynthesis;

function read(){
      if($(".read-box").css("display")=="flex"){
         $(".read-box").css("display","none");
         synth.cancel()
         $("#play-button").attr("src","/static/blog/play.png")
      }else{
         $(".read-box").css("display","flex");
      }
}


$("#play-button").on('click',function(e){
   e.preventDefault();

   if(synth.paused){
      synth.resume();
      $("#play-button").attr("src","/static/blog/pause.png")
   }else if(synth.speaking){
      synth.pause();
      $("#play-button").attr("src","/static/blog/play.png")
   }else{
      get_contents();
      $("#play-button").attr("src","/static/blog/pause.png")      
   }

})

function get_contents(){
   var j=$('div#content_div p');
   let split=$('div#content_div').html().split('\n\n')
   split.forEach(function(item){speak(item.replace(/<[^>]*>/g, ''))})
}

function speak(ok) {
   utterance = new SpeechSynthesisUtterance(ok);
   voices = synth.getVoices();
   utterance.voice = voices[4];
   synth.speak(utterance);
 }