// Post like function
function likefunction(){
    {% if request.user.is_authenticated %}
    $jq.ajax({
        type : "GET", 
        url: "{% url 'blogdetail' post.id %}",
        data: {
        form: "likefunction",
        },           
        success: function(data){
        let num_of_likes = data.new_number_of_likes == "" ? "" : data.new_number_of_likes[0];
        
        if (data.color != "red") {
            $jq('#number_of_likes').html(" "+num_of_likes);   
            $jq('#like_icon').removeClass('fas').addClass('far');
            $jq('.like-button').removeClass('text-red-500').addClass('hover:text-red-500');
            
        } else {  
            $jq('#number_of_likes').html(" "+num_of_likes); 
            $jq('#like_icon').removeClass('far').addClass('fas');
            $jq('.like-button').removeClass('hover:text-red-500').addClass('text-red-500');

        }
        },   
        error: function() {
        console.log("Error occurred");
        }
    });
    {% else %}
    showToast("You have to login to like a post..", 'error');
    {% endif %}
}