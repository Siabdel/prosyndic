var eventBus = new Vue()

// composant pour gerer l'ecran de recherche utilisateurs
var compo_member = {
  // OUT : render template
  template : "#members_template",
	// data IN
	delimiters: ['[[', ']]'],
	props :  {
		key_search :  "",
		invites : [],
    project_id : false,
	},

	data () {
		return {
      message : "ICI composant_member",
      cle : "",
      members : [],
      members_selected : [],
      users_dispo : [],
      currentSort : 'user',
			currentSortDir : 'asc',
      pageSize : 4,
	 		currentPage : 1,
      sortBy : "user",
      filterBy : "",
			pageSize : 4,
      member_delete : false,
      checked : false,
      active : false,
      showModal : false,
      form_active : true,
      key : this.index ,
			csrfmiddlewaretoken : "",
			url_delete_user : `/da/cac/delete_user/`  ,
      url_all_user : `/pro/api/members.json/`,
      ConfirmeDeleteUser : this.emitConfirmeDeleteUser,
			}
	},

  created : function() {
    this.members_disponible()
    //console.log( " tout les members = ",  this.members.length )
  }, // fin de created

  mounted() {
    //do something after mounting vue instance
    eventBus.$on('del-member',  ( ) => {
      console.log("je recoie bien le signale 'del-member'  " )
      this.members_disponible()
      //
     })
  },

  computed:{

    sortedCats:function() {
        return this.dict_ofs.sort((a,b) => {
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
    },

    SortedMembersDispo() {
      if (this.users_dispo.length > 0) {
        //console.log( "SortedMembersDispo len = ", this.users_dispo.length )
        return this.users_dispo.filter( member  => member.user.includes(this.filterBy))
          .sort( (a, b) => a[this.sortBy].localeCompare(b[this.sortBy]))
          .filter((row, index) => {
            var start = (this.currentPage-1)*this.pageSize
            var end = this.currentPage*this.pageSize
            if(index >= start && index < end) return true
            return false
        });
      }

    }
  }, // fin de computed

	methods : {
    sortedMembers() {
      return this.members.sort((a,b) => {
        let modifier = 1
        if(this.currentSortDir === 'desc') modifier = -1
        if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier
        if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier
        return 0
      }).filter((row, index) => {
        var start = (this.currentPage-1)*this.pageSize
        var end = this.currentPage*this.pageSize
        if(index >= start && index < end) return true
        console.log( "sort by  ",  a  )
        return false
    })
    },
    // tri
    sort:function(elem) {
      //if s == current sort, reverse
      if(elem === this.currentSort) {
       this.currentSortDir = this.currentSortDir==='asc'?'desc':'asc'
      }
      this.currentSort = elem
    },
    // paginator
    nextPage:function() {

      if((this.currentPage*this.pageSize) < this.members.length) this.currentPage++
      console.log( "next page  = ", this.currentPage++ )
    },
    prevPage:function() {
      if(this.currentPage > 1) this.currentPage--
    },
  // fonction check : Selection des membres
   selectMember( checked, pk, index){
     //console.log("check = " + checked +  "elem", pk)
     if(checked){

       if ( this.members_selected.indexOf(pk) == -1 ){
          this.members_selected.push(pk)
       }

     }else {
       var ind = this.members_selected.indexOf(pk)
       this.members_selected.splice( ind, pk)
       console.log("delete = " + pk +  " index=", ind)
       //Vue.delete(this.items, index);
     }
     //console.log("check = ", this.members_selected)
   },

   // Ajout des members
   api_add_members(event){
     var url = `/pro/api/add_members/`
     var cle_csrf = $( "input[name='csrfmiddlewaretoken']" ).val()

     data_project = {
       'project' : project_id,
       'members' : this.members_selected,
       'csrfmiddlewaretoken' : cle_csrf ,
     }
     //
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
     body : js_data

     })
     .then(response => response.json())
     .then(json=>{eventBus.$emit('add-member', project_id)})
     .then( function (response) {
          //location.replace("/da/cac/list/")
          $(event.target).toggleClass("btn-warning");
          console.log("fetch add members !!" + response );
          // emeteur
          eventBus.$emit('add-member', project_id);
          this.members_selected = [];
     }).catch((err)=>console.log( err))
   },

   //
   members_disponible(){
      this.api_members_project(event)
    },

    // tout les memebrs dispo
    api_members_project(){
      var url = `/pro/api/users_dispo/${project_id}.json`

      fetch(url)
        .then(response =>  response )
        .then( result    => {
          this.users_dispo = result.json();
          console.log( "api_members_project  = ", this.users_dispo );
        })
        .catch((err)=>console.log(err))
    },


    // tout les utilisateurs
    api_all_members(event){
      var url = `/pro/api/members.json/`
      fetch(url)
        .then( reponse => reponse )
        .then( result  => { this.members = result.json() },)
         //console.log( "api_all_members = ", this.members.length) )
        .catch((err)=>console.log(err))
    },

    // les members qui correspondent a la cle de reherche
    api_filter_members(search_key){
      //pro/api/member/ab.json
      var url = `/pro/api/member/${search_key}.json`
      //var url = `/pro/api/member/ab.json`

      fetch(url).then( reponse => reponse.json() )
       .then( result => {
          this.users_dispo = result
          console.log("api_filter_members = " + url);
       })
       .catch((err)=>console.log(err))
    },

  }
}


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
    el: '#app_edit',
    delimiters: ['[[', ']]'],
    components : {
  		compomember : compo_member ,
  	},

    data : {
      message : "Ici vm2 ...",
      show_desc: true,
      errors : [],
      project_id : false,
      users_disponible : [],
      members_project : [],
      sortBy: "user",
      isActive : true,
      show_list : true,
      transition_select: 'fade',
      showModal: false,
      showAddMember:false,
      showDelMember:true,
    },  //

    created() {
      //do something after creating vue instance
      if(project_id){
        this.api_members_project(event, self.project_id)
      }
    },

    mounted() {
      //do something after mounting vue instance
      eventBus.$on('add-member',  () => {
        console.log("je recoie bien le signale 'add-member'  " )
        this.api_members_project(event, self.project_id)
       })
    },

    computed:{
       //
       members_project_refresh : function(){
         //this.api_members_project(event, self.project_id)
         return this.members_project
       }
    },

    methods:{
      // tout les utilisateurs
      api_members_project(event, project_id){
        var url = `/pro/api/member/list/${project_id}.json`

        fetch(url, {
          method  :  "GET",
          headers : {
                  'Content-Type': 'application/json',
                  'Accept': 'application/json'
                }
        })
        .then(response =>  response.json() )
        .then( result => {
          this.members_project = result ;
          console.log("api_members_project ... = " + url )
        })
        .catch((err)=>console.log(err))

      },

      delete_member(project_id, member_id){
        //
        var url = `/pro/api/delete_member/${project_id}/${member_id}`
        var cle_csrf = $( "input[name='csrfmiddlewaretoken']" ).val()

        console.log("project id= " + project_id)

        fetch(url,
          {
            method  :  "DELETE",
            headers : {
            //'Content-Type': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'X-CSRFToken': cle_csrf,
            }
          }
        ).then( reponse => reponse)
          .then( json    =>  {
              this.message=json;
              eventBus.$emit('del-member');
              this.api_members_project(event, self.project_id);
          })
          .catch((err)=>console.log(err))
        },// fin delete_member

      },

    })
