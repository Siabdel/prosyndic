var now = moment();
var day  = now.day();
var date = now.date(); // Number

m = moment('2013-03-01', 'YYYY-MM-DD')
This parses the given date using the given format. Returns a moment object.

Formatting
m
  .format()
  .format('dddd')
  .format('MMM Do YY') // → "Sep 2nd 07"
  .fromNow() // → "31 minutes ago"
  .calendar() // → "Last Friday at 9:32PM"

Add
m.add(1, 'day')
m.subtract(2, 'days')
m.startOf('day')
m.endOf('day')
m.startOf('hour')

moment().day(-7); // last Sunday (0 - 7)
moment().day(0); // this Sunday (0)
moment().day(7); // next Sunday (0 + 7)
moment().day(10); // next Wednesday (3 + 7)
moment().day(24); // 3 Wednesdays from now (3 + 7 + 7 + 7)

moment().day("Sunday");
moment().day("Monday");

// --
moment().isoWeekdayCalc({
  rangeStart: '1 Apr 2015',
  rangeEnd: '31 Mar 2016',
  weekdays: [1,2,3,4,5], //weekdays Mon to Fri
  exclusions: ['6 Apr 2015','7 Apr 2015']  //public holidays
}) //returns 260 (260 workdays excluding two public holidays)


if you are like me with a mind that get confused on maths:

var startDate = moment().startOf('month');
var endDate = moment().endOf('month');

var aDate = moment(startDate).day('Sunday');

var weekDays = 0;
while (aDate.isSameOrBefore(endDate)) {
   if (aDate.isSameOrAfter(startDate) && aDate.isSameOrBefore(endDate))
        weekDays++;
   aWeekDayDate.add(1, 'week');
}

//--
moment().startOf('month').add(90,'minutes')
moment().startOf('month').add({'days':1, 'hours':3 })

// returns 1-7 where 1 is Monday and 7 is Sunday
moment().isoWeekday(); // returns 1-7 where 1 is Monday and 7 is Sunday
moment().weekday(); //if today is thursday it will return 4


moment().weekdayCalc('1 Apr 2015','31 Mar 2016',[0,1,2,3,4,5,6]); //366, here Sunday is 0
moment().isoWeekdayCalc('1 Apr 2015','31 Mar 2016',[1,2,3,4,5,6,7]); //366, here Sunday is 7


// Count all Monday to Friday workdays except particular holidays:

moment().weekdayCalc('1 Apr 2015','31 Mar 2016',[1,2,3,4,5],['6 Apr 2015','7 Apr 2015'],['10 Apr 2015']); //260
moment().isoWeekdayCalc('1 Apr 2015','31 Mar 2016',[1,2,3,4,5],['6 Apr 2015','7 Apr 2015'],['10 Apr 2015']); //260
moment().weekdayCalc({
  rangeStart: '1 Apr 2015',
  rangeEnd: '31 Mar 2016',
  weekdays: [1,2,3,4,5],
  exclusions: ['6 Apr 2015','7 Apr 2015'],
  inclusions: ['10 Apr 2015']
}) //260

moment().addWorkdays(5); //Will find a date within 5 business days from now


// How many calendar days within 11 days from set of We,Th,Fr,Sa,Su, excluding Oct 15 from Oct 05:

moment('2015-10-05').weekdaysFromSetToCalendarDays(11, [0,3,4,5,6], ['2015-10-15']) //17
moment('2015-10-05').isoWeekdaysFromSetToCalendarDays(11, [3,4,5,6,7], ['2015-10-15']) //17 iso format, sunday is 7
expect(moment('2015-10-05').isoWeekdaysFromSetToCalendarDays({
  'workdays': 11,
  'weekdays': [3,4,5,6,7],
  'exclusions': ['2015-10-15']
}); //17


// npm install moment-recur
//<script src="moment.min.js"></script>
//<script src="moment-recur.js"></script>

var interval = moment( "01/01/2014" ).recur().every(2).days(); // Length Interval
interval.matches( "01/03/2014" ); // true
interval.next( 2, "L" ); // ["01/03/2014", "01/05/2014"]
interval.forget( "days" ); // Remove a rule
interval.dayOfMonth( 10 ); // Calendar Interval
interval.matches( "05/10/2014" ); // true
interval.previous( 2, "L" ); // ["12/10/2013", "11/10/2013"]


var rInterval = moment( "01/01/2014" ).recur().every(2).days();
rInterval.matches( "01/03/2014" ); // true

var rCalendar = moment.recur().every(10).dayOfMonth();
rCalendar.matches( "05/10/2014" ); // true

// -----------
// Match between 2 dates
var decemberOccurrence = recur.startDate("12/01/2017").endDate("12/31/2017").all()
