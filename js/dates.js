n = new Date();
y = n.getFullYear();
m = n.getMonth();
d = n.getDate();

m25 = new Date(2020, 4, 25);

Months = {
    0 : "January",
    1 : "February",
    2 : "March",
    3 : "April",
    4 : "May",
    5 : "June",
    6 : "July",
    7 : "August",
    8 : "September",
    9 : "October",
    10: "November",
    11: "December"
}

Months_3 = {
    'Jan' : "January",
    'Feb' : "February",
    'Mar' : "March",
    'Apr' : "April",
    'May' : "May",
    'Jun' : "June",
    'Jul' : "July",
    'Aug' : "August",
    'Sep' : "September",
    'Oct' : "October",
    'Nov' : "November",
    'Dec' : "December"
}

Days = {
    1: "1st",
    2: "2nd",
    3: "3rd",
    4: "4th",
    5: "5th",
    6: "6th",
    7: "7th",
    8: "8th",
    9: "9th",
    10: "10th",
    11: "11th",
    12: "12th",
    13: "13th",
    14: "14th",
    15: "15th",
    16: "16th",
    17: "17th",
    18: "18th",
    19: "19th",
    20: "20th",
    21: "21st",
    22: "22nd",
    23: "23rd",
    24: "24th",
    25: "25th",
    26: "26th",
    27: "27th",
    28: "28th",
    29: "29th",
    30: "30th",
    31: "31st",
}

for(var i = 0; i < document.getElementsByClassName("date-obj").length; i++){
    document.getElementsByClassName("date-obj")[i].innerHTML = Months[m] + " " + getDayAsStr(d);
}

function getDayAsStr(num){
    return Days[num];
}

function getDaysSinceStart(){
    return (new Date(y,m,d) - m25)/86400000;
}

function getDaysSinceStartPassedDate(date){
    return (date-m25)/86400000;
}

function addDays(date, days) {
  let copy = new Date(Number(date))
  copy.setDate(date.getDate() + days)
  return copy
}

function dateToMD(date){
    Months[date.getMonth()] + " " + getDayAsStr(date.getDate());
}
