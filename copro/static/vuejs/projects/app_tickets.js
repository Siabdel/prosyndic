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


Vue.component('cpn_toggle_image', {
    props: {
      admin: {
        type: Boolean,
        required: true
      }
    },
    template: `
        <div class="profil-image">
          <img :src="image" />
        </div>
        <div class="color-box"
              v-for="(variant, index) in variants"
              :key="variant.variantId"
              :style="{ backgroundColor: variant.variantColor }"
              @mouseover="updateProduct(index)"
              >
         </div>
      `,

      data() {
         return {
             brand: 'Vue photo',
             selectedVariant: 0,
             image : '/static/images/avatar.jpg',

             variants: [
               {
                 variantId: 2234,
                 variantColor: 'green',
                 variantImage: '/static/images/avatar.jpg',
               },
               {
                 variantId: 2235,
                 variantColor: 'blue',
                 variantImage: '/static/images/photo.jpg'
               }
             ],
         }
       },

     methods: {
       updateProduct(index) {
           this.image = this.variants[index].variantImage
       } ,
     }
})

var ComponenTickets = {
  // OUT : render template
  template : "#tickets_admin_template",
	// data IN
	delimiters: ['[[', ']]'],
	props :  {
		key_search :  "",
    project_id : {
      required : false
    },
    current_user_id : {
      required : false
    }
	},

	data () {
		return {
      titre : "ICI composant actions du projet",
      donnees : [],
      message : "",
      currentComment : "",
      showComment : false,
      cle : "",
      title : "",
      currentTask : Object,
      currentTaskId :  Number,
      currentUser  :  Object,
      currentUserId : Number,
      currentSort : 'title',
			currentSortDir : 'asc',
      pageSize : 25,
	 		currentPage : 1,
      sortBy : "title",
      filterBy : "a",
      ticket_delete : false,
      checked : false,
      active : false,
      visibility : true,
      showModal : false,
      url_project : `/pro/`,
      url_delete_ticket : `/pro/`,

			}
	},


  mounted() {
    // charger utilisateur
    this.currentUserId = this.current_user_id
    // load data
    this.api_reload_tickets(event)
    this.api_get_user_profile(event)
    //console.log("currentUser = " +  this.current_user_id)
  },

  computed:{

    sortedTickets() {
      if (this.donnees.length > 0) {
        //console.log( "SortedTicketsSortBy = ", this.sortBy )
        return this.donnees.filter( ticket  => ticket.title.includes(this.filterBy))
          .sort( (a, b) => {
            a[this.sortBy].localeCompare(b[this.sortBy])
            let modifier = 1
  	        if(this.currentSortDir === 'desc') modifier = -1
  	        if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
  	        if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
  	        return 0

          }).filter((row, index) => {
  	        var start = (this.currentPage-1)*this.pageSize
  	        var end = this.currentPage*this.pageSize
  	        if(index >= start && index < end) return true
  					return false
        })
      }
    },
    // --
    sortedTickets2() {

      if (this.donnees.length > 0) {

        return this.donnees.sort((a,b) => {
	        let modifier = 1
	        if(this.currentSortDir === 'desc') modifier = -1
	        if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier
	        if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier
	        return 0
	      }).filter((row, index) => {
	        var start = (this.currentPage-1)*this.pageSize
	        var end = this.currentPage*this.pageSize
	        if(index >= start && index < end) return true
					return false
      })
     }
    },

    // changement status on live asynchrone

  }, // fin de computed

  // les methodes
  methods: {
    //--------------------------
    // api Reload tickets
    //--------------------------
    api_reload_tickets(event){
      if(this.project_id){
        var url = `/pro/api/tickets/${this.project_id}.json/`
        console.log("api pour projet  = " + url)
        //this.project_id = `${project_id}`
        // on charge les tickets du user
        fetch(url)
         .then(response => response.json())
         .then( json => { this.donnees = json},
           console.log("api retour pour projet = " + this.project_id )
         ).catch((err)=>console.log(err))

      } else if (this.current_user_id) {
        var url = `/pro/api/mestickets/${this.current_user_id}.json/`
        console.log("api pour user sage  = " + url)

        //this.project_id = `${project_id}`
        // on charge les tickets du user
        fetch(url)
         .then(response => response.json())
         .then( json => { this.donnees = json},
           console.log("api retour pour projet = " + this.project_id )
         ).catch((err)=>console.log(err))
      }

    },
    //--------------------------
    // Autorizations
    //--------------------------

    is_currentuser_assignee(task){
      if ((task.assignee ) && (task.assignee.id == this.currentUser.user.id) ){
        return true
      }
    },

    user_permissions_task(task){
      //
      Autorizations_admin   = (this.currentUser.user.is_superuser | (this.currentUser.user.is_staff) )
      Autorizations_manager = task.is_manager

      return ( (Autorizations_admin ) |  ( Autorizations_manager ) )
    },



    url_ticket_edit(ticket_id){
      // modifier le ticket
      var url = `/pro/projects/tickets/${ticket_id}/`
      return url
    },

    // -------------------
    // url ticket show
    // -------------------
    url_ticket_show(ticket_id){
      // modifier le ticket
      var url = `/pro/projects/tickets/${ticket_id}/edit/`
      return url
    },

    // -------------------
    // accepter la tache
    // -------------------
    accepter_tache(e){
      //terminer la tache et saisir le commentaire
      console.log("accpter la tache .." + this.currentTask)
      this.currentComment = ""
      //location.replace()
      this.api_update_tache("ENCOURS")
      return true
    },

    // -------------------
    // terminer la tache
    // -------------------
    terminer_tache(e){
      //terminer la tache et saisir le commentaire
      console.log("termner la tache .." + this.currentTask)
      this.api_update_tache("RESOLUE")
      this.showComment = false
      // mise a blanc du commentaire
      this.currentComment = ""
      return true
    },

    // -------------------
    // annuler tache
    // -------------------
    annuler_tache(e){
      //terminer la tache et saisir le commentaire
      console.log("REFUSEE la tache .." + this.currentTask.id)
      this.api_update_tache("REFUSEE")
      this.showComment = false
      // mise a blanc du commentaire
      this.currentComment = ""
      return true
    },

    // -------------------
    // cloture tache
    // -------------------
    cloturer_tache(e){
      //terminer la tache et saisir le commentaire
      console.log("Cloturer la tache .." + this.currentTask)
      // mise a blanc du commentaire
      this.currentComment = ""
      this.showComment = false
      // update
      this.api_update_tache("CLOTUREE")

      return true
    },

    // -------------------
    // mise pause tache
    // -------------------
    mise_pause_tache(e){
      //terminer la tache et saisir le commentaire
      console.log("mise pause tache .." + this.currentTask.id)
      this.api_update_tache("ENATTENTE")
      this.showComment = false
      // mise a blanc du commentaire
      this.currentComment = ""
      return true
    },

    // -------------------
    // ajouter commentaire
    // -------------------
    ajouter_comment(e){
      //
      //terminer la tache et saisir le commentaire
      console.log("Ajouter un commentaire .." + this.currentTask)
      // mise a blanc du commentaire

      this.api_update_tache("ENCOURS")
      // mise a blanc du commentaire
      this.currentComment = ""
      //update
      this.showComment = false

      return true
    },

    // -------------------
    // mettre a jour la tache
    // -------------------
    api_update_tache(action){
      //passer status a ENCOURS et updater la tache ..
      var url = `/pro/api/update_ticket/${this.currentTask.id}`
      // var cle_csrf = $( "input[name='csrfmiddlewaretoken']" ).val()

      console.log("majla tache .." + this.currentTask)
      // before
      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      });

      var data_ticket = {
        'task_id' : this.currentTask.id,
        'comment' : this.currentComment,
        'action' : action,
        //'csrfmiddlewaretoken' : cle_csrf ,
        "X-CSRF-Token":"Fetch"

        }
      //
      fetch(url, {
        method: "put",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json"
              },
              body: JSON.stringify( data_ticket)
          }).then(function(response) {
              return response.json();
          }).then(function(data) {
              console.log("Data is ok", data);
              // refresh
          }).catch(function(ex) {
              console.log("parsing failed", ex);
        })
      } ,

    emit_open_modal_confirm(e){
      // popup de confirmation
      return true
    },

    api_delete_tache(elem, task){
      //emit_open_modal_confirm(task.pk)
      //var target = elem.$parent.css({"color": "red", "back-ground": "red"});

      var target = elem.$parent
      var url = `/pro/api/ticket/${task.id}/delete/`
      var CSRF_TOKEN =  getCookie("csrftoken")
      console.log("Supprimer la tache " + url )
      // fetch
      fetch(url,
        {
         method: 'delete',
         credentials: "same-origin",
         headers : {
             "X-CSRFToken": CSRF_TOKEN,
           }
        }).then( function (response) {
          // redirect project show
          //location.href = "/da/cac/list/"
          var url_details = `/pro/projects/${task.project.id}/`
          location.replace(url_details)
          //hide
          //$(elem).parent().parent().hide() ;
   				return  response
        }) .catch(error => { console.log(error)})

      return true
    },

    //--------------------------
    // api get user profile
    //--------------------------
    api_get_user_profile(event){
      var url = `/pro/api/puser/${this.currentUserId}.json/`
      //this.project_id = `${project_id}`
      // on charge les tickets du user
      if (this.currentUserId == null){
          console.log("attention this.currentUserId est null !! ")
          return null
      }
      fetch(url)
       .then(response => response.json())
       .then( json => { this.currentUser = json},
         console.log("api_get_user_profile current User = " + url)
       ).catch((err)=>console.log(err))
    },

    // sort
    // tri
    sort:function(elem) {
      console.log("sort by me !!" + elem )
      //if s == current sort, reverse
      if(elem === this.currentSort) {
       this.currentSortDir = this.currentSortDir==='asc'?'desc':'asc'
      }
      this.currentSort = elem
    },
    // paginator
    nextPage() {
      if((this.currentPage*this.pageSize) < this.donnees.length) this.currentPage++
      console.log( "next page  = ", this.currentPage++ )
    },

    prevPage() {
      if(this.currentPage > 1) this.currentPage--
    },

    // les tickets qui correspondent a la cle de reherche
    api_filter_tickets(search_key){
      //pro/api/member/ab.json
      var url = `/pro/api/ticket/${search_key}.json`

      fetch(url)
        .then( reponse => reponse.json() )
        .then( result => {
          this.donnees = result
          //console.log("api_filter_tickets = " + url)
        })
        .catch((err)=>console.log(err))
    },

    setFocusComment: function()
    {
      //focus to input
      console.log("focus sur ecran de commentaire !" + this.$refs.zcomment.name)
      this.$refs.zcomment.focus();
    }
  },
}// fin de comppsant ticket

