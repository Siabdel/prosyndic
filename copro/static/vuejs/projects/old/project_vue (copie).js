var eventBus = new Vue()

// register modal component
Vue.component('modal', {
  template: '#modal-template',
  methods: {
     emitValidationDa(id) {
          console.info("validation emit  **" + id)
          //eventBus.$emit("validation", id)
          this.valider_ligne_da(id)
      },

      // API valider_ligne_da
      valider_ligne_da(da_id){
          // envoie de la validation
          var url = `/da/cart/validateda/${da_id}/`
          fetch(url).then(
           function (response) {
              console.log("valider_ligne_da excuter !!" + response)
              // redirect
              //location.href = "/da/cac/list/"
              location.replace("/da/cac/list/")
              return  response
          }).catch((err)=>console.error(err))

       },
    },

})

Vue.filter('arrondi', function (value, number) {
  return parseFloat(value.toFixed(number))
})

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('DD/MM/YYYY HH:mm')
  }
});

// instance view de propostion DA simulation
var vm2 = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data : {
      message : "***  ici etapes !!! ***",
      search: "",
      ticket : {
        project : "",
        sequence : 101,
        status : 1,
        project : "",
        title : "",
        description : "",
        author : 1,
        created_by : 1,
        categories : 1,

      },
      errors : [],
      tasks :  Object,
      isActive : true,
      show_create : false,
      show_list : true,
      transition_select: 'fade',
      showModal: false,
    },  //

    mounted() {
      //do something after mounting vue instance
      // var url = `/api/projects/${project_id}/etapes`
      var url = `/pro/api/projects/${project_id}/etapes/`
      this.ticket.project = `${project_id}`
      console.log("mounted projet = " + this.ticket.project )

      fetch(url).then(
    	 function (response) {
    		   return  response.json()
    		   console.log("api on charge les etapes !!")
    		 }
       ) .then( json => { this.tasks = json},
    	   console.log("api retour pour projet = " + this.tasks )
       )
       .catch((err)=>console.log(err))
        },


      methods: {
        // toper article selectionner
        add_etape_project(event, project_id) {
          //var url = `/pro/api/add_etape_project/${project_id}`
          if (! this.checkTicketForm()) {
            return false
          }
          var url = `/pro/api/tickets/`

          var cle_csrf = $( "input[name='csrfmiddlewaretoken']" ).val()

          data_project = {
            'project' : project_id,
            'sequence' : this.code,
            'title' : this.title,
            'description' : this.description,
            'author' : this.author,
            'assignee' : this.assignee,
            'csrfmiddlewaretoken' : cle_csrf ,
          }
          form = $( "#form_task" ).serialize()
          ///QueryDict: {u'comment': [u'ZZZZZZZZZZZZZ'], u'csrfmiddlewaretoken': [u'DMbU0yI7I9lVACrt7agLPHu9bzkMoektWe7sd1N85rVvfbRk60rNEJZ10ntNESoF']}
          js_data = JSON.stringify(data_project) // on

        fetch(url,
          {
          method : 'POST',
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            'Accept': 'application/json',
            'X-CSRFToken': cle_csrf,

          },
          //body : JSON.stringify({'comment' : 'wwwwwwwwwwwww' }),
          body : form,


      		}).then(response => console.log(response))
            .then( function (response) {
               console.log("add commentaire project_id=%s ..." % js_data)
               // redirect
               //location.replace("/da/cac/list/")
               $(event.target).toggleClass("btn-warning")
               return  response
          }).catch((err)=>console.log( err))

          console.log("apres fetch add_etape_project !!" + cle_csrf)

        },

        // validation form
        checkTicketForm: function (e) {
          console.log("check ticket   " + this.ticket.title  + this.sequence)

          if (this.ticket.title && this.ticket.sequence) {
            console.log("check ticket form  ok " + e)
            return true;
          }

          this.errors = [];

          if (!this.ticket.title) {
            this.errors.push('saisie titre obligatoire.');
          }
          if (!this.ticket.sequence) {
            this.errors.push('sequence requise.');
          }
          //e.preventDefault();
          }


          },
    })
