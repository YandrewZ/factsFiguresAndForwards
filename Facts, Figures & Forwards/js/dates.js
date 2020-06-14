n = new Date();
y = n.getFullYear();
m = n.getMonth();
d = n.getDate();

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

for(var i = 0; i < document.getElementsByClassName("date-obj").length; i++){
    document.getElementsByClassName("date-obj")[i].innerHTML = Months[m] + " " + getDayAsStr(d);
}
function getDayAsStr(num){
    if(num % 10 == 1){
        return num + "st";
    } else if(num % 10 == 2){
        return num + "nd";
    }
    return num + "th";
}