//--------------------------
// register modal component
//--------------------------

Vue.component('modal', {
  template: '#modal-template',
  methods: {
     emitValidationDa(id) {
          console.info("validation emit  **" + id)
          //eventBus.$emit("validation", id)
          this.valider_ligne_user(id)
      },

      // API valider_ligne_user
      valider_ligne_user(da_id){
          // envoie de la validation
          var url = `/da/cart/validateda/${da_id}/`
          fetch(url).then(
           function (response) {
              console.log("valider_ligne_user excuter !!" + response)
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
    return moment(String(value)).format('dd DD/MM/YYYY HH:mm')
  }
});

Vue.filter('reverse', function (value) {
  return value.split('').reverse().join('')
})

Vue.filter('substr', function (value, pos) {
  if(value){
      return value.slice(0, pos)
  }
  return false
})

var vm2 = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    components : {
      compo_task_admin : ComponenTickets,
    },

    data : {
      message : "***  ici App project details  !!! ***",
      project_id : "",
      user_online : Object,
      errors: [],
      toggle:true,
      selected : "",
      isActive : true,
      show_create : false,
      show_list : true,
      transition_select: 'fade',
      showModal: false,
    },  //

    ///
    mounted() {
      //do something after mounting vue instance
      // var url = `/api/projects/${project_id}/etapes`
    },

    ///
    computed: {
        // un accesseur (getter) calculé
        reloadTicket: function () {
          // `this` pointe sur l'instance vm
          return this.tasks
        }
      },

      methods: {

        // ---
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
          js_userta = JSON.stringify(data_project) // on

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
