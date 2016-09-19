function getCookie(name) {
       var cookieValue = null;
       if (document.cookie && document.cookie != '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
         var cookie = jQuery.trim(cookies[i]);
         // Does this cookie string begin with the name we want?
         if (cookie.substring(0, name.length + 1) == (name + '=')) {
             cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
             break;
          }
     }
 }
 return cookieValue;
}

$("#submit").click(function(e) {

 e.preventDefault();

 var csrftoken = getCookie('csrftoken');

 var query = $('#inputQuery').val();
 var inpObj = document.getElementById("inputQuery");
 document.getElementById("query-output").innerHTML = "";
 

 $.ajax({
         url : "http://127.0.0.1:8000/get_search/", // the endpoint,commonly same url
         type : "GET", // http method
         data : { csrfmiddlewaretoken : csrftoken, 
         query : query
 }, // data sent with the post request

 // handle a successful response
 success : function(json) {
    console.log('Query data submitted: ', json); // another sanity check
      //On success show the data posted to server as a message
 },

 // handle a non-successful response
 error : function(xhr,errmsg,err) {
 console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
 }
 });
 $( '#query').each(function(){
    this.reset();
});
});