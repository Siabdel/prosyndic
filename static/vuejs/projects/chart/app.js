//------------------------------------
// composant pour gerer  mes tickets
//------------------------------------
// Bus
var eventBus = new Vue()
// getCookie
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

// composant rapport
var project_report_cpn = {
  // OUT : render template
  delimiters: ['[[', ']]'],
  template : "#rapport_template",

	// data IN
	props :  {
		project_id : Number,
	},
  components: {
    //
  },


	data () {
		return {
			//ofs : Array,
      titre : "Rapport project",
			checked : true,
			data_stat : Object,
      employees:  Object,
      taux_realisation : 0,
			}
	},
	// Fetches posts when the component is created.

  created() {
    //do something after creating vue instance
    ///var url = `/pro/api/tickets/${this.project_id}.json/`
  },

  mounted() {
    var url_project = `/pro/api/get_project_ticket_stat/${this.project_id}`
    var url_staff = `/pro/api/get_staff/`
    this.loadDataChart(url_project)
    console.log("mounted data = " + this.data_in )
    this.loadDataStaff(url_staff)
  },

  methods: {
    //do something after creating vue instance
    loadDataChart(url){
      ///var url = `/pro/api/get_project_ticket_stat/${this.project_id}`
      // this.project_id = `${project_id}`
      fetch(url)
        .then(response =>  response.json() )
        .then(data => { this.data_stat = data })
         .catch(error => console.log("erreur==" + error))
    },// fin loadDataChart

    // Staff
    loadDataStaff(url){
      //--
      fetch(url)
        .then(response  => response.json()  )
        .then(response => {
          //this.employees = JSON.parse('{ "status" : 10 }'),
          this.employees = response.data
          console.log("loadDataStaff = " + this.employees)
         })
        .catch(error => console.log("erreur==" + error))
    }// fin loadDataStaff
	},
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
       project_report_cpn : project_report_cpn,
    },

    data(){
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

    mounted() {
    },

    methods: {
      //--------------------------
    },//fin methods
  })// fin vm3
