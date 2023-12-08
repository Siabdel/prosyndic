// this automatically intercepts each ajax request, checks if it is going to
// your server, and adds the csrf token if so:
$(document).ajaxSend(function(event, xhr, settings) {
  //* see this as a html "dictionary" that is middleground between django and js, remember its a bad practice to put js in html file */
  var csrf_token = '{{csrf_token}}' ;
  // note POST method does not cache

  $.ajaxSetup({timeout: 2000, }); // docs -- api.jquery.com/jQuery.ajaxSetup/

  function sameOrigin(url) {
      var host = document.location.host,
          protocol = document.location.protocol,
          sr_origin = '//' + host,
          origin = protocol + sr_origin;

      return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
          (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
          !(/^(\/\/|http:|https:).*/.test(url));
  }

  function safeMethod(method) {
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
      xhr.setRequestHeader("X-CSRFToken", csrf_token);
  }

  });

$(document).ready(function() {
    //$('[data-toggle="popover"]').popover();
    $('[data-toggle="popover"]').tooltip();
    $('#id_update_qte').click(function(event){
      // --       alert("ok ..");
      var quantite = prompt('titre',  event.quantite_prevue, button = {"ok" : true, "cancel": false } );
    });


    // note POST method does not cache

    $.ajaxSetup({timeout: 2000, }); // docs -- api.jquery.com/jQuery.ajaxSetup/

    var aujourdhui  = new Date();
    var d = aujourdhui.getDate();
    var m = aujourdhui.getMonth();
    var y = aujourdhui.getFullYear();
    var currentLangCode = 'fr';

    // datepicker  calendar
    $.datepicker.setDefaults($.datepicker.regional['fr']);
    // initialize the datepicker
    $('#datepicker').datepicker({
	    dateFormat: 'yy-mm-dd', // needed for defaultDate
	    //defaultDate: '2014-01-12',
	    showWeek: true,
	    showButtonPanel: true,
	    // on select
	    onSelect: function(dateText, inst) {
          var dateSelect = new Date(dateText);
          $('#calendar').fullCalendar('gotoDate', dateSelect);
      },
      // calcul week
      calculateWeek: function(nativeDate) {
        // use Moment to calculate the local week number
        //return moment(nativeDate).lang(currentLangCode).week();
        return moment(nativeDate).local().week();

        // moment().startOf('month').add(90,'minutes')
        //moment().startOf('month').add({'days':1, 'hours':3 })
      }
    });
    // Fullcalendar

    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next aujourdhui',
            center: 'title',
            //right: 'month,agendaWeek,agendaDay'
            right: 'month,basicWeek,basicDay'
        },

        lang: 'fr', // langue choisi francais
        timezone:"Europe/Paris",
        firstDay : 4,
        hiddenDays:[7], // on cache journee Dimanche
        editable : true,
        droppable : true,
        //data load
        // defaultView: 'agendaWeek', // defaultView: 'timelineDay', // defaultView: 'month',
        defaultView : 'basicWeek',
        events : "/of/api/get_of/{{status_of}}/" ,
        resources : "{% url 'api_get_machine' %}",

        //eventColor: '#3780AA',
        //eventTextColor : 'white',
        //eventBackgroundColor : '#2b5de5',

        defaultDate: '{{ date_semaine_start }}',

        eventRender: function(event, element) {
            console.log("event Render !!");
            // $('#calendar').fullCalendar('gotoDate', moment(aujourdhui).local() );
            var class_name = element[0].className;
            //element[0].className = 'fc-title' ;
            var edit_url = "{% url 'api_edit_of' 12345  %}".replace(/12345/, event.event_id);
            var edit_button = "<a target='_blanc' href='" + edit_url +
                "'> <button type='button' class='btn btn-warning btn-sm pull-right'><span class='fa fa-pencil'></span></button></a>"
            //var delete_url = "{ url 'api_delete_event' 12345  }".replace(/12345/, event.event_id);
            //var delete_button = "<a href='"+ delete_url + "'> <button type='button' class='btn btn-primary btn-sm pull-right'><span class='glyphicon glyphicon-trash'></span>Del</button></a>"

            title = element.children().find( '.fc-time' );
            //title.addClass('fc-event');
            body = element.children().find( '.fc-title' );
            //alert(event.eventColor);
            title.html(" <li style='color:12345'  class='list-group-item text-bold'> OF : ".replace(/12345/, event.eventColor) + event.id + "</li>" );
            //title.css("background-color", "yellow");
            body.html("<hr>" +
                       "<li class='list-unstyled'>Commande : "  + event.commande + "</li>" +
                       "<li class='list-unstyled'>Client : "  + event.client + "</li>" +
                       "<li class='list-unstyled'>Machine : "   + event.machine + "</li>" +
                       "<li class='list-unstyled'>Formule : "   + event.formule_cond + "</li>" +
                       "<li class='list-unstyled'>Date de liv : " + event.date_livraison + "</li>" +
                       "<li class='list-unstyled'> <A class='fc-blanc' id='id_update_qte' onlick='alert('ok');' href='#'> Quantite : " + event.quantite + " U </A></li>"  ) ;

            chaine = "<a href='#' data-toggle='popover' title='Popover Header' data-content='Some content inside the popover ...'>Toggle popover</a> " +
                      "commande :" + event.commande

            body.append(edit_button  + '<br>');
            // Affichage en semaine
            //$('#calendar').fullCalendar('changeView', 'agendaWeek');
            // moment().startOf('month').add(90,'minutes')
            //moment().startOf('month').add({'days':1, 'hours':3 })
          },


        resourceFilter__: function(resource) {
                        var active = $("input").map(function() {
                            return this.checked ? this.name : null;
                        }).get();
                        return $.inArray(resource.id, active) > -1;
                    },
        eventDrop: function(event, delta, revertFunc) {
           if (event.start  ){
             console.log("event Drop !! " + event.start.toISOString());
             $.ajax({
                     type: 'POST',
                     url: "{% url 'api_move_of' %}",
                     dataType: 'json',
                     data : {
                          'id': event.id,

                         'start': event.start.toISOString(),
                         //'end' : event.end.toISOString(),
                         'delta' : delta.asMinutes(),
                         'calendar_slug' : '{{calendar_slug}}',
                     },

                     beforeSend: function(request) {
                         //request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                         return request.setRequestHeader('X-CSRF-Token', $("meta[name='token']").attr('content'));
                       },
                     success : function(result) {
                         if (result.success) $('#feedback input').attr('value', '');
                         console.log(" Move Success!! " + result);

                         $('#calendar').fullCalendar('refetchEvents');

                         },
                     error : function(req, status, error) {
                         console.log(error);
                     }
                 });
            }
         },

        eventMouseover : function(event, jsEvent, view){
          console.log(" event Mouse Over !!");
          //popup
          $('#element').popover('show');
        },

        eventClick__ : function(event, jsEvent, view){
          // trace info ...
          console.log(" event Click !!");
          console.log('Event title: ' + event.title);
          console.log('Event url: ' + jsEvent.url + event.url );
          console.log('Coordinates: pageX, pageY ' + jsEvent.pageX + ',' + jsEvent.pageY);
          console.log('View: name ' + view.name );
          // change the border color just for fun
          if (event.url) {
            window.open(event.url);
            return false;
          }

          $(this).css('border-color', 'red');

          var quantite = prompt('titre',  event.quantite_prevue, button = {"ok" : true, "cancel": false } );

          if(quantite){
            // event.quantite_prevue = quantite_prevue;
            $.ajax({
                    type: 'POST',
                    url: "{% url 'api_update_qte_of' %}",
                    dataType: 'json',
                    data : {
                         'id': event.id,
                        'quantite_prevue' : quantite,
                        'calendar_slug' : '{{calendar_slug}}',
                    },
                    success : function(result) {
                        if (result.success) $('#feedback input').attr('value', '');
                        console.log(" Move Success!! " + result);

                        $('#calendar').fullCalendar('refetchEvents');
                        },
                    error : function(req, status, error) {
                        console.log(error);
                    }
                });
          } //fin if
        } //  fin eventClick
      }); // FullCalendar

    }); // document.ready
    //------------------------------------------
    //---------FIN--------------
    //------------------------------------------
