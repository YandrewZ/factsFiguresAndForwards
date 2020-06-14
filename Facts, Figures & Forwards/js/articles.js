//all the following is subject to change as the project progresses

//file utilized to create article objects from the collected data

var itm = document.getElementById("")

var articles = [];

class Article {

    //creates an article object from a link(h), date(d), likes(l), and mentions(m)
    constructor(h, d, l, m){
        this.link     = h,
        this.time     = dateToTime(d),
        this.date     = dateToDate(d),
        this.likes    = l,
        this.mentions = m
    }

    get date(){
        return this.date();
    }

    get time(){
        return this.time();
    }

    get year(){
        return this.date().slice(0, this.date().indexOf(':'));
    }

    get month(){
        return this.date().slice(this.date().indexOf(':')).slice(0, this.date().indexOf(':'));
    }

    get day(){
        return this.date().slice(this.date()).indexOf(':')).slice(this.date().indexOf(':'));
    }

    get hour(){
        return this.time().slice(0, this.time().indexOf(':'));
    }

    get minute(){
        return this.time().slice(this.time().indexOf(':')).slice(0, this.time().indexOf(':'));
    }

    get second(){
        return this.time().slice(this.time()).indexOf(':')).slice(this.time().indexOf(':'));
    }

    get likes(){
        return this.likes();
    }

    get mentions(){
        return this.mentions();
    }

}

//parses the date-time structure into a time in the form hh:mm:ss
//returns a string "hh:mm:ss"
function dateToTime(date){

}

//parses the date-time structure into a single date in the form yy:mm:dd
//returns a string "yy:mm:dd"
function dateToDate(date){

}

function findEarliestArticleDate(){

}
