let timeline = document.getElementById('timeline');

let datesLeft = true;
let turn_right = true;
let universal_date_index = 1;
let current_article_index = 0;

let top_bp = document.getElementById("timeline_top_bp");
let mid_right_bp = document.getElementById("timeline_mid_right_bp");
let mid_left_bp = document.getElementById("timeline_mid_left_bp");

$(window).scroll(function() {
    if($(window).scrollTop() + $(window).height() >= $(document).height() - 200) {
        extendFile();
    }
})

function extendFile() {
    if(datesLeft){
        let tempArt = fetch_HEAD(global_links_array[universal_date_index], 0);

        let finished_top = createTop();

        let tempDate = addDays(m25, universal_date_index);

        finished_top.getElementsByClassName("top-node-date")[0].innerText = Months[tempDate.getMonth()] + " " + getDayAsStr(tempDate.getDate());

        timeline.appendChild(finished_top);
        if(articlesByDate[universal_date_index].length > 4){
            for(let i = 0; i < 2; i++){
                if(turn_right){
                    tempCard = createRightMid();
                } else{
                    tempCard = createLeftMid();
                }
                turn_right = !turn_right;

                tempCard.getElementsByClassName("article-title")[0].innerText = articlesByDate[universal_date_index][i].link;
                tempCard.getElementsByClassName("introductory-snippet")[0].innerText = articlesByDate[universal_date_index][i].link;
                tempCard.getElementsByClassName("source-url")[0].innerText = articlesByDate[universal_date_index][i].link;
                tempCard.getElementsByClassName("likes-and-mentions")[0].innerText = `Likes: ${global_likes_array[universal_date_index][current_article_index]}, Appearances on #BlackLivesMatter: ${global_mntns_array[universal_date_index][current_article_index]}`;

                try {
                    tempCard.getElementsByClassName("mid-node-img")[0].innerText = tempArt.image;
                } catch (e){
                    var trm = tempCard.getElementsByClassName("mid-node-img")[0];
                    var par = trm.parentNode;
                    par.removeChild(tmr);
                }

                timeline.appendChild(tempCard);
            }
            if(turn_right){
                tempCard = createRightMid();
            } else{
                tempCard = createLeftMid();
            }
            turn_right = !turn_right;
            tempCard.getElementsByClassName("article-title")[0].innerText = `View ${articlesByDate[universal_date_index].length - 2} more links shared on ${Months[tempDate.getMonth()]} ${getDayAsStr(tempDate.getDate())}`;
            tempCard.getElementsByClassName("introductory-snippet")[0].innerText = articlesByDate[universal_date_index][i].link;

            timeline.appendChild(tempCard);

        } else{
            for(let i = 0; i < articlesByDate[universal_date_index].length; i++){
                if(turn_right){
                    tempCard = createRightMid();
                } else{
                    tempCard = createLeftMid();
                }
                turn_right = !turn_right;
                //
                // articlesByDate[universal_date_index][current_article_index].description = tempArt.description;
                // articlesByDate[universal_date_index][current_article_index].image = tempArt.image;
                // articlesByDate[universal_date_index][current_article_index].title = tempArt.title;

                // try{
                //     tempCard.getElementsByClassName("article-title")[0].innerText = articlesByDate[universal_date_index][current_article_index].title;
                //     tempCard.getElementsByClassName("introductory-snippet")[0].innerText = articlesByDate[universal_date_index][current_article_index].description;
                //     tempCard.getElementsByClassName("source-url")[0].innerText = articlesByDate[universal_date_index][current_article_index].link;
                //     tempCard.getElementsByClassName("likes-and-mentions")[0].innerText = `Likes: ${global_likes_array[universal_date_index][current_article_index]}, Appearances on #BlackLivesMatter: ${global_mntns_array[universal_date_index][current_article_index]}`;
                //     tempCard.getElementsByClassName("mid-node-image")[0].innerText = articlesByDate[universal_date_index][current_article_index].image;
                // } catch (e){
                //
                // }

                tempCard.getElementsByClassName("article-title")[0].innerText = articlesByDate[universal_date_index][i].link;
                tempCard.getElementsByClassName("introductory-snippet")[0].innerText = articlesByDate[universal_date_index][i].link;
                tempCard.getElementsByClassName("source-url")[0].innerText = articlesByDate[universal_date_index][i].link;
                tempCard.getElementsByClassName("likes-and-mentions")[0].innerText = `Likes: ${global_likes_array[universal_date_index][i]}, Appearances on #BlackLivesMatter: ${global_mntns_array[universal_date_index][i]}`;

                timeline.appendChild(tempCard);
            }
        }
        // let clone = top_bp.cloneNode(true);
        // clone.id = global_dates_array[universal_date_index];
        //
        //
        //

    }
    universal_date_index++;
}

//fucntion for creating a card on the right side of the screen
function createRightMid(){
    let mid_right_clone = mid_right_bp.cloneNode(true);
    mid_right_clone.id = "";
    mid_right_clone.style = "";
    return mid_right_clone;
}

//function for creating a card on the left side of the screen
function createLeftMid(){
    let mid_left_clone = mid_left_bp.cloneNode(true);
    mid_left_clone.id = "";
    mid_left_clone.style = "";
    return mid_left_clone;
}

//function for creating a pointer for the date
function createTop() {
    let top_clone = top_bp.cloneNode(true);
    top_clone.id = global_dates_array[universal_date_index];
    top_clone.style = "";
    return top_clone;
}

async function fetch_HEAD(url, index){
    console.log(url);
    let data = '';
    const proxies = ["https://cors-anywhere.herokuapp.com/", "https://cors-proxy.htmldriven.com/?url=", "https://thingproxy.freeboard.io/fetch/"]
    if(index < proxies.length){
        try {
            const response = await fetch(proxies[index] + url, {method: 'GET'});
            data = await response.text();
        } catch(e) {
            console.log(e);
            fetch_HEAD(url, index + 1);
        }
    } else {
        console.log('All proxies have failed');
    }
    let parser = new DOMParser();
    let xmlDoc = parser.parseFromString(data, 'text/xml');
    console.log(xmlDoc);
    let ret = {};
    try{ret.image = xmlDoc.querySelector('[rel="image_src"]')[0].href; return ret;} catch{}
    try{ret.image = xmlDoc.querySelector('[property="og:image"]')[0].content; return ret;} catch{}

    return ret;
}
