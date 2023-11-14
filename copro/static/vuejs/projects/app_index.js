var eventBus = new Vue()
// instance view de propostion DA simulation

//import SearchBox  from './components/SearchBox.vue'
//--------------------------
// composant pour gerer  mes tickets
//--------------------------
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

var csrftoken = getCookie('csrftoken');


Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('DD/MM/YYYY HH:mm')
  }
});

var vm3 = new Vue({
    el : '#app_contacte',
    delimiters: ['[[', ']]'],
    // OUT : render template
  	// data IN
    props : {
      currentUser : "",
      currentUserId : {
        required : false
      },
    },

    data () {
  		return {
        titre : "Nous Contactez",
        isSaved : false,
        message : "",
        error : "",
        showForm : true,
        contacte : {
          nom : "",
          email : "",
          message : "",
          is_connect : false
        },
  		}
  	},

    mounted() {
      //do something after mounting vue instance
      if(username != "" ) {
        this.contacte.nom = username
        this.contacte.email = email
      }
      this.isSaved = false
    },  // fin de mounted

    // les methodes
    methods: {
      //--------------------------
      // api Reload tickets
      //--------------------------
      mise_a_blanc(){
        this.contacte.nom = ""
        this.contacte.email = ""
        this.contacte.message = ""
      },


      create_ticket(){
        // remplir data
        var data = {
          'user_id' : this.currentUserId,
          'nom' : this.contacte.nom,
          'email' : this.contacte.email,
          'message' : this.contacte.message,
          //'csrfmiddlewaretoken' : cle_csrf ,
          "X-CSRF-Token":"Fetch"
          }
        if(this.contacte.nom == "" ) {
          this.error = " veuillez saisir votre Nom !"
          this.contacte.nom = username
          return false
        } else if(this.contacte.email == ""){
          this.error = " veuillez saisir votre Email !"
          return false
        } else if (this.contacte.message == ""){
          this.error = " veuillez saisir votre Message !" + this.contacte.message
          return false
        }
        //
        console.log("api_create_ticket .." + data)
        // envoie de l'api
        this.api_create_ticket(data)
        this.mise_a_blanc()
        this.showForm = false
        this.isSaved = true
        //--
        this.message = "Merci Votre message est bien pris en compte ! "

      },

      //--------------------------
      // api Reload tickets
      //--------------------------
      api_create_ticket(data_contacte){
        //passer status a ENCOURS et updater la tache ..
        var url = `/pro/api/add_ticket_contacte/`
        //var cle_csrf = $( "input[name='csrfmiddlewaretoken']" ).val()

        console.log("api_create_ticket .." + url)
        //
        fetch(url, {
          method: "put",
          credentials: "same-origin",
          headers: {
              "X-CSRFToken": getCookie("csrftoken"),
              "Accept": "application/json",
              "Content-Type": "application/json"
                },
                body: JSON.stringify(data_contacte)
            }).then(function(response) {
                return response.json();
            }).then(function(data) {
                this.message = "Votre message est bien pris en compte ! "
                this.error = ""
                console.log("Data is ok", this.message);

                // refresh
            }).catch(function(ex) {
                console.log("parsing failed", ex);
          })
        }, //api_create_ticket
    },

  })
