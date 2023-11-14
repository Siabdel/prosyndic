// import UserTasks from './UserTasks.vue'
//import UserTaskParser from './UserTaskParser'

var EasyGantt = {
  // OUT : render template
  template : "#id_tmplate_gantt",
	// data IN
	delimiters: ['[[', ']]'],

  components: {
    //UserTasks
  },

  data () {
    return {
      dates : [],
      isLoading: false
    }
  },

  props: {
    utasks: {
      type: Array,
      default: []
    },

    sdate: Object,

    spinner: {
      type: String,
      default: 'default'
    }
  },

  computed: {

    egtasks() {
      let items = []
      this.utasks.forEach((obj, idx) => {
        //let utp = new UserTaskParser(obj.tasks, this.sdate)
        let utp = {}
        let data = {}
        data.user = obj
        data.tasks = utp.items
        data.total = utp.total
        this.dates = utp.dates
        items.push(data)
      })
      return items
    }

  },

  created () {
    this.isLoading = true
    console.log("is loading ...!" + this.utasks)
  },

  updated () {
    this.isLoading = false
    console.log("is updated  ...!" + this.utasks[0].start)
  }
}
