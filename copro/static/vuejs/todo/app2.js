// Full spec-compliant TodoMVC with localStorage persistence
// and hash-based routing in ~150 lines.

// localStorage persistence

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

// app Vue instance
var app = new Vue({
  // app initial state
  delimiters: ['[[', ']]'],
  data: {
    user_id : "2",
    todos: Array,
    newTodo: '',
    editedTodo: null,
    visibility: 'all',
  },

mounted() {
    //do something after mounting vue instance
    var url = `/pro/api/vtodo/${this.user_id}.json/`
    //
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
        this.save_todo()
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
    }
    ,
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
      this.newTodo = ''
    },

    removeTodo(todo) {
      this.todos.splice(this.todos.indexOf(todo), 1)
    },

    editTodo(todo) {
      this.beforeEditCache = todo.title
      this.editedTodo = todo
    },

    doneEdit(todo) {
      if (!this.editedTodo) {
        return
      }
      this.editedTodo = null
      todo.title = todo.title.trim()
      if (!todo.title) {
        this.removeTodo(todo)
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
  }
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
app.$mount('.todoapp')
