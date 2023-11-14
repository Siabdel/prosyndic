var eventBus = new Vue()
// instance view de propostion DA simulation

//import SearchBox  from './components/SearchBox.vue'
//-----------------------------
// composant pour gerer config
//-----------------------------
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
}//

var csrftoken = getCookie('csrftoken');

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('DD/MM/YYYY HH:mm')
  }
});

var vm4 = new Vue({
    el : '#app_config',
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
        title : "Paramètrage",
        currentSociete : false,
        currentService : false,
        serviceSelected : "",
        societeSelected : "1",
        showForm : true,
        societes : [],
        services : [],
        message : "",
        error : "",
  		}
  	},

    mounted() {
      //do something after mounting vue instance
      this.societeSelected = $("#id_societe_selected").val()
      this.serviceSelected = $("#id_service_selected").val()
      console.log(" Societe Selected .." +  this.societeSelected)
      this.api_load_societe()
      this.api_load_service()
    },  // fin de mounted

    watch:{
      societeSelected : function() {
        // watching nested property
        //this.societeSelected = $("#id_societe").val();
        console.log(" Societe Selected .." +  this.societeSelected)
        this.api_load_societe()
        },

    }, //fin watch
    // les methodes
    methods: {
      //--------------------------
      // api Reload tickets
      //--------------------------
      load_service(){
        // remplir data
        console.log("api_load_service de societe" + this.societeSelected)
        // envoie de l'api
        this.api_load_service()
      },
      //--------------------------
      // api Reload les societes
      //--------------------------
      api_load_societe(){
          //passer status a ENCOURS et updater la tache ..
          var url = `/pro/api/get_societes.json`
          //var cle_csrf = $( "input[name='csrfmiddlewaretoken']" ).val()
          console.log("api_load_societe .." + url)
          //
          fetch(url)
           .then(response => response.json())
           .then( json => { this.societes = json },
             //console.log("api retour currentSociete= " + this.currentSociete )
           ).catch((err)=>console.log(err))

          }, //api_load_societe
    //--------------------------
    // api Reload tickets
    //--------------------------
    api_load_service(){
      //passer status a ENCOURS et updater la tache ..
      var url = `/pro/api/get_services/${this.societeSelected}.json`
      //var cle_csrf = $( "input[name='csrfmiddlewaretoken']" ).val()
      console.log("api_load_service .." + url)
      //
      fetch(url)
       .then(response => response.json())
       .then( json => { this.services = json },
         //console.log("api retour currentSociete= " + this.currentSociete )
       ).catch((err)=>console.log(err))

      }, //api_load_service
  },

  })
