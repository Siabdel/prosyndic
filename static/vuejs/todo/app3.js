// Full spec-compliant TodoMVC with localStorage persistence
// and hash-based routing in ~150 lines.
var eventBus = new Vue()
//traitement de cookies pour reuperer la cle CSRF_TOKEN
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

var todos = []
// visibility filters
var filters = {

  all(todos) {
    return todos
  },

  active(todos) {
    return todos.filter(function (todo) {
      return !todo.completed
    })
  },

  completed(todos) {
    return todos.filter(function (todo) {
      return todo.completed
    })
  }
}

// composant pour gerer l'ecran de recherche utilisateurs

var component_vtodo = {
  delimiters: ['[[', ']]'],
  // OUT : render template
  template : "#vtodo_template",
  // data IN
  //props
  props :  {
    user_id : {
      required : false
    },
  },
  //data
  data () {
  	return {
        todos: Array,
        newTodo: '',
        editedTodo: null,
        visibility: 'all',
      }
  },

  mounted() {
        //do something after mounting vue instance
        //do something after mounting vue instance
        var url = `/pro/api/vtodo/${this.user_id}.json/`
        console.log("url= " +  url )

        fetch(url)
          .then(response => response.json())
          .then(data => this.todos = data )
          .catch(error => { console.log(error)})
          ///
          console.log("mounted! " +   this.todos.length)
      },

  // watch todos change for localStorage persistence
  watch: {
    todos: {
      handler: function (todos) {
        //todoStorage.save(todos)
        //this.save_todo()
      },
      deep: true
    }
  },

  // computed properties
  // https://vuejs.org/guide/computed.html
  computed: {

    filteredTodos() {
      return filters[this.visibility](this.todos)
    },

    remaining() {
      return todos.filter(function (todo) {
        return !todo.completed
      })
      //return filters.active(this.todos).length
    },

    allDone: {
      get: function () {
        return this.remaining === 0
      },
      set: function (value) {
        this.todos.forEach(function (todo) {
          todo.completed = value
        })
      }
    }
  },

  filters: {
    pluralize: function (n) {
      return n === 1 ? 'item' : 'items'
    }
  },

  // methods that implement data logic.
  // note there's no DOM manipulation here at all.
  methods: {
    save_todo(){
      // someting
      let url = `/pro/api/vtodo/create/`
      // chercher la cle de securité
      let CLE_CSRF = $("input[name='csrfmiddlewaretoken']" ).attr('value')
      CLE_CSRF = CLE_CSRF.trim()

      console.log("CLE_CSRF = " +  CLE_CSRF)

      let data_todo = {
        //'csrfmiddlewaretoken' : CLE_CSRF,
        'author' : this.user_id,
        'title' : this.newTodo.trim(),
         //"X-CSRF-Token": "Fetch",
      }
      //console.log("CLE_CSRF = " +  data_todo.csrfmiddlewaretoken);


      fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers : {
            //"X-CSRFToken": getCookie("csrftoken"),
            "X-CSRFToken": CLE_CSRF,
            "Accept": "application/json",
            "Content-Type": "application/json"
              },
              body: JSON.stringify(data_todo)
          })
          .then(response => response.json())
          .then(function(data) {
              this.message = "Votre todo est bien pris en compte ! "
              console.log("Data is ok", data);
              // refresh
          }).catch(function(ex) {
              console.log("parsing failed", ex);
        })
        ///
        console.log("add ok " +  url)
    }
    ,
    //Fiche
    addTodo() {
      var value = this.newTodo && this.newTodo.trim()
      if (!value) {
        return
      }
      this.todos.push({
        user_id: this.user_id,
        title: value,
        completed: false
      })
      //save data in base
      this.save_todo()
      // mise a blanc
      this.newTodo  = ''
    },
    //------------
    // delete todo
    removeTodo(todo) {
      // rayer le todo
      this.todos.splice(this.todos.indexOf(todo), 1)
      // delete en vrai de la base
      var url = `/pro/api/vtodo/delete/${todo.id}`
      var CSRF_TOKEN =  getCookie("csrftoken")
      console.log("url " +  url)

      fetch(url,
        {
         method: 'delete',
         credentials: "same-origin",
         headers : {
             "X-CSRFToken": CSRF_TOKEN,
           }
        })
        .then(response => response.json())
        .then(data => this.todos = data )
        .catch(error => { console.log(error)})
        ///
    },
    //------------
    // update todo
    updateTodo(todo) {
      // rayer le todo
      this.todos.splice(this.todos.indexOf(todo), 1)
      // delete en vrai de la base
      var url = `/pro/api/vtodo/update/${todo.id}`
      console.log("url= " +  url )

      fetch(url,
        {
         method: 'put',
         credentials: "same-origin",
         headers : {
             "X-CSRFToken": getCookie("csrftoken"),
           }
        })
        .then(response => response.json())
        .then(data => this.todos = data )
        .catch(error => { console.log(error)})
        ///
    },

    editTodo(todo) {
      this.beforeEditCache = todo.title
      this.editedTodo = todo

    },

    doneEdit(todo) {
      if (!this.editedTodo) {
        //this.updateTodo(todo)
        return
      }
      this.editedTodo = null
      todo.title = todo.title.trim()

      if (!todo.title) {
        //this.removeTodo(todo)
      }
    },

    cancelEdit(todo) {
      this.editedTodo = null
      todo.title = this.beforeEditCache
    },

    removeCompleted() {
      this.todos = filters.active(this.todos)
    }
  },

  // a custom directive to wait for the DOM to be updated
  // before focusing on the input field.
  // https://vuejs.org/guide/custom-directive.html
  directives: {
    'todo-focus': function (el, binding) {
      if (binding.value) {
        el.focus()
      }
    }
  }, //directive
} // fin component_vtodo



// app Vue instance
var app = new Vue({
  // app initial state
  el: '#app',
  delimiters: ['[[', ']]'],
  components : {
    componentodo : component_vtodo ,
  },

  data(){
    return {
      message : "***  ici App TODO TODAY !!! ***",
    }
  },

})


// handle routing
function onHashChange () {
  var visibility = window.location.hash.replace(/#\/?/, '')
  if (filters[visibility]) {
    app.visibility = visibility
  } else {
    window.location.hash = ''
    app.visibility = 'all'
  }
}

window.addEventListener('hashchange', onHashChange)
onHashChange()

// mount
//app.$mount('.todoapp')
