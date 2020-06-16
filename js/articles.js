//all the following is subject to change as the project progresses

//file utilized to create article objects from the collected data

var articles       = [];
var articlesByDate = [];

class Article {

    //creates an article object from a link(h), date(d), likes(l), mentions(m), image link(i), description(e), and title(t)
    constructor(h, d, l, m, i, e, t){
        this.link        = h,
        this.time        = dateToTime(d),
        this.date        = dateToDate(d),
        this.likes       = l,
        this.mentions    = m,
        this.image       = i,
        this.description = e,
        this.title       = t
    }

    get year(){
        return this.date.slice(0, this.date.indexOf(':'));
    }

    get month(){
        return this.date.slice(this.date.indexOf(':')).slice(1, this.date.indexOf(':') + 1);
    }

    get day(){
        return this.date.slice(this.date.indexOf(':')).slice(this.date.indexOf(':') + 2);
    }

    get hour(){
        return this.time.slice(0, this.time.indexOf(':'));
    }

    get minute(){
        return this.time.slice(this.time.indexOf(':')).slice(0, this.time.indexOf(':'));
    }

    get second(){
        return this.time.slice(this.time).indexOf(':').slice(this.time.indexOf(':'));
    }

}

function dateToDays(date){
    let m = date.slice(3, 5);
    m -= 5;
    let d = date.slice(6);
    return m*31 + d - 25;
}

//parses the date-time structure into a time in the form hh:mm:ss
//returns a string "hh:mm:ss"
function dateToTime(date){
    return date.slice(11,19);
}

//parses the date-time structure into a single date in the form yy:mm:dd
//returns a string "yy:mm:dd"
function dateToDate(date){
    let year = date.slice(2,4);
    let month = date.slice(5,7);
    let day = date.slice(8,10);
    return `${year}:${month}:${day}`;
}

function sortArticlesByDate(){
    for(var i = 0; i < getDaysSinceStart(); i++){
        articlesByDate.push([]);
    }
    for(var i = 0; i < articles.length; i++){
        let a = articles[i];
        index = getDaysSinceStartPassedDate(new Date(2000 + parseInt(a.year), parseInt(a.month) - 1, a.day));
        articlesByDate[index].push(a);
    }
}

function sortArticlesByMentions(){
    for(var i = 0; i < articlesByDate.length; i++){
        articlesByDate[i].sort((a, b) => {
            if( b.mentions === a.mentions ) return b.likes - a.likes;
            return b.mentions - a.mentions;
        });
    }
}

function displayList(id, date){
    if( !window.localStorage) alert("Sorry, you're using an unsupported browser");
    else {
        localStorage.myArray = JSON.stringify(articlesByDate[id]);
        localStorage.setItem('date', Months_3[date.slice(4, 7)] + " " + getDayAsStr(date.slice(8,10)));
    }
}
