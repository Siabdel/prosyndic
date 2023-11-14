// instance view  chart Gantt
// import EasyGantt from '../components/EasyGantt.js'
//------------------------------------
// composant pour gerer  mes tickets
//------------------------------------
// Bus
var eventBus = new Vue()

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


var composant_stat = {
	// data IN
	props :  {
		project_id : Number,
	},

	data () {

		return {
			//ofs : Array,
			checked : true,
			data_in = Object,
			}
	},
	// Fetches posts when the component is created.
  created() {
      loadData(),
  },

  methods: {
      loadData() {
        ///var url = `/pro/api/tickets/${this.project_id}.json/`
        var api_url = `/pro/api/get_mesticket_stat/`;

        // this.project_id = `${project_id}`
        fetch(url)
         .then(response => response.json())
         .then( json => {
           this.data_in = json
         }
         )
      },
	},
 // OUT : render template

template : "#stat_template"

};



var csrftoken = getCookie('csrftoken');

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('DD HH:mm')
  }
});

var vm3 = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    components: {
       statProject : composant_stat,
    },

    data () {
      return {
        message : "***  ici App Gantt  !!! ***",
        sdate: null,
        utasks: [],
        project_id : 41,
        task: {
          'currentUserId' : '',
          'currentTacheId' : '',
          'startDate' : '',
          'endDate'  : '',
        }
      }
    },

    components : {
      easy_gantt : EasyGantt ,
    },

    mounted () {
      this.loadData()
      console.log("data tasks ...count" + this.utasks.length)
    },

    methods: {
      loadData() {
        ///var url = `/pro/api/tickets/${this.project_id}.json/`
        var url = `/pro/api/projectevents/${this.project_id}.json/`
        // this.project_id = `${project_id}`
        fetch(url)
         .then(response => response.json())
         .then( json => {
           this.utasks  = json
           this.sdate   = json
         }
         )
      },
      // update lignes task Gantt
      //--------------------------
      // api Reload tickets
      //--------------------------

      move_ticket(){
        // remplir data
        var data_task = {
          'user_id' : this.task.currentUserId,
          'task_id' : this.task.currentTacheId,
          'start' :   this.task.startDate,
          'end' : this.task.endDate,
          //'csrfmiddlewaretoken' : cle_csrf ,
          "X-CSRF-Token":"Fetch"
          }
        // url updater la tache ..
        var url = `/pro/api/api/move_ticket/${this.task.currentTacheId}`
        //var cle_csrf = $( "input[name='csrfmiddlewaretoken']" ).val()

        console.log("api/move_ticket/ .." + url)
        //
        fetch(url, {
          method: "put",
          credentials: "same-origin",
          headers: {
              "X-CSRFToken": getCookie("csrftoken"),
              "Accept": "application/json",
              "Content-Type": "application/json"
                },
                body: JSON.stringify(data_task)
            }).then(function(response) {
                return response.json();
            }).then(function(data) {
                this.message = "Votre message est bien pris en compte ! "
                this.error = ""
                console.log("Data is ok", this.message);
                // refresh
            }).catch(function(ex) {
                console.log("update task failed", ex);
          })
        }, //api_create_ticket
    },
    }

  })// fin vm3
